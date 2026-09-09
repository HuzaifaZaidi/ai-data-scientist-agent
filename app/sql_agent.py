from app.llm import ask_llm
from app.database import get_database_info


def generate_sql(user_question):
    """Generate a PostgreSQL SELECT query from a user's question."""

    database_info = get_database_info()

    prompt = f"""
You are an AI data analyst working with a PostgreSQL e-commerce database.

Your job is to convert the user's business question into a SQL query.

DATABASE SCHEMA:
{database_info["schema"]}

DATABASE RELATIONSHIPS:
{database_info["relationships"]}

IMPORTANT RULES:
1. Generate PostgreSQL SQL.
2. Only generate SELECT queries.
3. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE.
4. Use only tables and columns that exist in the schema.
5. Use JOINs when data from multiple tables is required.
6. Return ONLY the SQL query.
7. Do not use markdown code fences.
8. Do not explain the query.

USER QUESTION:
{user_question}
"""

    sql_query = ask_llm(prompt)

    return sql_query.strip()