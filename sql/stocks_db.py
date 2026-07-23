from pathlib import Path
import pandas as pd
import sqlite3

ROOT_DIR = Path(__file__).resolve().parent.parent

csv_path = ROOT_DIR / "data" / "processed" / "stock_prices_clean.csv"
db_path = ROOT_DIR / "sql" / "stocks.db"

# Load cleaned CSV
df = pd.read_csv(csv_path)

# Create database
connection = sqlite3.connect(db_path)

# DF to table
df.to_sql(
    "stock_prices",
    connection,
    if_exists="replace",
    index=False
)

connection.close()