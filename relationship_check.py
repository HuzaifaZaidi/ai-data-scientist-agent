import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


# --------------------------------------------------
# 1. Load datasets
# --------------------------------------------------

orders = pd.read_csv(DATA_DIR / "List of Orders.csv")
details = pd.read_csv(DATA_DIR / "Order Details.csv")
targets = pd.read_csv(DATA_DIR / "Sales target.csv")


# --------------------------------------------------
# 2. Remove completely blank rows from Orders
# --------------------------------------------------

orders_clean = orders.dropna(how="all").copy()


print("=" * 60)
print("ORDERS")
print("=" * 60)

print(f"Original rows: {len(orders)}")
print(f"Rows after removing completely blank rows: {len(orders_clean)}")

print(f"Unique Order IDs: {orders_clean['Order ID'].nunique()}")

print(f"Duplicate Order IDs: {orders_clean['Order ID'].duplicated().sum()}")


# --------------------------------------------------
# 3. Order Details
# --------------------------------------------------

print("\n" + "=" * 60)
print("ORDER DETAILS")
print("=" * 60)

print(f"Total detail rows: {len(details)}")
print(f"Unique Order IDs: {details['Order ID'].nunique()}")

print(
    f"Average detail rows per order: "
    f"{len(details) / details['Order ID'].nunique():.2f}"
)


# --------------------------------------------------
# 4. Check relationship between Orders and Details
# --------------------------------------------------

order_ids = set(orders_clean["Order ID"])
detail_order_ids = set(details["Order ID"])


details_without_order = detail_order_ids - order_ids
orders_without_details = order_ids - detail_order_ids


print("\n" + "=" * 60)
print("ORDER ID RELATIONSHIP")
print("=" * 60)

print(
    f"Order IDs in Order Details but NOT in Orders: "
    f"{len(details_without_order)}"
)

print(
    f"Order IDs in Orders but NOT in Order Details: "
    f"{len(orders_without_details)}"
)


# --------------------------------------------------
# 5. Check Sales Targets
# --------------------------------------------------

print("\n" + "=" * 60)
print("SALES TARGETS")
print("=" * 60)

print(f"Target rows: {len(targets)}")

print(
    f"Unique Month + Category combinations: "
    f"{targets[['Month of Order Date', 'Category']].drop_duplicates().shape[0]}"
)

print(
    f"Duplicate Month + Category combinations: "
    f"{targets.duplicated(subset=['Month of Order Date', 'Category']).sum()}"
)


# --------------------------------------------------
# 6. Categories
# --------------------------------------------------

print("\n" + "=" * 60)
print("CATEGORIES")
print("=" * 60)

print("\nCategories in Order Details:")

for category in sorted(details["Category"].unique()):
    print(f"- {category}")


print("\nSub-Categories:")

for subcategory in sorted(details["Sub-Category"].unique()):
    print(f"- {subcategory}")


# --------------------------------------------------
# 7. Date information
# --------------------------------------------------

orders_clean["Order Date"] = pd.to_datetime(
    orders_clean["Order Date"],
    dayfirst=True
)


print("\n" + "=" * 60)
print("DATE RANGE")
print("=" * 60)

print(f"Minimum order date: {orders_clean['Order Date'].min()}")
print(f"Maximum order date: {orders_clean['Order Date'].max()}")