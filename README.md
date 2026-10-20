# Agricultural Market Intelligence Platform

## Overview
A data engineering and analytics project designed to integrate agricultural market price data, improve data quality, and support analysis of commodity prices across markets and dates.

## Objectives
- Ingest agricultural market data from CSV files and REST APIs.
- Standardize commodity, market, date, and price fields.
- Identify missing, duplicate, and inconsistent records.
- Store structured data in PostgreSQL.
- Organize raw and processed data for reproducible analysis.
- Analyze price trends across commodities and markets.

## Technology Stack
- **Language:** Python
- **Data Processing:** pandas
- **Database:** PostgreSQL
- **Data Sources:** CSV files, REST APIs
- **Cloud Storage:** AWS S3
- **Version Control:** Git and GitHub

## Project Status
**Current stage:** Initial project setup.

Planned components will be documented as they are implemented and tested.

## Project Structure
```text
agricultural-market-intelligence/
├── data/
│   ├── raw/
│   ├── processed/
│   └── quality_reports/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   └── validation/
├── sql/
├── tests/
├── logs/
├── .gitignore
└── README.md
```

## Data Sources

### Agricultural Market Prices

- **Dataset:** Current Daily Price of Various Commodities from Various Markets (Mandi)
- **Publisher:** Ministry of Agriculture and Farmers Welfare, Government of India
- **Data source:** AGMARKNET
- **Official portal:** https://www.data.gov.in/catalog/current-daily-price-various-commodities-various-markets-mandi
- **Local file:** `data/raw/mandi_prices_raw.csv`
- **Format:** CSV
- **Verification status:** Dataset structure and sample records match the official dataset description; the exact download provenance has not yet been independently confirmed.
## Future Enhancements
- Automated data quality tests
- Scheduled ingestion workflows
- Cloud-based raw and processed data storage
- Analytical SQL queries and price comparisons

## Disclaimer
This project is for learning and portfolio development. Results and capabilities will be updated to reflect the implemented and verified functionality.
