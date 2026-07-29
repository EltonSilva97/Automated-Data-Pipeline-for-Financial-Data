import pandas as pd

from src.validate import (
    validate_duplicates,
    validate_negative_prices,
    validate_negative_volumes,
)


def sample_data():
    return pd.DataFrame(
        {
            "date": ["2025-01-01", "2025-01-01"],
            "ticker": ["AAPL", "AAPL"],
            "open": [100.0, -1.0],
            "high": [105.0, 3.0],
            "low": [99.0, 1.0],
            "close": [104.0, 2.0],
            "volume": [1000, -10],
        }
    )


def test_duplicate_detection():
    assert validate_duplicates(sample_data()) == 1


def test_negative_price_detection():
    assert len(validate_negative_prices(sample_data())) == 1


def test_negative_volume_detection():
    assert len(validate_negative_volumes(sample_data())) == 1