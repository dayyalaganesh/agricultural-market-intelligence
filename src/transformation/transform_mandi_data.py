
import csv
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "mandi_prices_raw.csv"
OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "mandi_prices_transformed.csv"
)

PRICE_COLUMNS = ["Min_Price", "Max_Price", "Modal_Price"]

COLUMN_RENAMES = {
    "Min_x0020_Price": "Min_Price",
    "Max_x0020_Price": "Max_Price",
    "Modal_x0020_Price": "Modal_Price",
}


def standardize_columns(row):
    """Rename price columns and trim surrounding whitespace."""
    return {
        COLUMN_RENAMES.get(column, column): value.strip()
        for column, value in row.items()
    }


def standardize_date(date_value):
    """Convert DD/MM/YYYY to YYYY-MM-DD."""
    parsed_date = datetime.strptime(date_value, "%d/%m/%Y")
    return parsed_date.strftime("%Y-%m-%d")


def validate_and_standardize_prices(row):
    """Validate prices and normalize their numeric representation."""
    for column in PRICE_COLUMNS:
        price = float(row[column])

        if price < 0:
            raise ValueError(f"Negative price in {column}: {price}")

        row[column] = str(int(price)) if price.is_integer() else str(price)

    return row


def transform_row(row):
    """Apply the transformation rules to one CSV record."""
    transformed_row = standardize_columns(row)
    transformed_row["Arrival_Date"] = standardize_date(
        transformed_row["Arrival_Date"]
    )
    return validate_and_standardize_prices(transformed_row)


def transform_mandi_data():
    """Transform the raw CSV and save the processed output."""
    print("AGRICULTURAL MARKET DATA TRANSFORMATION")
    print("=" * 42)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    seen_rows = set()
    transformed_count = 0
    duplicate_count = 0

    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)

        if reader.fieldnames is None:
            raise ValueError("Input CSV has no header.")

        output_columns = [
            COLUMN_RENAMES.get(column, column)
            for column in reader.fieldnames
        ]

        with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=output_columns)
            writer.writeheader()

            for row in reader:
                transformed_row = transform_row(row)

                row_key = tuple(
                    transformed_row.get(column, "")
                    for column in output_columns
                )

                if row_key in seen_rows:
                    duplicate_count += 1
                    continue

                seen_rows.add(row_key)
                writer.writerow(transformed_row)
                transformed_count += 1

    print(f"Input file: {INPUT_FILE.name}")
    print(f"Transformed records: {transformed_count}")
    print(f"Duplicate rows skipped: {duplicate_count}")
    print(f"Output file: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    print("Transformation completed successfully.")


if __name__ == "__main__":
    transform_mandi_data()
