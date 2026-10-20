
import csv
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "mandi_prices_raw.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "mandi_prices_transformed.csv"

PRICE_COLUMNS = ["Min_Price", "Max_Price", "Modal_Price"]

COLUMN_RENAMES = {
    "Min_x0020_Price": "Min_Price",
    "Max_x0020_Price": "Max_Price",
    "Modal_x0020_Price": "Modal_Price",
}


def transform_mandi_data():
    """Standardize columns, prices, and dates; then save processed data."""

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
                transformed_row = {
                    COLUMN_RENAMES.get(column, column): value.strip()
                    for column, value in row.items()
                    if column is not None
                }

                # Standardize the date as YYYY-MM-DD.
                try:
                    parsed_date = datetime.strptime(
                        transformed_row["Arrival_Date"], "%d/%m/%Y"
                    )
                    transformed_row["Arrival_Date"] = parsed_date.strftime(
                        "%Y-%m-%d"
                    )
                except ValueError as error:
                    raise ValueError(
                        f"Invalid Arrival_Date: {transformed_row['Arrival_Date']}"
                    ) from error

                # Validate and normalize price fields.
                for column in PRICE_COLUMNS:
                    try:
                        price = float(transformed_row[column])
                    except (ValueError, KeyError) as error:
                        raise ValueError(
                            f"Invalid price in column {column}: "
                            f"{transformed_row.get(column)}"
                        ) from error

                    if price < 0:
                        raise ValueError(
                            f"Negative price in {column}: {price}"
                        )

                    if price.is_integer():
                        transformed_row[column] = str(int(price))
                    else:
                        transformed_row[column] = str(price)

                # Skip exact duplicate rows after standardization.
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
