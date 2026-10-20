
import csv
import math
from datetime import datetime
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "mandi_prices_raw.csv"

PRICE_COLUMNS = [
    "Min_x0020_Price",
    "Max_x0020_Price",
    "Modal_x0020_Price",
]

REQUIRED_COLUMNS = [
    "State",
    "District",
    "Market",
    "Commodity",
    "Variety",
    "Grade",
    "Arrival_Date",
    *PRICE_COLUMNS,
]

DATE_FORMAT = "%d/%m/%Y"


def validate_data():
    total_records = 0
    missing_values = Counter()
    invalid_prices = 0
    negative_prices = Counter()
    min_greater_than_max = 0
    modal_below_min = 0
    modal_above_max = 0
    invalid_dates = 0
    dates = []
    unique_rows = set()
    duplicate_rows = 0

    if not DATA_FILE.is_file():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    with DATA_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != REQUIRED_COLUMNS:
            raise ValueError(
                f"Unexpected CSV columns: {reader.fieldnames}"
            )

        for row in reader:
            total_records += 1

            # Check missing values
            for column in REQUIRED_COLUMNS:
                value = row.get(column)
                if value is None or not value.strip():
                    missing_values[column] += 1

            # Check exact duplicate records
            row_key = tuple(row.get(column) for column in REQUIRED_COLUMNS)
            if row_key in unique_rows:
                duplicate_rows += 1
            else:
                unique_rows.add(row_key)

            # Validate arrival dates
            try:
                arrival_date = datetime.strptime(
                    row["Arrival_Date"], DATE_FORMAT
                ).date()
                dates.append(arrival_date)
            except (ValueError, TypeError):
                invalid_dates += 1

            # Validate numeric and finite prices
            try:
                prices = [
                    float(row[column]) for column in PRICE_COLUMNS
                ]
                if not all(math.isfinite(price) for price in prices):
                    raise ValueError("Prices must be finite numbers")
            except (ValueError, TypeError):
                invalid_prices += 1
                continue

            minimum, maximum, modal = prices

            # Check negative prices
            for column, value in zip(PRICE_COLUMNS, prices):
                if value < 0:
                    negative_prices[column] += 1

            # Check price consistency
            if minimum > maximum:
                min_greater_than_max += 1
            if modal < minimum:
                modal_below_min += 1
            if modal > maximum:
                modal_above_max += 1

    # Build the validation report
    report_lines = [
        "AGRICULTURAL MARKET DATA QUALITY REPORT",
        "=" * 45,
        f"Dataset: {DATA_FILE.name}",
        f"Total records: {total_records}",
        f"Expected columns: {len(REQUIRED_COLUMNS)}",
        f"Unique records: {len(unique_rows)}",
        f"Duplicate extra rows: {duplicate_rows}",
        "",
        "Missing values:",
    ]

    for column in REQUIRED_COLUMNS:
        report_lines.append(
            f"  {column}: {missing_values[column]}"
        )

    report_lines.extend([
        "",
        "Price validation:",
        f"Invalid numeric or non-finite price rows: {invalid_prices}",
        f"Minimum > maximum: {min_greater_than_max}",
        f"Modal < minimum: {modal_below_min}",
        f"Modal > maximum: {modal_above_max}",
        "",
        "Negative prices:",
    ])

    for column in PRICE_COLUMNS:
        report_lines.append(
            f"  {column}: {negative_prices[column]}"
        )

    report_lines.extend([
        "",
        "Date validation:",
        f"Invalid dates: {invalid_dates}",
        f"Distinct valid dates: {len(set(dates))}",
        f"Earliest date: {min(dates) if dates else 'N/A'}",
        f"Latest date: {max(dates) if dates else 'N/A'}",
        "",
        "Validation report completed.",
    ])

    report = "\n".join(report_lines)
    print(report)

    report_dir = PROJECT_ROOT / "data" / "quality_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / "mandi_data_quality_report.txt"
    report_file.write_text(report + "\n", encoding="utf-8")

    print(f"\nReport saved to: {report_file}")


if __name__ == "__main__":
    validate_data()
