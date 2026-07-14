# Automated Data Pipeline for Financial Data
**Author:** Elton Silva

## Overview


## Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Power BI

## Skills Demonstrated

- Data Cleaning
- Data Validation
- Feature Engineering
- ETL Pipelines
- SQL Analytics
- Relational Databases
- Data Visualization
- Dashboard Development
- Business Insight Generation


## Commands:
To run the data engineering pipeline:
```bash
python src\pipeline.py
```

To create the database:
```bash
python sql\stocks_db.py
```

## File Structure
```text
- root:
    - dashboard:
    - data:
        - processed:
            - stock_prices_clean.csv
            - stock_prices_clean.parquet
            - validation_report.csv
        - raw:
            - raw_stock_prices.csv
    - notebooks:
        - 01_data_exploration.ipynb
        - 02_analysis_overview.ipynb
    - sql:
        - stocks_db.py
        - queries.sql
    - src:
        - __init__.py
        - .gitignore
        - data_cleaning.py
        - extract.py
        - feature_engineering.py
        - pipeline.py
        - validate.py
    - visuals:
        - dashboard_screenshots:
        - sql_outputs
    - __init__.py
    - README.md
    - requirements.txt
- lisbon_housing.db
```
