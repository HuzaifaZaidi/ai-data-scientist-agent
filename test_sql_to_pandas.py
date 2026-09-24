from app.database import execute_query
from app.analytics_tools import analyze_data, summarize_numeric_column


query = """
SELECT
    o.state,
    SUM(od.amount) AS revenue
FROM orders o
JOIN order_details od
    ON o.order_id = od.order_id
GROUP BY o.state
ORDER BY revenue DESC;
"""


columns, rows = execute_query(query)

print("DATABASE RESULT")
print("=" * 50)
print(rows)


df = analyze_data(columns, rows)

print("\nPANDAS DATAFRAME")
print("=" * 50)
print(df)


summary = summarize_numeric_column(
    df,
    "revenue"
)

print("\nREVENUE SUMMARY")
print("=" * 50)
print(summary)