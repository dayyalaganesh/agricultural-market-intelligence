
import unittest

from src.transformation.transform_mandi_data import (
    standardize_columns,
    standardize_date,
    validate_and_standardize_prices,
    transform_row,
)


class TestMandiDataTransformation(unittest.TestCase):

    def test_column_names_are_standardized(self):
        row = {
            "Min_x0020_Price": "2500",
            "Max_x0020_Price": "3000",
            "Modal_x0020_Price": "2700",
        }

        result = standardize_columns(row)

        self.assertIn("Min_Price", result)
        self.assertIn("Max_Price", result)
        self.assertIn("Modal_Price", result)

    def test_date_is_standardized(self):
        result = standardize_date("18/10/2026")

        self.assertEqual(result, "2026-10-18")

    def test_invalid_date_is_rejected(self):
        with self.assertRaises(ValueError):
            standardize_date("31/02/2026")

    def test_prices_are_standardized(self):
        row = {
            "Min_Price": "2500.0",
            "Max_Price": "3000.0",
            "Modal_Price": "2700.0",
        }

        result = validate_and_standardize_prices(row)

        self.assertEqual(result["Min_Price"], "2500")
        self.assertEqual(result["Max_Price"], "3000")
        self.assertEqual(result["Modal_Price"], "2700")

    def test_negative_price_is_rejected(self):
        row = {
            "Min_Price": "-100",
            "Max_Price": "3000",
            "Modal_Price": "2700",
        }

        with self.assertRaises(ValueError):
            validate_and_standardize_prices(row)

    def test_complete_row_transformation(self):
        row = {
            "State": " Tripura ",
            "District": "Dhalai",
            "Market": "Kulai APMC",
            "Commodity": "Bottle gourd",
            "Variety": "Bottle Gourd",
            "Grade": "Grade B",
            "Arrival_Date": "18/10/2026",
            "Min_x0020_Price": "2500.0",
            "Max_x0020_Price": "3000.0",
            "Modal_x0020_Price": "2700.0",
        }

        result = transform_row(row)

        self.assertEqual(result["State"], "Tripura")
        self.assertEqual(result["Arrival_Date"], "2026-10-18")
        self.assertEqual(result["Min_Price"], "2500")
        self.assertEqual(result["Max_Price"], "3000")
        self.assertEqual(result["Modal_Price"], "2700")


if __name__ == "__main__":
    unittest.main()
