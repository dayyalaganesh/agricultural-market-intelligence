
import csv
from pathlib import Path

# Locate the project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Define the raw dataset path
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "mandi_prices_raw.csv"

# Define the expected columns
EXPECTED_COLUMNS = [
    "State",
    "District",
    "Market",
    "Commodity",
    "Variety",
    "Grade",
    "Arrival_Date",
    "Min_x0020_Price",
    "Max_x0020_Price",
    "Modal_x0020_Price",
]


def ingest_mandi_data():
    """Read the raw agricultural market CSV and verify its schema."""

    print("AGRICULTURAL MARKET DATA INGESTION")
    print("=" * 40)

    # Check whether the input file exists
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT_FILE}")

    print(f"Input file: {INPUT_FILE.name}")

    # Read the CSV file
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        actual_columns = reader.fieldnames

        # Validate the column names
        if actual_columns != EXPECTED_COLUMNS:
            raise ValueError(
                f"Schema mismatch!\n"
                f"Expected: {EXPECTED_COLUMNS}\n"
                f"Found: {actual_columns}"
            )

        # Count records without loading the entire dataset into memory
        record_count = sum(1 for _ in reader)

    print(f"Schema validation: PASSED")
    print(f"Records ingested: {record_count}")
    print("Ingestion completed successfully.")


if __name__ == "__main__":
    ingest_mandi_data()
