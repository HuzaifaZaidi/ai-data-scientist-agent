from app.analytics_tools import analyze_dataframe


data = """state,revenue,profit
Maharashtra,95348,6176
Madhya Pradesh,105140,5551
Delhi,22531,2987
"""


result = analyze_dataframe.invoke(data)

print(result)