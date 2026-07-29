from extract import directory_path, extract_and_save
from data_cleaning import data_cleaning
from feature_engineering import feature_engineering
from validate import build_validation_report
import pandas as pd
from pathlib import Path
import logging
from logger import configure_logging

TICKERS = ["NVDA", "GOOG", "AAPL", "MSFT", "AMZN", "TSM", "AVGO", "2222.SR", "005930.KS", "TSLA", "META", "MU", "000660.KS", "BRK-B", "LLY", "WMT", "JPM", "AMD", "V", "INTC"]

START_DATE = "2023-01-01"

RAW_DATA_PATH = directory_path("data/raw/raw_stock_prices.csv")

PROCESSED_DATA_PATH = directory_path("data/processed")

def load_data(input_path: Path) -> pd.DataFrame:
    """
    Load raw dataset from CSV file.

    Parameters
    path : str or Path

    Returns
    pd.DataFrame
    """
    return pd.read_csv(input_path)

def save_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save the processed dataset in CSV and Parquet formats.

    Parameters
    ----------
    df : pd.DataFrame
        Processed financial dataset.
    output_path : Path
        Destination directory.
    """
    
    csv_path = output_path / "stock_prices_clean.csv"
    parquet_path = output_path / "stock_prices_clean.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

def run_pipeline(input_path, output_path) -> None:
    """
    Run the financial-data transformation pipeline.

    Parameters
    ----------
    input_path : Path
        Path to the raw CSV dataset.
    output_path : Path
        Directory where processed files and the validation report are saved.
    """
    
    logging.info("Loading raw data from %s", input_path)
    df = load_data(input_path)
    
    logging.info("Cleaning data")
    df = data_cleaning(df)
    
    logging.info("Creating financial features")
    df = feature_engineering(df)
    
    logging.info("Running validation checks")
    validation_report = build_validation_report(df)
    
    critical = validation_report[
        (validation_report["status"] == "ERROR") &
        (validation_report["result"] > 0)
    ]

    if not critical.empty:
        logging.error("Critical validation failures detected")
        raise ValueError(f"Pipeline failed:\n{critical}")
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    logging.info("Saving processed datasets")
    save_data(df, output_path)
    
    validation_report.to_csv(
        output_path / "validation_report.csv",
        index=False
    )
    
    logging.info("Pipeline completed successfully")

def run_full_pipeline() -> None:
    """
    Run extraction, transformation, validation and output generation.
    """
    print("Downloading financial data...")

    extract_and_save(tickers=TICKERS, start=START_DATE, output_path=RAW_DATA_PATH,)

    print(f"Raw data saved to: {RAW_DATA_PATH}")

    run_pipeline(input_path=RAW_DATA_PATH, output_path=PROCESSED_DATA_PATH)

    print("Processed data and validation report saved to: "
        f"{PROCESSED_DATA_PATH}"
    )
    
if __name__ == "__main__":
    run_full_pipeline()