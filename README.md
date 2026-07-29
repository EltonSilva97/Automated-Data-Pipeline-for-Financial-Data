# Automated Data Pipeline for Financial Data
**Author:** Elton Silva

## Overview
This project demonstrates the design and implementation of an end-to-end data engineering pipeline for financial market data. It automates data extraction, cleaning, feature engineering, validation, storage, and exploratory analysis using Python, SQLite, and SQL.

## Objectives
- Build an automated ETL pipeline
- Apply financial feature engineering
- Validate data quality
- Store processed data efficiently
- Perform SQL-based analysis
- Produce exploratory visualizations

## Highlights
- Automated ETL workflow
- Modular Python architecture
- Data validation framework
- Financial feature engineering
- SQLite integration
- SQL analytics
- Automated testing with pytest
- GitHub Actions CI

## Continuous Integration
GitHub Actions automatically runs the project's test suite whenever new commits are pushed.

## Structure
```bash
Yahoo Finance
      │
      ▼
Data Extraction
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Data Validation
      │
      ▼
CSV / Parquet
      │
      ├──► SQLite Database
      │          │
      │          ▼
      │      SQL Analysis
      │
      ▼
Jupyter Notebook
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
### Trend indicators:
- 30-day moving average (Average closing price of an asset over the last 30 days.)
- 60-day EMA (Average price of an asset over the past 60 trading days giving more weight to recent price data, to make it react faster to current market changes than a simple moving average.)

### Risk indicators:
- 30-day rolling volatility (Measure of how much an asset's price bounces up and down over a moving 30-day window.)
- Drawdown (Percentage decline from the highest closing price reached so far, used to quantify downside risk.)
  
### Performance indicators:
- Daily intraday return (Compounded sequence of daily open-to-close returns over the observation period.)
- Cumulative return (Compounded percentage return accumulated over the observation period.)

### Price-behaviour indicators:
- High–low spread (Percentage intraday price range between the daily high and daily low, used to measure daily price movement.)

### Technical indicators:
- Bollinger Bands (Upper and lower volatility bands placed around a 30-day moving average using two rolling standard deviations.)

### Trading-activity indicators:
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

Run all tests:
```bash
python -m pytest
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
    - README.md
    - requirements.txt
    - .gitignore
```