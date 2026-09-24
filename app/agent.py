from app.database import get_database_info
from app.graph import graph


def ask_data_agent(question: str):
    database_info = get_database_info()

    prompt = f"""
You are an AI data analyst working with an e-commerce PostgreSQL database.

DATABASE SCHEMA:
{database_info["schema"]}

DATABASE RELATIONSHIPS:
{database_info["relationships"]}

Your job is to answer the user's question using the available tools.

USER QUESTION:
{question}

Rules:
- Use only tables and columns present in the database schema.
- Use the database relationships when a JOIN is required.
- Do not invent table names or column names.
- Use the SQL tool whenever database information is required.
- Do not answer using general knowledge when the database can provide the answer.
- After receiving the tool result, provide a concise answer to the user.
"""

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    final_content = result["messages"][-1].content

    if isinstance(final_content, list):
        text_parts = []

        for item in final_content:
            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        return "\n".join(text_parts)

    return final_content