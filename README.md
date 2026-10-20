# Agricultural Market Intelligence Platform

A Python and PostgreSQL data engineering project that ingests, transforms, validates, and analyzes agricultural market price data from Indian mandis.

## Project Overview

This project demonstrates an end-to-end data processing workflow for agricultural commodity prices. It converts raw CSV data into a standardized format, validates data quality, stores structured records in PostgreSQL, and enables SQL-based market analysis.

## Key Features

- **Data Ingestion:** Checks input file availability and validates the expected CSV schema.
- **Data Transformation:** Standardizes column names, normalizes arrival dates, validates prices, and removes duplicate rows.
- **Data Validation:** Checks for missing values, duplicate records, invalid dates, negative prices, and price-range inconsistencies.
- **Database Storage:** Loads transformed agricultural market data into PostgreSQL.
- **SQL Analytics:** Analyzes average modal prices by commodity and market.
- **Unit Testing:** Includes automated tests for transformation functions.

## Technology Stack

- **Programming:** Python
- **Data Processing:** CSV-based ingestion and transformation
- **Database:** PostgreSQL
- **Query Language:** SQL
- **Testing:** Python `unittest`
- **Version Control:** Git and GitHub
- **Environment:** Ubuntu on WSL

## Dataset

- **Dataset:** Current Daily Price of Various Commodities from Various Markets (Mandi)
- **Publisher:** Ministry of Agriculture and Farmers Welfare, Government of India
- **Portal:** [data.gov.in — Mandi Prices](https://www.data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi)
- **Format:** CSV
- **Raw file:** `data/raw/mandi_prices_raw.csv`
- **Records processed:** 10,797

The dataset structure and sample records match the official dataset description. The exact download provenance has not yet been independently confirmed.

## Project Structure

```text
agricultural-market-intelligence/
├── data/
│   ├── raw/
│   ├── processed/
│   └── quality_reports/
├── logs/
├── sql/
│   └── market_analysis.sql
├── src/
│   ├── ingestion/
│   │   └── ingest_mandi_data.py
│   ├── transformation/
│   │   └── transform_mandi_data.py
│   └── validation/
│       └── validate_mandi_data.py
├── tests/
│   └── test_transform_mandi_data.py
├── .gitignore
└── README.md
```

## Data Pipeline

1. **Ingest:** Verify the input CSV and its expected schema.
2. **Transform:** Standardize columns and dates, validate prices, and remove duplicate rows.
3. **Validate:** Run data-quality checks on the dataset.
4. **Load:** Import transformed records into PostgreSQL.
5. **Analyze:** Execute SQL queries to summarize commodity and market prices.

## PostgreSQL Setup

Create a database named `agricultural_market_intelligence` and a table named `mandi_prices` with columns matching the transformed CSV schema.

After creating the table, load the processed CSV from the project root:

```bash
sudo -u postgres psql -d agricultural_market_intelligence \
  -c "\copy mandi_prices FROM 'data/processed/mandi_prices_transformed.csv' WITH (FORMAT csv, HEADER true)"
```

Verify the imported record count:

```bash
sudo -u postgres psql -d agricultural_market_intelligence \
  -c "SELECT COUNT(*) FROM mandi_prices;"
```

Expected record count for the current dataset: `10797`.

## Run the Project

Execute the scripts from the project root:

```bash
python3 src/ingestion/ingest_mandi_data.py
python3 src/transformation/transform_mandi_data.py
python3 src/validation/validate_mandi_data.py
python3 -m unittest discover -s tests -v
```

Run the SQL analytics after PostgreSQL is configured and the data has been loaded:

```bash
sudo -u postgres psql -d agricultural_market_intelligence \
  -f sql/market_analysis.sql
```

## Current Implementation Status

- CSV ingestion and schema validation implemented.
- Data transformation implemented.
- Six transformation unit tests passing.
- Data-quality validation implemented.
- PostgreSQL table created and 10,797 records imported.
- SQL analytics queries saved in `sql/market_analysis.sql`.
- Git version history maintained in GitHub.

## Future Enhancements

- Automate ingestion and transformation with Apache Airflow.
- Add incremental ingestion and scheduled pipeline execution.
- Integrate additional verified agricultural market datasets.
- Develop richer analytical reports and visualizations.
- Explore cloud storage and deployment.

## Disclaimer

This project is for educational and portfolio purposes. Price summaries describe the available dataset and should not be interpreted as long-term market trends. The current dataset contains one distinct arrival date.
