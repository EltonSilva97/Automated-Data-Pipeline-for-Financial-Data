import pandas as pd

SOURCE_COLUMNS = [
    "date",
    "ticker",
    "open",
    "high",
    "low",
    "close",
    "volume",
]

ROLLING_FEATURE_COLUMNS = [
    "ma_30",
    "volatility_30d",
    "bb_middle",
    "bb_upper",
    "bb_lower",
    "ema_60",
    "volume_ratio_30d",
]

def validate_duplicates(df) -> int:
    """Count duplicated ticker-date records."""
    return int(df.duplicated(subset=["date", "ticker"]).sum())

def validate_negative_prices(df)  -> pd.DataFrame:
    """Return rows containing zero or negative OHLC prices."""
    price_cols = ["open", "high", "low", "close"]

    negative_prices = df[
        (df[price_cols] <= 0).any(axis=1)
    ]

    return negative_prices

def validate_negative_volumes(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows containing negative trading volume."""
    return df[df["volume"] < 0]

# Minor inconsistencies may arise from adjusted prices or floating-point precision.
# These are reported but do not stop the pipeline.
def validate_ohlc(    df: pd.DataFrame, tolerance: float = 1e-6,) -> pd.DataFrame:
    invalid_ohlc = df[
        (df["high"] + tolerance < df["open"]) |
        (df["high"] + tolerance < df["close"]) |
        (df["high"] + tolerance < df["low"]) |
        (df["low"] - tolerance > df["open"]) |
        (df["low"] - tolerance > df["close"])
    ]

    return invalid_ohlc

def validate_missing_values(df: pd.DataFrame) -> int:
    """
    Count missing values in the original source columns.

    Missing source values are unexpected and should stop the pipeline.
    """
    missing_columns = [ column for column in SOURCE_COLUMNS if column not in df.columns]

    if missing_columns:
        raise KeyError(f"Required source columns are missing: {missing_columns}")

    return int(df[SOURCE_COLUMNS].isna().sum().sum())

def validate_feature_missing_values(df: pd.DataFrame) -> int:
    """
    Count missing values in rolling engineered features.

    These values normally occur during each ticker's rolling-window
    warm-up period and are reported without stopping the pipeline.
    """
    available_feature_columns = [ column for column in ROLLING_FEATURE_COLUMNS if column in df.columns]

    if not available_feature_columns:
        return 0

    return int(df[available_feature_columns].isna().sum().sum())

# Pipeline policy:
# ERROR -> stop execution
# WARN  -> report only
# PASS  -> no issues detected
def get_status(check: str, result: int) -> str:
    """Assign a pipeline status according to validation severity."""
    
    if check in ["duplicates", "negative_prices", "negative_volumes",  "source_missing_values"]:
        return "ERROR" if result > 0 else "PASS"

    if check in ["invalid_ohlc", "feature_warmup_missing_values"]:
        return "WARN" if result > 0 else "PASS"
    
    raise ValueError(f"Unknown validation check: {check}")

def build_validation_report(df: pd.DataFrame) -> pd.DataFrame:
    """Run all checks and return the validation report."""
    results = {
        "duplicates": validate_duplicates(df),
        "invalid_ohlc": len(validate_ohlc(df)),
        "negative_prices": len(validate_negative_prices(df)),
        "negative_volumes": len(validate_negative_volumes(df)),
        "source_missing_values": validate_missing_values(df),
        "feature_warmup_missing_values": (validate_feature_missing_values(df)),
    }

    validation_report = pd.DataFrame(
        {
            "check": list(results.keys()),
            "result": list(results.values()),
        }
    )

    validation_report["status"] = validation_report.apply(
        lambda row: get_status(row["check"], int(row["result"]),),axis=1,
    )
    
    return validation_report