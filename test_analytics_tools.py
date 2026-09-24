from app.analytics_tools import (
    analyze_data,
    summarize_numeric_column
)


columns = ["state", "revenue"]

rows = [
    ("Maharashtra", 95348),
    ("Madhya Pradesh", 105140),
    ("Delhi", 22531),
]


df = analyze_data(columns, rows)

print("DATAFRAME")
print("=" * 50)
print(df)

print("\nREVENUE SUMMARY")
print("=" * 50)

summary = summarize_numeric_column(
    df,
    "revenue"
)

print(summary)