from langchain_core.messages import HumanMessage

from app.graph import graph
from app.database import get_database_info


database_info = get_database_info()

question = "What is the total revenue from Maharashtra?"


message = HumanMessage(
    content=f"""
You are an e-commerce data analyst.

DATABASE SCHEMA:
{database_info["schema"]}

DATABASE RELATIONSHIPS:
{database_info["relationships"]}

Use the SQL tool to answer the user's question.

USER QUESTION:
{question}

Rules:
- Use only tables and columns from the database schema.
- Use database relationships when a JOIN is required.
- Do not invent columns.
- Use the SQL tool rather than answering from general knowledge.
"""
)


result = graph.invoke(
    {
        "messages": [message]
    }
)


print("\nFinal messages:")

for message in result["messages"]:
    print("\n---")
    print(message)