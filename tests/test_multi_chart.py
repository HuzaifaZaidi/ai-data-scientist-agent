from app.analytics_tools import create_chart

sample_data = [
    {"category": "Electronics", "revenue": 165267, "profit": 10494},
    {"category": "Clothing", "revenue": 139054, "profit": 11163},
    {"category": "Furniture", "revenue": 127181, "profit": 2298}
]

import json

result = create_chart.invoke({
    "data": json.dumps(sample_data),
    "x_column": "category",
    "y_columns": ["revenue", "profit"]
})

print(result)