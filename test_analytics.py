from app.database import get_revenue_by_state


results = get_revenue_by_state()


print("Revenue and Profit by State")
print("=" * 50)


for state, revenue, profit in results:
    print(
        f"{state:<25} "
        f"Revenue: ₹{revenue:>10,.2f}   "
        f"Profit: ₹{profit:>10,.2f}"
    )