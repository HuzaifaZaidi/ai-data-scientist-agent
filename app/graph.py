from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from app.sql_agent import generate_sql
from app.database import execute_query, get_database_info
from app.llm import ask_llm
from app.analytics_tools import analyze_data, summarize_numeric_column


class AgentState(TypedDict):
    user_question: str
    analysis_plan: str
    generated_sql: str
    database_result: list
    analysis_result: dict
    sql_error: str
    retry_count: int
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

    sql = generate_sql(
        state["user_question"],
        state["analysis_plan"]
    )

    print("Generated SQL:", sql)

    return {
    "generated_sql": sql,
    "sql_error": ""
}


def execute_sql_node(state: AgentState):
    print("Executing SQL...")

    try:
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
            "database_result": result,
            "sql_error": ""
        }

    except Exception as e:

        error_message = str(e)

        print("SQL execution error:", error_message)

        return {
            "database_result": [],
            "sql_error": error_message
        }
    
def repair_sql_node(state: AgentState):
    print("Repairing SQL...")

    database_info = get_database_info()

    prompt = f"""
You are a PostgreSQL SQL expert.

The user asked:

{state["user_question"]}

The analysis plan is:

{state["analysis_plan"]}

DATABASE SCHEMA:
{database_info["schema"]}

DATABASE RELATIONSHIPS:
{database_info["relationships"]}

The generated SQL was:

{state["generated_sql"]}

PostgreSQL returned this error:

{state["sql_error"]}

Fix the SQL query.

Rules:
1. Return ONLY the corrected SQL query.
2. Generate only a SELECT query.
3. Use only tables and columns from the database schema.
4. Follow the analysis plan.
5. Do not explain the query.
6. Do not use markdown code fences.
"""

    repaired_sql = ask_llm(prompt)

    print("Repaired SQL:", repaired_sql)

    return {
        "generated_sql": repaired_sql.strip(),
        "retry_count": state["retry_count"] + 1,
        "sql_error": ""
    }

def decide_after_sql(state: AgentState):
    if state["sql_error"] == "":
        return "final_answer"

    if state["retry_count"] >= 1:
        return "final_answer"

    return "repair_sql"

def python_analysis_node(state: AgentState):
    print("Running Python analysis...")

    columns = list(state["database_result"][0].keys())
    rows = [
        tuple(row.values())
        for row in state["database_result"]
    ]

    dataframe = analyze_data(
        columns,
        rows
    )

    print("Pandas DataFrame:")
    print(dataframe)

    analysis_result = {}

    if "revenue" in dataframe.columns:
      analysis_result["revenue_summary"] = summarize_numeric_column(
        dataframe,
        "revenue"
    )

    elif "total_revenue" in dataframe.columns:
        analysis_result["revenue_summary"] = summarize_numeric_column(
        dataframe,
        "total_revenue"
    )

    print("Python analysis result:", analysis_result)

    return {
        "analysis_result": analysis_result
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
builder.add_node("python_analysis", python_analysis_node)
builder.add_node("repair_sql", repair_sql_node)
builder.add_node("final_answer", final_answer_node)

# Connect nodes
builder.add_edge(START, "receive_question")
builder.add_edge("receive_question", "analysis_plan")
builder.add_edge("analysis_plan", "generate_sql")
builder.add_edge("generate_sql", "execute_sql")

builder.add_conditional_edges(
    "execute_sql",
    decide_after_sql,
    {
        "repair_sql": "repair_sql",
        "final_answer": "python_analysis"
    }
)

builder.add_edge("python_analysis", "final_answer")

builder.add_edge("repair_sql", "execute_sql")

builder.add_edge("final_answer", END)

# Compile the graph
graph = builder.compile()