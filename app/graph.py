from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from app.sql_agent import generate_sql
from app.database import execute_query, get_database_info
from app.llm import ask_llm


class AgentState(TypedDict):
    user_question: str
    analysis_plan: str
    generated_sql: str
    database_result: list
    final_answer: str


def receive_question(state: AgentState):
    print("User question:", state["user_question"])

    return {}

def analysis_plan_node(state: AgentState):
    print("Creating analysis plan...")

    database_info = get_database_info()

    prompt = f"""
You are a senior data analyst working with a PostgreSQL e-commerce database.

USER QUESTION:
{state["user_question"]}

DATABASE SCHEMA:
{database_info["schema"]}

DATABASE RELATIONSHIPS:
{database_info["relationships"]}

Create a short analysis plan for answering the user's question.

IMPORTANT RULES:
1. Use ONLY tables and columns that actually exist in the database schema.
2. Do not invent column names.
3. Identify the main metric.
4. Identify relevant dimensions and filters.
5. If the question asks "why", identify useful comparisons or breakdowns.
6. Use the actual database terminology. For example, revenue is represented by the "amount" column.
7. Do not generate SQL yet.
8. Keep the plan concise.
"""

    plan = ask_llm(prompt)

    print("Analysis plan:", plan)

    return {
        "analysis_plan": plan.strip()
    }

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
builder.add_node("analysis_plan", analysis_plan_node)
builder.add_node("generate_sql", generate_sql_node)
builder.add_node("execute_sql", execute_sql_node)
builder.add_node("final_answer", final_answer_node)

# Connect nodes
builder.add_edge(START, "receive_question")
builder.add_edge("receive_question", "analysis_plan")
builder.add_edge("analysis_plan", "generate_sql")
builder.add_edge("generate_sql", "execute_sql")
builder.add_edge("execute_sql", "final_answer")
builder.add_edge("final_answer", END)

# Compile the graph
graph = builder.compile()