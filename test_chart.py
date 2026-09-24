from app.analytics_tools import create_chart

data = """
[
    {"state": "Maharashtra", "revenue": 95348},
    {"state": "Madhya Pradesh", "revenue": 105140},
    {"state": "Delhi", "revenue": 22531},
    {"state": "Uttar Pradesh", "revenue": 22359},
    {"state": "Rajasthan", "revenue": 21149}
]
"""

result = create_chart.invoke(
    {
        "data": data,
        "x_column": "state",
        "y_column": "revenue"
    }
)

print("Chart created:")
print(result)