# Agricultural Market Intelligence Platform

An end-to-end data engineering project that ingests, transforms, validates, and loads Indian agricultural market price data into PostgreSQL for SQL-based analysis.

## Project Overview

This project demonstrates a batch data pipeline built with Python and PostgreSQL. It processes agricultural commodity prices from mandi markets, applies data-quality checks, and stores structured records for analysis.

**Current dataset:** 10,797 records
**Pipeline:** CSV → Ingestion → Transformation → Validation → PostgreSQL → SQL Analytics

## Key Features

- **Data Ingestion:** Checks source-file availability and validates the expected CSV schema.
- **Data Transformation:** Standardizes column names and dates, validates prices, and removes duplicate rows.
- **Data Quality:** Checks missing values, duplicate records, invalid dates, negative or non-finite prices, and inconsistent price ranges.
- **PostgreSQL Loading:** Loads records into a temporary staging table, verifies record counts, and supports a transactional full refresh.
- **Safe Dry Run:** Tests the staging process without modifying the target table by default.
- **SQL Analytics:** Includes queries for commodity and market price analysis.
- **Automated Testing:** Includes transformation and validation tests.

## Technology Stack

- **Language:** Python
- **Database:** PostgreSQL
- **Data Processing:** Python CSV module
- **SQL:** PostgreSQL SQL
- **Database Driver:** Psycopg 3
- **Testing:** Python `unittest`
- **Version Control:** Git and GitHub
- **Environment:** Ubuntu on WSL

## Dataset

- **Dataset:** Current Daily Price of Various Commodities from Various Markets (Mandi)
- **Publisher:** Ministry of Agriculture and Farmers Welfare, Government of India
- **Portal:** [data.gov.in — Mandi Prices](https://www.data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi)
- **Format:** CSV
- **Raw file:** `data/raw/mandi_prices_raw.csv`
- **Processed file:** `data/processed/mandi_prices_transformed.csv`
- **Records:** 10,797

The project currently contains one distinct arrival date. Its results describe the available snapshot and should not be interpreted as long-term price trends. The exact provenance of the downloaded CSV has not yet been independently confirmed.

## Project Structure

```text
agricultural-market-intelligence/
├── data/
│   ├── raw/
│   ├── processed/
│   └── quality_reports/
├── sql/
│   └── market_analysis.sql
├── src/
│   ├── ingestion/
│   │   └── ingest_mandi_data.py
│   ├── transformation/
│   │   └── transform_mandi_data.py
│   ├── validation/
│   │   └── validate_mandi_data.py
│   └── loading/
│       └── load_mandi_data.py
├── tests/
│   ├── test_transform_mandi_data.py
│   └── test_validate_mandi_data.py
├── .gitignore
└── README.md
```

## Data Pipeline

1. **Ingest:** Check that the raw CSV exists and has the expected columns.
2. **Transform:** Standardize column names and dates, validate prices, and remove duplicate records.
3. **Validate:** Run data-quality checks and generate a quality report.
4. **Stage:** Load transformed records into a temporary PostgreSQL staging table.
5. **Verify:** Confirm that the staged record count matches the source record count.
6. **Load:** Optionally refresh the target table inside a transaction.
7. **Analyze:** Run SQL queries to examine commodity and market prices.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/dayyalaganesh/agricultural-market-intelligence.git
cd agricultural-market-intelligence
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install "psycopg[binary]"
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named `agricultural_market_intelligence` and a `mandi_prices` table with these columns:

| Column | PostgreSQL type |
|---|---|
| state | text |
| district | text |
| market | text |
| commodity | text |
| variety | text |
| grade | text |
| arrival_date | date |
| min_price | numeric(12,2) |
| max_price | numeric(12,2) |
| modal_price | numeric(12,2) |

The loader connects using the local PostgreSQL role `ganesh` by default. Configure an appropriate local role and database permissions for your environment. Do not commit passwords or other credentials.

### 5. Run the pipeline

Run these commands from the project root:

```bash
python src/ingestion/ingest_mandi_data.py
python src/transformation/transform_mandi_data.py
python src/validation/validate_mandi_data.py
python -m unittest discover -s tests -v
```

Ensure the transformed CSV exists before loading.

### 6. Test the PostgreSQL loader safely

The default mode is a dry run. It stages the records and verifies the count without refreshing the target table.

```bash
python src/loading/load_mandi_data.py
```

To apply a full refresh after reviewing the source and confirming that replacement is intended:

```bash
python src/loading/load_mandi_data.py --apply
```

**Warning:** `--apply` replaces all records in `public.mandi_prices` with the processed CSV contents. Run it only when a full refresh is intended. The transaction rolls back if an error occurs before commit.

### 7. Verify the loaded records

```bash
psql -d agricultural_market_intelligence \
  -c "SELECT COUNT(*) FROM mandi_prices;"
```

Expected count for the current dataset: `10797`.

### 8. Run SQL analytics

```bash
psql -d agricultural_market_intelligence \
  -f sql/market_analysis.sql
```

## Verified Results

- 10,797 source records read.
- 10,797 records loaded into the staging table during the successful dry run.
- Existing table remained unchanged during the dry run.
- 10,797 records present after the successful PostgreSQL refresh.
- Sample database records returned correctly typed dates and numeric prices.
- 17 transformation and validation tests had passed in the development environment.

These results reflect the current development run. Re-run the tests and checks when changing the code or dataset.

## Future Enhancements

- Schedule the pipeline with Apache Airflow.
- Add incremental ingestion and idempotent load strategies.
- Add database constraints and stronger automated integration tests.
- Integrate additional verified market datasets with multiple dates.
- Build visual analytics and explore cloud deployment.

## Disclaimer

This is an educational portfolio project. Price summaries describe the records available in the current dataset and do not establish long-term market trends.
