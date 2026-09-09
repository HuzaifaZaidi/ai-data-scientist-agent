from app.sql_agent import generate_sql
from app.database import execute_query
from app.llm import ask_llm


def answer_question(user_question):
    """Answer a business question using the database and LLM."""

    # Step 1: Generate SQL
    sql_query = generate_sql(user_question)

    # Step 2: Execute SQL safely
    columns, rows = execute_query(sql_query)

    # Step 3: Convert database result into readable text
    result_text = []

    for row in rows:
        result_text.append(
            dict(zip(columns, row))
        )

    # Step 4: Ask Gemini to explain the result
    prompt = f"""
You are a business data analyst.

Answer the user's question using ONLY the database result provided below.

USER QUESTION:
{user_question}

SQL QUERY:
{sql_query}

DATABASE RESULT:
{result_text}

Instructions:
1. Give the direct answer first.
2. Use the actual values from the database result.
3. Do not invent information.
4. Keep the answer concise and business-friendly.
5. If the result contains multiple rows, summarize the important findings.
"""

    final_answer = ask_llm(prompt)

    return {
        "question": user_question,
        "sql": sql_query,
        "result": result_text,
        "answer": final_answer.strip()
    }