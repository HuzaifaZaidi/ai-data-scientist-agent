from app.agent import ask_data_agent

question = """
Show me the revenue for each state and create a chart
comparing revenue across states.
"""

answer = ask_data_agent(question)

print("\nFinal Answer:")
print(answer)