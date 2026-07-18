# Automated Data Pipeline for Financial Data
**Author:** Elton Silva

## Overview

## Structure
```bash
    extract
    ↓
    clean
    ↓
feature engineer
    ↓
validate
    ↓
processed dataset
    ↓
    SQLite
    ↓
    SQL
    ↓
analysis notebook
```

## Technology Stack

- Python
- Pandas
- NumPy
- SQLite
- SQL

## Skills Demonstrated

- Data Cleaning
- Data Validation
- Feature Engineering
- ETL Pipelines
- SQL Analytics
- Relational Databases
- Data Visualization
- Business Insight Generation

## Feature engineering:
Trend indicators:
- 30-day moving average (Average closing price of an asset over the last 30 days.)
- 60-day EMA (Average price of an asset over the past 60 trading days giving more weight to recent price data, to make it react faster to current market changes than a simple moving average.)

Risk indicators:
- 30-day rolling volatility (Measure of how much an asset's price bounces up and down over a moving 30-day window.)
- Drawdown (Percentage decline from the highest closing price reached so far, used to quantify downside risk.)
  
Performance indicators:
- Daily intraday return (Percentage change between the opening and closing price during a single trading day.)
- Cumulative return (Compounded percentage return accumulated over the observation period.)

Price-behaviour indicators:
- High–low spread (Percentage intraday price range between the daily high and daily low, used to measure daily price movement.)

Technical indicators:
- Bollinger Bands (Percentage intraday price range between the daily high and daily low, used to measure daily price movement.)

Trading-activity indicators:
- 30-day volume ratio (Compares the current trading volume with its 30-day average to identify unusually high or low trading activity.)

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
        - stocks.db
    - src:
        - __init__.py
        - data_cleaning.py
        - extract.py
        - feature_engineering.py
        - pipeline.py
        - validate.py
    - __init__.py
    - README.md
    - requirements.txt
    - .gitignore
```
