from app.llm import llm
from app.analytics_tools import run_sql_query
from app.database import get_database_info


database_info = get_database_info()

tools = [run_sql_query]

llm_with_tools = llm.bind_tools(tools)


prompt = f"""
You are an e-commerce data analyst working with a PostgreSQL database.

The database schema and relationships are provided below.

DATABASE SCHEMA:
{database_info["schema"]}

DATABASE RELATIONSHIPS:
{database_info["relationships"]}

Your job is to answer the user's question by using the SQL tool.

USER QUESTION:
What is the total revenue from Maharashtra?

Rules:
1. Use only tables and columns present in the database schema.
2. Use the relationships provided when a JOIN is required.
3. Do not invent column names.
4. Determine the appropriate metric from the available schema.
5. Use the SQL tool to retrieve the answer.
6. Do not answer from your general knowledge.
"""


response = llm_with_tools.invoke(prompt)


print("LLM response:")
print(response)

print("\nTool calls:")
print(response.tool_calls)