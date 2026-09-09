from app.llm import ask_llm


response = ask_llm(
    "Explain what revenue means in an e-commerce business "
    "in two simple sentences."
)

print("LLM RESPONSE")
print("=" * 50)
print(response)