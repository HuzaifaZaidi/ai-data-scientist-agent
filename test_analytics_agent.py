from app.analytics_agent import answer_question


question = "Which sub-category generated the highest revenue?"

question = "Which category generated the highest profit?"
result = answer_question(question)

print("USER QUESTION")
print("=" * 60)
print(result["question"])

print("\nGENERATED SQL")
print("=" * 60)
print(result["sql"])

print("\nDATABASE RESULT")
print("=" * 60)
print(result["result"])

print("\nFINAL ANSWER")
print("=" * 60)
print(result["answer"])