import yfinance as yf
from pathlib import Path

def extract_data(tickers, start):
    data = yf.download(tickers=tickers, start=start, group_by="ticker", auto_adjust=True)
    return data

def to_csv(df, path):
    return df.to_csv(path,  index=False)

def directory_path(path):
    BASE_DIR = Path(__file__).resolve().parent.parent
    return BASE_DIR / Path(path)