import pandas as pd

def validate_duplicates(df):
    return df.duplicated(subset=["date","ticker"]).sum()

def validate_negative_prices(df):
    price_cols = ["open", "high", "low", "close"]

    negative_prices = df[
        (df[price_cols] <= 0).any(axis=1)
    ]

    return negative_prices

def validate_negative_volumes(df):
    return df[df["volume"] < 0]

# Minor inconsistencies may arise from adjusted prices or floating-point precision.
# These are reported but do not stop the pipeline.
def validate_ohlc(df, tolerance=1e-6):
    invalid_ohlc = df[
        (df["high"] + tolerance < df["open"]) |
        (df["high"] + tolerance < df["close"]) |
        (df["high"] + tolerance < df["low"]) |
        (df["low"] - tolerance > df["open"]) |
        (df["low"] - tolerance > df["close"])
    ]

    return invalid_ohlc

def validate_missing_values(df):
    return df.isna().sum()

# Pipeline policy:
# ERROR -> stop execution
# WARN  -> report only
# PASS  -> no issues detected
def get_status(check, result):
    if check in ["duplicates", "negative_prices", "negative_volumes"]:
        return "ERROR" if result > 0 else "PASS"

    if check in ["invalid_ohlc", "missing_values"]:
        return "WARN" if result > 0 else "PASS"

def build_validation_report(df: pd.DataFrame) -> pd.DataFrame:
    duplicates = validate_duplicates(df)
    negative_prices = validate_negative_prices(df)
    negative_volumes = validate_negative_volumes(df)
    invalid_ohlc = validate_ohlc(df)
    missing_values = validate_missing_values(df)
    total_missing_values = missing_values.sum()
    
    validation_report = pd.DataFrame({
        "check": [
            "duplicates",
            "invalid_ohlc",
            "negative_prices",
            "negative_volumes",
            "missing_values"
        ],
        "result": [
            duplicates,
            len(invalid_ohlc),
            len(negative_prices),
            len(negative_volumes),
            total_missing_values,
        ]
    })
    
    validation_report["status"] = validation_report.apply(
        lambda row: get_status(row["check"], row["result"]),
        axis=1
    )
    
    return validation_report