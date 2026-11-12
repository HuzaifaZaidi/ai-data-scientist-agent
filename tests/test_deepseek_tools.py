from app.llm import llm
from app.analytics_tools import run_sql_query

# Give DeepSeek access to the SQL tool.
llm_with_tools = llm.bind_tools([run_sql_query])

# Ask a question that requires database access.
response = llm_with_tools.invoke(
    """
    Use the run_sql_query tool to find the total number of orders.

    Execute this SQL query:
    SELECT COUNT(*) AS total_orders FROM orders;

    Do not calculate or guess the answer yourself.
    """
)

# Display the tool call selected by DeepSeek.
print("Tool calls:", response.tool_calls)

if response.tool_calls:
    print("\nSUCCESS: DeepSeek successfully selected a tool.")
else:
    print("\nFAILED: DeepSeek did not select a tool.")