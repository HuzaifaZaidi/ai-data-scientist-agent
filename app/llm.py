import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError(
        "DEEPSEEK_API_KEY is not set in the .env file."
    )

llm = ChatDeepSeek(
    model="deepseek-flash",
    api_key=api_key,
    temperature=0
)

def ask_llm(prompt):
    response = llm.invoke(prompt)
    return response.content