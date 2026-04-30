import pandas as pd
from sqlalchemy import create_engine
import os

# Read your file
df = pd.read_csv(r"C:\Users\DELL\Desktop\retail business dashboard\Superstore.csv", encoding="latin-1")

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()

# Fix dates
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["ship_date"]  = pd.to_datetime(df["ship_date"],  errors="coerce")

# Save into SQLite database
os.makedirs("data", exist_ok=True)
engine = create_engine("sqlite:///data/sales.db")
df.to_sql("orders", engine, if_exists="replace", index=False)

print(f"Success! {len(df)} rows loaded into sales.db")
print("Columns:", list(df.columns))