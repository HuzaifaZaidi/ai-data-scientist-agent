from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from app.sql_agent import generate_sql
from app.database import execute_query
from app.llm import ask_llm


class AgentState(TypedDict):
    user_question: str
    generated_sql: str
    database_result: list
    final_answer: str


def receive_question(state: AgentState):
    print("User question:", state["user_question"])

    return {}


def generate_sql_node(state: AgentState):
    print("Generating SQL...")

    sql = generate_sql(state["user_question"])

    print("Generated SQL:", sql)

    return {
        "generated_sql": sql
    }


def execute_sql_node(state: AgentState):
    print("Executing SQL...")

    columns, rows = execute_query(
        state["generated_sql"]
    )

    result = []

    for row in rows:
        result.append(
            dict(zip(columns, row))
        )

    print("Database result:", result)

    return {
        "database_result": result
    }


def final_answer_node(state: AgentState):
    print("Generating final answer...")

    prompt = f"""
You are a business data analyst.

Answer the user's question using ONLY the database result provided below.

USER QUESTION:
{state["user_question"]}

SQL QUERY:
{state["generated_sql"]}

DATABASE RESULT:
{state["database_result"]}

Instructions:
1. Give the direct answer first.
2. Use the actual values from the database result.
3. Do not invent information.
4. Keep the answer concise and business-friendly.
"""

    answer = ask_llm(prompt)

    print("Final answer:", answer)

    return {
        "final_answer": answer.strip()
    }


# Create the graph
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("receive_question", receive_question)
builder.add_node("generate_sql", generate_sql_node)
builder.add_node("execute_sql", execute_sql_node)
builder.add_node("final_answer", final_answer_node)

# Connect nodes
builder.add_edge(START, "receive_question")
builder.add_edge("receive_question", "generate_sql")
builder.add_edge("generate_sql", "execute_sql")
builder.add_edge("execute_sql", "final_answer")
builder.add_edge("final_answer", END)

# Compile the graph
graph = builder.compile()