import os

import psycopg
from dotenv import load_dotenv


# Load variables from .env
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