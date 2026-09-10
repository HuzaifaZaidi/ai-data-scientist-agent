from app.graph import graph


question = input("Ask your question: ")


result = graph.invoke(
    {
        "user_question": question,
        "analysis_plan": "",
        "generated_sql": "",
        "database_result": [],
        "analysis_result": {},
        "final_answer": "",
        "sql_error": "",
        "retry_count": 0
    }
)

print("\nFINAL STATE")
print("=" * 60)

print("User Question:")
print(result["user_question"])

print("\nAnalysis Plan:")
print(result["analysis_plan"])

print("\nGenerated SQL:")
print(result["generated_sql"])

print("\nDatabase Result:")
print(result["database_result"])

print("\nPython Analysis:")
print(result["analysis_result"])

print("\nFinal Answer:")
print(result["final_answer"])