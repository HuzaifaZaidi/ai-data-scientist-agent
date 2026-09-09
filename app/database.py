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

def execute_query(query):
    """Execute a safe, read-only SQL query and return the results."""

    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    # Remove trailing semicolon for validation
    cleaned_query = query.rstrip(";").strip()

    # Only allow SELECT statements
    if not cleaned_query.upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    # Prevent multiple SQL statements
    if ";" in cleaned_query:
        raise ValueError("Multiple SQL statements are not allowed.")

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(cleaned_query)

            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()

            return columns, rows

    finally:
        connection.close()
def get_database_schema():
    """Return the tables and columns available to the analytics agent."""

    query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        AND table_name IN (
            'orders',
            'order_details',
            'sales_targets'
        )
        ORDER BY table_name, ordinal_position;
    """

    columns, rows = execute_query(query)

    schema = {}

    for table_name, column_name, data_type in rows:
        if table_name not in schema:
            schema[table_name] = []

        schema[table_name].append({
            "column": column_name,
            "data_type": data_type
        })

    return schema


def get_database_relationships():
    """Return the relationships between database tables."""

    query = """
        SELECT
            child_table.relname AS child_table,
            child_column.attname AS child_column,
            parent_table.relname AS parent_table,
            parent_column.attname AS parent_column
        FROM pg_constraint constraint_info

        JOIN pg_class child_table
            ON child_table.oid = constraint_info.conrelid

        JOIN pg_class parent_table
            ON parent_table.oid = constraint_info.confrelid

        JOIN pg_attribute child_column
            ON child_column.attrelid = constraint_info.conrelid
            AND child_column.attnum = constraint_info.conkey[1]

        JOIN pg_attribute parent_column
            ON parent_column.attrelid = constraint_info.confrelid
            AND parent_column.attnum = constraint_info.confkey[1]

        WHERE constraint_info.contype = 'f'
        AND child_table.relnamespace = (
            SELECT oid
            FROM pg_namespace
            WHERE nspname = 'public'
        );
    """

    columns, rows = execute_query(query)

    relationships = []

    for child_table, child_column, parent_table, parent_column in rows:
        relationships.append({
            "child_table": child_table,
            "child_column": child_column,
            "parent_table": parent_table,
            "parent_column": parent_column
        })

    return relationships

def get_database_info():
    """Return database schema and table relationships."""

    schema = get_database_schema()
    relationships = get_database_relationships()

    return {
        "schema": schema,
        "relationships": relationships
    }