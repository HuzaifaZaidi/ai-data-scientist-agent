from app.graph import graph


question = input("Ask your question: ")


result = graph.invoke(
    {
        "user_question": question,
        "generated_sql": "",
        "database_result": [],
        "final_answer": ""
    }
)


print("\nFINAL STATE")
print("=" * 60)

print("User Question:")
print(result["user_question"])

print("\nGenerated SQL:")
print(result["generated_sql"])

print("\nDatabase Result:")
print(result["database_result"])

print("\nFinal Answer:")
print(result["final_answer"])