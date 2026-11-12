import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


# Load the orders CSV
orders = pd.read_csv(DATA_DIR / "List of Orders.csv")


print("Original rows:", len(orders))


# Remove rows where every column is empty
orders_clean = orders.dropna(how="all").copy()


print("Rows after cleaning:", len(orders_clean))


# Save cleaned file
output_file = DATA_DIR / "List of Orders_clean.csv"

orders_clean.to_csv(output_file, index=False)


print("Cleaned file created:")
print(output_file)