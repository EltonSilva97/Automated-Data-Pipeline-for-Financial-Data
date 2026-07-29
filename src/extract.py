from pathlib import Path
from collections.abc import Sequence
import pandas as pd
import yfinance as yf

def directory_path(path: str | Path) -> Path:
    """Resolve a path relative to the repository root."""
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir / Path(path)

def extract_data(tickers: Sequence[str], start: str) -> pd.DataFrame:
    """
    Download historical OHLCV data from Yahoo Finance.

    Parameters
    ----------
    tickers : Sequence[str]
        Yahoo Finance ticker symbols.
    start : str
        Starting date in YYYY-MM-DD format.

    Returns
    -------
    pd.DataFrame
        Raw Yahoo Finance output with ticker-grouped columns.
    """
    
    data = yf.download(tickers=list(tickers), start=start, group_by="ticker", auto_adjust=True, progress=False)
    
    if data.empty:
        raise ValueError("Yahoo Finance didn't returned any data. "
            "Check the ticker symbols, date and internet connection."
        )
    return data

def reshape_stock_data(data: pd.DataFrame, tickers: Sequence[str]) -> pd.DataFrame:
    """
    Convert Yahoo Finance's wide output to one row per ticker and date.

    Resulting columns:
    date, ticker, open, high, low, close, volume
    """
    frames: list[pd.DataFrame] = []
    required_columns = [
        "date",
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    price_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    for ticker in tickers:
        try:
            ticker_data = data[ticker].copy()
        except KeyError:
            print(f"Warning: {ticker} was not found in the downloaded dataset.")
            continue

        ticker_data = ticker_data.reset_index()
        ticker_data["ticker"] = ticker

        ticker_data.columns = [ str(column).strip().lower() for column in ticker_data.columns]
 

        missing_columns = [ column for column in required_columns if column not in ticker_data.columns]

        if missing_columns:
            raise ValueError(f"{ticker} is missing columns: {missing_columns}")
        
        empty_market_rows = ticker_data[price_columns].isna().all(axis=1).sum()

        if empty_market_rows > 0:
            print(f"{ticker}: removed {empty_market_rows} empty calendar-alignment rows."
        )

        # Remove rows generated only because Yahoo Finance aligns
        # tickers from different exchanges on a shared date index.
        ticker_data = ticker_data.dropna(
            subset=price_columns,
            how="all",
        )
        frames.append(ticker_data[required_columns])

    if not frames:
        raise ValueError("None of the requested tickers produced usable data.")

    return pd.concat(frames, ignore_index=True)
    
def to_csv(df: pd.DataFrame, path: Path) -> None:
    """Save the normalized raw dataset to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    return df.to_csv(path,  index=False)

def extract_and_save(tickers: Sequence[str], start: str, output_path: Path) -> pd.DataFrame:
    """
    Download, reshape and save the raw financial dataset.
    """
    
    downloaded_data = extract_data(tickers=tickers, start=start)

    raw_data = reshape_stock_data(data=downloaded_data, tickers=tickers)

    to_csv(raw_data, output_path)

    return raw_data