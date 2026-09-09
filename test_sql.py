from app.database import execute_query


# Test 1: Safe SELECT query
print("TEST 1: Safe SELECT")
print("=" * 50)

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

print(columns)

for row in rows:
    print(row)


# Test 2: DELETE should be blocked
print("\nTEST 2: DELETE query")
print("=" * 50)

try:
    execute_query("DELETE FROM orders;")
except ValueError as e:
    print("Blocked:", e)


# Test 3: Multiple statements should be blocked
print("\nTEST 3: Multiple SQL statements")
print("=" * 50)

try:
    execute_query(
        "SELECT * FROM orders; SELECT * FROM order_details;"
    )
except ValueError as e:
    print("Blocked:", e)