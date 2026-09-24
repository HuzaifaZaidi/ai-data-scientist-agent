import pandas as pd


def analyze_data(columns, rows):
    """
    Convert database results into a Pandas DataFrame.
    Supports both list-of-tuples and list-of-dictionaries.
    """

    if rows and isinstance(rows[0], dict):
        dataframe = pd.DataFrame(rows)
    else:
        dataframe = pd.DataFrame(
            rows,
            columns=columns
        )

    return dataframe


def summarize_numeric_column(dataframe, column):
    """
    Calculate basic statistics for a numeric column.
    """

    return {
        "count": int(dataframe[column].count()),
        "mean": float(dataframe[column].mean()),
        "minimum": float(dataframe[column].min()),
        "maximum": float(dataframe[column].max()),
        "sum": float(dataframe[column].sum())
    }
from langchain_core.tools import tool


@tool
def run_sql_query(query: str) -> str:
    """
    Execute a read-only SQL query against the PostgreSQL database.

    Use this tool when database information is required to answer
    the user's question.
    """

    import json

    from app.database import execute_query

    columns, rows = execute_query(query)

    if not rows:
        return json.dumps([])

    result = []

    for row in rows:
        record = {}

        for column, value in zip(columns, row):
            if hasattr(value, "isoformat"):
                value = value.isoformat()
            elif hasattr(value, "__float__") and not isinstance(value, (int, float)):
                value = float(value)

            record[column] = value

        result.append(record)

    return json.dumps(result)


@tool
def analyze_dataframe(data: str) -> str:
    """
    Analyze tabular JSON data using Python and Pandas.

    Use this tool when calculations or statistical analysis
    are required after retrieving data from the database.
    """

    import json
    import pandas as pd

    records = json.loads(data)

    if not records:
        return "No data available for analysis."

    dataframe = pd.DataFrame(records)

    results = []

    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        results.append(
            f"Average {column}: {dataframe[column].mean():.2f}"
        )

    return "\n".join(results)
@tool
def create_chart(data: str, x_column: str, y_column: str) -> str:
    """
    Create a bar chart from tabular JSON data.

    Use this tool when a visualization would help explain
    the data or comparison requested by the user.
    """

    import json
    import os

    import matplotlib

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import pandas as pd

    records = json.loads(data)

    if not records:
        return "No data available for visualization."

    dataframe = pd.DataFrame(records)

    if x_column not in dataframe.columns:
        return f"Column '{x_column}' was not found in the data."

    if y_column not in dataframe.columns:
        return f"Column '{y_column}' was not found in the data."

    os.makedirs("charts", exist_ok=True)

    import uuid

    chart_path = f"charts/chart_{uuid.uuid4().hex[:8]}.png"

    plt.figure(figsize=(10, 6))
    plt.bar(dataframe[x_column], dataframe[y_column])

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{y_column} by {x_column}")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(chart_path)
    plt.close()

    return chart_path