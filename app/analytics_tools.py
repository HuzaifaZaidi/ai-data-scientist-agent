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