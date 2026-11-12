from app.llm import llm

response = llm.invoke(
    "Reply with exactly: DeepSeek connection successful"
)

print(response.content)