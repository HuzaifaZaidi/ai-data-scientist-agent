from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.agent import ask_data_agent
from fastapi.responses import FileResponse

app = FastAPI(
    title="AI Data Scientist Agent",
    description="AI-powered analytics agent for e-commerce data",
    version="1.0.0"
)

app.mount("/charts", StaticFiles(directory="charts"), name="charts")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return FileResponse("frontend/index.html")


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = ask_data_agent(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "chart": result["chart"]
    }