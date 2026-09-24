from app.analytics_tools import run_sql_query


result = run_sql_query.invoke(
    """
    SELECT
        SUM(od.amount) AS total_revenue
    FROM orders o
    JOIN order_details od
        ON o.order_id = od.order_id
    WHERE o.state = 'Maharashtra'
    """
)

print(result)