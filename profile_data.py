import pandas as pd
from pathlib import Path


# Location of our data files
DATA_DIR = Path("data")


# List of datasets we want to inspect
files = [
    "List of Orders.csv",
    "Order Details.csv",
    "Sales target.csv"
]


for file in files:
    print("\n" + "=" * 60)
    print(f"DATASET: {file}")
    print("=" * 60)

    file_path = DATA_DIR / file

    # Read CSV
    df = pd.read_csv(file_path)

    # Basic information
    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nData types:")
    print(df.dtypes)