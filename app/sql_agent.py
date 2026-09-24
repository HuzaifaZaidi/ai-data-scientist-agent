from app.llm import ask_llm
from app.database import get_database_info


def generate_sql(user_question, analysis_plan=""):
    """Generate a PostgreSQL SELECT query from a user's question."""

    database_info = get_database_info()

    prompt = f"""
You are an AI data analyst working with a PostgreSQL e-commerce database.

Your job is to convert the user's business question into a SQL query.

DATABASE SCHEMA:
{database_info["schema"]}

DATABASE RELATIONSHIPS:
{database_info["relationships"]}

ANALYSIS PLAN:
{analysis_plan}

IMPORTANT RULES:
1. Generate PostgreSQL SQL.
2. Only generate SELECT queries.
3. Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, or TRUNCATE.
4. Use only tables and columns that exist in the schema.
5. Follow the analysis plan when deciding what data to retrieve.
6. Use JOINs when data from multiple tables is required.
7. Give every calculated or aggregated expression a clear descriptive alias using AS.
8. Examples:
   - SUM(amount) AS total_revenue
   - AVG(amount) AS average_revenue
   - SUM(profit) AS total_profit
   - SUM(amount) - SUM(other_amount) AS revenue_difference
   - calculated percentages AS percentage_contribution
9. Do not return unnamed expressions such as ?column?.
10. Return ONLY the SQL query.
11. Do not use markdown code fences.
12. Do not explain the query.

USER QUESTION:
{user_question}
"""

    sql_query = ask_llm(prompt)

    return sql_query.strip()