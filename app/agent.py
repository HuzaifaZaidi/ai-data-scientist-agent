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
- Use the Python analysis tool when calculations or statistical analysis are required.
- Use the chart tool when the user asks for a chart or when a visualization would clearly help.
- Do not answer using general knowledge when the database can provide the answer.
- After receiving the tool results, provide a concise answer to the user.
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

        final_content = "\n".join(text_parts)

    chart_path = None

    for message in result["messages"]:
        if getattr(message, "type", None) != "tool":
            continue

        content = message.content

        if isinstance(content, str) and content.startswith("CHART_CREATED:"):
            chart_path = content.replace(
                "CHART_CREATED:",
                "",
                1
            ).strip()

    return {
        "answer": final_content,
        "chart": chart_path
    }