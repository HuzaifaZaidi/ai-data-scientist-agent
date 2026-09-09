import os

import psycopg
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    """Create and return a PostgreSQL database connection."""

    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    return connection


def get_order_count():
    """Return the total number of orders."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM orders;"
            )

            result = cursor.fetchone()

            return result[0]

    finally:
        connection.close()


def get_revenue_by_state():
    """Return revenue and profit for each state."""

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT
                    o.state,
                    SUM(od.amount) AS revenue,
                    SUM(od.profit) AS profit
                FROM orders o
                JOIN order_details od
                    ON o.order_id = od.order_id
                GROUP BY o.state
                ORDER BY revenue DESC;
            """

            cursor.execute(query)

            results = cursor.fetchall()

            return results

    finally:
        connection.close()