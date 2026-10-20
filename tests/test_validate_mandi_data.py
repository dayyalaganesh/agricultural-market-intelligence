
import csv
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.validation import validate_mandi_data as validator


class TestMandiDataValidation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.test_root = Path(self.temp_dir.name)
        self.data_file = self.test_root / "mandi_prices_raw.csv"
        self.report_dir = self.test_root / "data" / "quality_reports"

        self.valid_row = {
            "State": "Andhra Pradesh",
            "District": "Guntur",
            "Market": "Guntur",
            "Commodity": "Paddy",
            "Variety": "Common",
            "Grade": "FAQ",
            "Arrival_Date": "18/10/2026",
            "Min_x0020_Price": "2000",
            "Max_x0020_Price": "2500",
            "Modal_x0020_Price": "2250",
        }

    def run_validation(self, rows):
        with self.data_file.open(
            "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file, fieldnames=validator.REQUIRED_COLUMNS
            )
            writer.writeheader()
            writer.writerows(rows)

        output = StringIO()

        with (
            patch.object(validator, "DATA_FILE", self.data_file),
            patch.object(validator, "PROJECT_ROOT", self.test_root),
            redirect_stdout(output),
        ):
            validator.validate_data()

        return output.getvalue()

    def test_valid_record_passes_checks(self):
        report = self.run_validation([self.valid_row.copy()])

        self.assertIn("Total records: 1", report)
        self.assertIn("Invalid dates: 0", report)
        self.assertIn(
            "Invalid numeric or non-finite price rows: 0", report
        )
        self.assertIn("Report saved to:", report)

    def test_missing_commodity_is_reported(self):
        row = self.valid_row.copy()
        row["Commodity"] = ""

        report = self.run_validation([row])

        self.assertIn("Commodity: 1", report)

    def test_invalid_date_is_reported(self):
        row = self.valid_row.copy()
        row["Arrival_Date"] = "31/02/2026"

        report = self.run_validation([row])

        self.assertIn("Invalid dates: 1", report)

    def test_nan_price_is_reported(self):
        row = self.valid_row.copy()
        row["Min_x0020_Price"] = "NaN"

        report = self.run_validation([row])

        self.assertIn(
            "Invalid numeric or non-finite price rows: 1", report
        )

    def test_infinite_price_is_reported(self):
        row = self.valid_row.copy()
        row["Max_x0020_Price"] = "inf"

        report = self.run_validation([row])

        self.assertIn(
            "Invalid numeric or non-finite price rows: 1", report
        )

    def test_negative_price_is_reported(self):
        row = self.valid_row.copy()
        row["Min_x0020_Price"] = "-10"

        report = self.run_validation([row])

        self.assertIn("Min_x0020_Price: 1", report)

    def test_minimum_greater_than_maximum_is_reported(self):
        row = self.valid_row.copy()
        row["Min_x0020_Price"] = "3000"
        row["Max_x0020_Price"] = "2000"

        report = self.run_validation([row])

        self.assertIn("Minimum > maximum: 1", report)

    def test_modal_below_minimum_is_reported(self):
        row = self.valid_row.copy()
        row["Modal_x0020_Price"] = "1500"

        report = self.run_validation([row])

        self.assertIn("Modal < minimum: 1", report)

    def test_modal_above_maximum_is_reported(self):
        row = self.valid_row.copy()
        row["Modal_x0020_Price"] = "3000"

        report = self.run_validation([row])

        self.assertIn("Modal > maximum: 1", report)

    def test_duplicate_record_is_reported(self):
        row = self.valid_row.copy()

        report = self.run_validation([row, row.copy()])

        self.assertIn("Total records: 2", report)
        self.assertIn("Duplicate extra rows: 1", report)

    def test_quality_report_is_saved(self):
        self.run_validation([self.valid_row.copy()])

        report_file = (
            self.report_dir / "mandi_data_quality_report.txt"
        )
        self.assertTrue(report_file.is_file())
        self.assertIn(
            "Total records: 1",
            report_file.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
