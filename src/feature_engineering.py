import pandas as pd

# Feature engineering includes a mix of indicators that analyze the the evolution of price:
#    Trend indicators (MA, EMA)
#    Risk indicators (volatility, drawdown)
#    Performance indicators (daily and cumulative return)
#    Price behaviour (high-low spread)
#    Technical indicators (Bollinger Bands)

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Daily return from open to close
    df["daily_return"] = (df["close"] - df["open"]) / df["open"]
    
    df["ma_30"] = (
        df.groupby("ticker")["close"].transform(lambda x: x.rolling(30).mean())
    )
    
    df["volatility_30d"] = (
        df.groupby("ticker")["daily_return"].transform(lambda x: x.rolling(30).std())
    )
    
    # Define parameters
    window = 30 # Window for the moving average
    std_multiplier = 2 # Number of standard deviations to use

    # Calculate the rolling mean and standard deviation
    rolling_mean = (
        df.groupby("ticker")["close"].transform(lambda x: x.rolling(window).mean())
    )

    rolling_std = (
        df.groupby("ticker")["close"].transform(lambda x: x.rolling(window).std())
    )

    df["bb_middle"] = rolling_mean
    df["bb_upper"] = rolling_mean + std_multiplier * rolling_std
    df["bb_lower"] = rolling_mean - std_multiplier * rolling_std

    # Cumulative return per ticker
    df["cumulative_return"] = (
        (1 + df["daily_return"]).groupby(df["ticker"]).cumprod() - 1
    )

    # Intraday range percentage
    df["high_low_spread_pct"] = (
        (df["high"] - df["low"]) / df["high"] * 100
    )

    # Drawdown per ticker
    running_max = (df.groupby("ticker")["close"].cummax())

    df["drawdown"] = (
        (df["close"] - running_max) / running_max
    )

    # EMA 60 per ticker
    df["ema_60"] = (
        df.groupby("ticker")["close"].transform(lambda x: x.ewm(span=60, adjust=False, min_periods=30).mean())
    )
    
    df["volume_ratio_30d"] = (
        df["volume"] / df.groupby("ticker")["volume"].transform(lambda x: x.rolling(30).mean())
    )

    return df