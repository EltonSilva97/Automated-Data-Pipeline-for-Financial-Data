import pandas as pd

from src.data_cleaning import data_cleaning


def test_data_cleaning_sorts_by_ticker_and_date():
    df = pd.DataFrame(
        {
            "ticker": ["MSFT", "AAPL", "AAPL"],
            "date": ["2025-01-02", "2025-01-03", "2025-01-01"],
        }
    )

    result = data_cleaning(df)

    expected = pd.DataFrame(
        {
            "ticker": ["AAPL", "AAPL", "MSFT"],
            "date": pd.to_datetime(
                ["2025-01-01", "2025-01-03", "2025-01-02"]
            ),
        }
    )

    pd.testing.assert_frame_equal(result, expected)