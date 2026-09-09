from app.graph import graph


result = graph.invoke(
    {
        "message": "Hello Agent"
    }
)

print("\nFINAL STATE")
print("=" * 50)
print(result)