import pandas as pd
import sqlite3

# Load cleaned CSV
df = pd.read_csv("root/data/processed/stock_prices_clean.csv", sep=",")

# Create database
conn = sqlite3.connect("financial_market.db")

# DF to table
df.to_sql(
    "stock_prices",
    conn,
    if_exists="replace",
    index=False
)

conn.close()