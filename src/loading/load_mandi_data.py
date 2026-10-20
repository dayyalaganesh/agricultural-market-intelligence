
import argparse
import csv
from pathlib import Path

import psycopg
from psycopg import sql

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "mandi_prices_transformed.csv"
)

DATABASE_NAME = "agricultural_market_intelligence"
DATABASE_USER = "ganesh"
TABLE_NAME = "mandi_prices"

EXPECTED_COLUMNS = [
    "State",
    "District",
    "Market",
    "Commodity",
    "Variety",
    "Grade",
    "Arrival_Date",
    "Min_Price",
    "Max_Price",
    "Modal_Price",
]

DB_COLUMNS = [
    "state",
    "district",
    "market",
    "commodity",
    "variety",
    "grade",
    "arrival_date",
    "min_price",
    "max_price",
    "modal_price",
]


def load_mandi_data(dry_run=True):
    """Validate and stage CSV data; refresh PostgreSQL only when requested."""

    print("AGRICULTURAL MARKET DATA LOADING")
    print("=" * 38)
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLY CHANGES'}")

    if not INPUT_FILE.is_file():
        raise FileNotFoundError(f"Processed CSV not found: {INPUT_FILE}")

    # Validate the CSV header and count its records.
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                f"CSV schema mismatch.\n"
                f"Expected: {EXPECTED_COLUMNS}\n"
                f"Found: {reader.fieldnames}"
            )

        expected_count = sum(1 for _ in reader)

    if expected_count == 0:
        raise ValueError("CSV contains no data records. Load cancelled.")

    connection_string = (
        f"dbname={DATABASE_NAME} user={DATABASE_USER}"
    )

    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            # Stage records in a temporary table.
            cur.execute(
                sql.SQL(
                    "CREATE TEMP TABLE staging_mandi_prices "
                    "(LIKE {} INCLUDING DEFAULTS) ON COMMIT DROP"
                ).format(sql.Identifier("public", TABLE_NAME))
            )

            insert_staging = sql.SQL(
                "INSERT INTO staging_mandi_prices ({}) VALUES ({})"
            ).format(
                sql.SQL(", ").join(
                    sql.Identifier(column) for column in DB_COLUMNS
                ),
                sql.SQL(", ").join(
                    sql.Placeholder() for _ in DB_COLUMNS
                ),
            )

            # Read and insert every CSV record into staging.
            with INPUT_FILE.open(
                "r", encoding="utf-8-sig", newline=""
            ) as file:
                reader = csv.DictReader(file)

                for row_number, row in enumerate(reader, start=2):
                    try:
                        values = (
                            row["State"].strip(),
                            row["District"].strip(),
                            row["Market"].strip(),
                            row["Commodity"].strip(),
                            row["Variety"].strip(),
                            row["Grade"].strip(),
                            row["Arrival_Date"],
                            row["Min_Price"],
                            row["Max_Price"],
                            row["Modal_Price"],
                        )
                        cur.execute(insert_staging, values)

                    except (KeyError, TypeError, ValueError, AttributeError) as exc:
                        raise ValueError(
                            f"Invalid CSV record at line {row_number}"
                        ) from exc

            cur.execute("SELECT COUNT(*) FROM staging_mandi_prices")
            staged_count = cur.fetchone()[0]

            if staged_count != expected_count:
                raise RuntimeError(
                    f"Staging count mismatch: expected {expected_count}, "
                    f"loaded {staged_count}"
                )

            if dry_run:
                # Do not modify the existing target table.
                print("DRY RUN: staging validation successful.")
                print("Existing PostgreSQL records will NOT be changed.")
                final_count = None

            else:
                # Replace the target records inside the same transaction.
                cur.execute(
                    sql.SQL("DELETE FROM {}").format(
                        sql.Identifier("public", TABLE_NAME)
                    )
                )

                cur.execute(
                    sql.SQL(
                        "INSERT INTO {} ({}) "
                        "SELECT {} FROM staging_mandi_prices"
                    ).format(
                        sql.Identifier("public", TABLE_NAME),
                        sql.SQL(", ").join(
                            sql.Identifier(column) for column in DB_COLUMNS
                        ),
                        sql.SQL(", ").join(
                            sql.Identifier(column) for column in DB_COLUMNS
                        ),
                    )
                )

                cur.execute(
                    sql.SQL("SELECT COUNT(*) FROM {}").format(
                        sql.Identifier("public", TABLE_NAME)
                    )
                )
                final_count = cur.fetchone()[0]

                if final_count != expected_count:
                    raise RuntimeError(
                        f"Final count mismatch: expected {expected_count}, "
                        f"found {final_count}"
                    )

    # The transaction commits only after all checks pass.
    print(f"Source records: {expected_count}")
    print(f"Staged records: {staged_count}")

    if dry_run:
        print("Database refresh: NOT performed")
    else:
        print(f"Records in PostgreSQL: {final_count}")
        print("Database refresh completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load transformed mandi data into PostgreSQL."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Replace existing PostgreSQL records after staging validation.",
    )
    args = parser.parse_args()

    load_mandi_data(dry_run=not args.apply)
