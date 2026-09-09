from app.sql_agent import generate_sql
from app.database import execute_query


question = "Which sub-category generated the highest revenue?"

print("USER QUESTION")
print("=" * 50)
print(question)

# Step 1: Ask Gemini to generate SQL
sql = generate_sql(question)

print("\nGENERATED SQL")
print("=" * 50)
print(sql)

# Step 2: Execute the generated SQL
try:
    columns, rows = execute_query(sql)

    print("\nDATABASE RESULT")
    print("=" * 50)
    print(columns)

    for row in rows:
        print(row)

except ValueError as e:
    print("\nQUERY BLOCKED")
    print("=" * 50)
    print(e)