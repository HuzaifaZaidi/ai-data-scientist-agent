from app.database import execute_query


tests = [
    (
        "Valid SELECT",
        "SELECT category, SUM(amount) AS revenue "
        "FROM order_details "
        "GROUP BY category"
    ),
    (
        "DELETE attack",
        "DELETE FROM orders"
    ),
    (
        "Multiple statements",
        "SELECT * FROM orders; DELETE FROM orders"
    ),
    (
        "SQL comment",
        "SELECT * FROM orders -- delete something"
    ),
    (
        "DROP attack",
        "SELECT * FROM orders; DROP TABLE orders"
    ),
]


for name, query in tests:

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    try:
        columns, rows = execute_query(query)

        print("ALLOWED")
        print("Columns:", columns)
        print("Rows returned:", len(rows))

    except ValueError as e:

        print("BLOCKED")
        print("Reason:", e)