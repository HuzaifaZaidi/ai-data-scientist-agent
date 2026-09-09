from app.database import execute_query


# Test 1: Safe SELECT query
query = """
SELECT
    category,
    SUM(amount) AS revenue,
    SUM(profit) AS profit
FROM order_details
GROUP BY category
ORDER BY revenue DESC;
"""

columns, rows = execute_query(query)

print("Safe query result:")
print(columns)

for row in rows:
    print(row)


# Test 2: Dangerous query
print("\nTesting unsafe query...")

try:
    execute_query("DELETE FROM orders;")
except ValueError as e:
    print("Blocked:", e)