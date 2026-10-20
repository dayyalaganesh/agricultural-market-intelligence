
import csv
from datetime import datetime
from collections import Counter
from pathlib import Path

# Locate the project and raw dataset
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "mandi_prices_raw.csv"

PRICE_COLUMNS = [
    "Min_x0020_Price",
    "Max_x0020_Price",
    "Modal_x0020_Price",
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

    with DATA_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        required_columns = [
            "State", "District", "Market", "Commodity",
            "Variety", "Grade", "Arrival_Date",
            *PRICE_COLUMNS,
        ]

        if reader.fieldnames != required_columns:
            raise ValueError(
                f"Unexpected CSV columns: {reader.fieldnames}"
            )

        for row in reader:
            total_records += 1

            # Check missing values
            for column, value in row.items():
                if value is None or not value.strip():
                    missing_values[column] += 1

            # Check exact duplicate records
            row_key = tuple(row.values())
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

            # Validate prices
            try:
                minimum = float(row[PRICE_COLUMNS[0]])
                maximum = float(row[PRICE_COLUMNS[1]])
                modal = float(row[PRICE_COLUMNS[2]])
            except (ValueError, TypeError):
                invalid_prices += 1
                continue

            for column, value in zip(
                PRICE_COLUMNS, [minimum, maximum, modal]
            ):
                if value < 0:
                    negative_prices[column] += 1

            if minimum > maximum:
                min_greater_than_max += 1
            if modal < minimum:
                modal_below_min += 1
            if modal > maximum:
                modal_above_max += 1

    # Print the validation report
    print("\nAGRICULTURAL MARKET DATA QUALITY REPORT")
    print("=" * 45)
    print(f"Dataset: {DATA_FILE.name}")
    print(f"Total records: {total_records}")
    print(f"Expected columns: {len(required_columns)}")
    print(f"Unique records: {len(unique_rows)}")
    print(f"Duplicate extra rows: {duplicate_rows}")

    print("\nMissing values:")
    for column in required_columns:
        print(f"  {column}: {missing_values[column]}")

    print("\nPrice validation:")
    print(f"Invalid numeric price rows: {invalid_prices}")
    print(f"Minimum > maximum: {min_greater_than_max}")
    print(f"Modal < minimum: {modal_below_min}")
    print(f"Modal > maximum: {modal_above_max}")

    print("\nNegative prices:")
    for column in PRICE_COLUMNS:
        print(f"  {column}: {negative_prices[column]}")

    print("\nDate validation:")
    print(f"Invalid dates: {invalid_dates}")
    print(f"Distinct valid dates: {len(set(dates))}")
    print(f"Earliest date: {min(dates) if dates else 'N/A'}")
    print(f"Latest date: {max(dates) if dates else 'N/A'}")

    print("\nValidation report completed.")
    
    

    # Save the report to a text file
    report_dir = PROJECT_ROOT / "data" / "quality_reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / "mandi_data_quality_report.txt"
    report_file.write_text(
        "Agricultural Market Data Quality Report\n"
        f"Dataset: {DATA_FILE.name}\n"
        f"Total records: {total_records}\n"
        f"Unique records: {len(unique_rows)}\n"
        f"Duplicate extra rows: {duplicate_rows}\n"
        f"Invalid numeric price rows: {invalid_prices}\n"
        f"Minimum > maximum: {min_greater_than_max}\n"
        f"Modal < minimum: {modal_below_min}\n"
        f"Modal > maximum: {modal_above_max}\n"
        f"Invalid dates: {invalid_dates}\n"
        f"Distinct valid dates: {len(set(dates))}\n"
        f"Earliest date: {min(dates) if dates else 'N/A'}\n"
        f"Latest date: {max(dates) if dates else 'N/A'}\n",
        encoding="utf-8",
    )

    print(f"Report saved to: {report_file}")



if __name__ == "__main__":
    validate_data()
