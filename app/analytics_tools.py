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

    try:
        records = json.loads(data)
    except json.JSONDecodeError:
        return (
            "The analysis tool received invalid JSON data. "
            "Please run the SQL query again and pass the complete "
            "JSON result to the analysis tool."
        )

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

def create_chart(data: str, x_column: str, y_columns: list[str]) -> str:
    """
    Create a bar chart containing one or more numerical metrics.

    Use this tool when the user requests a visualization.
    Pass all requested numerical columns in y_columns.
    """

    import json
    import os
    import uuid

    import matplotlib
    matplotlib.use("Agg")

    import matplotlib.pyplot as plt
    import pandas as pd

    try:
        records = json.loads(data)
    except json.JSONDecodeError:
        return "Invalid JSON data received for chart generation."

    if not records:
        return "No data available for visualization."

    dataframe = pd.DataFrame(records)

    if x_column not in dataframe.columns:
        return f"Column '{x_column}' was not found in the data."

    if not y_columns:
        return "At least one metric column is required."

    for column in y_columns:
        if column not in dataframe.columns:
            return f"Column '{column}' was not found in the data."

    os.makedirs("charts", exist_ok=True)

    chart_path = f"charts/chart_{uuid.uuid4().hex[:8]}.png"

    # Create one subplot for each requested metric.
    fig, axes = plt.subplots(
        nrows=len(y_columns),
        ncols=1,
        figsize=(10, 5 * len(y_columns)),
        squeeze=False
    )

    axes = axes.flatten()

    for ax, column in zip(axes, y_columns):

        values = pd.to_numeric(dataframe[column], errors="coerce")

        if values.isna().all():
            plt.close(fig)
            return f"Column '{column}' does not contain valid numeric values."

        ax.bar(dataframe[x_column], values)

        ax.set_xlabel(x_column)
        ax.set_ylabel(column)
        ax.set_title(f"{column} by {x_column}")

        ax.tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    return f"CHART_CREATED:{chart_path}"