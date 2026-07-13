from extract import directory_path
from data_cleaning import data_cleaning
from feature_engineering import feature_engineering
from validate import build_validation_report
import pandas as pd
from pathlib import Path

stocks_price_path = directory_path("data/raw/raw_stock_prices.csv")

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
    Save dataset in CSV and Parquet formats.

    Parameters
    ----------
    path : str or Path

    Returns
    -------
    Path after all transformations
    """
    
    csv_path = output_path / "stock_prices_clean.csv"
    parquet_path = output_path / "stock_prices_clean.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

def run_pipeline(input_path, output_path) -> None:
    """
    Load dataset from Path.

    Parameters
    ----------
    input path : str or Path
    output path : str or Path

    Returns
    -------
    Output Path after cleaning, feature engineering and validation
    """
    
    df = load_data(input_path)
    df = data_cleaning(df)
    df = feature_engineering(df)
    validation_report = build_validation_report(df)
    
    critical = validation_report[
        (validation_report["status"] == "ERROR") &
        (validation_report["result"] > 0)
    ]

    if not critical.empty:
        raise ValueError(f"Pipeline failed:\n{critical}")
    
    output_path.mkdir(parents=True, exist_ok=True)
    save_data(df, output_path)
    validation_report.to_csv(
        output_path / "validation_report.csv",
        index=False
    )
    
if __name__ == "__main__":

    output_path = directory_path("data/processed")

    run_pipeline(
        stocks_price_path,
        output_path
    )