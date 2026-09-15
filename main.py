from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os


app = FastAPI(
    title="SivoAI",
    description="Personal AI assistant",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# OpenRouter
# =========================

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "openrouter/free"


# =========================
# Question
# =========================

class Question(BaseModel):
    question: str


# =========================
# API
# =========================

@app.get("/api")
def api_home():
    return {
        "message": "SivoAI API is running!",
        "model": MODEL,
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_ai(data: Question):

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return {
            "question": data.question,
            "answer": "SivoAI is not configured with an AI API key."
        }

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": data.question
                }
            ]
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    answer = result["choices"][0]["message"]["content"]

    return {
        "question": data.question,
        "answer": answer
    }


# =========================
# Frontend
# =========================

frontend_path = os.path.join(
    os.path.dirname(__file__),
    "frontend"
)

app.mount(
    "/static",
    StaticFiles(directory=frontend_path),
    name="static"
)


@app.get("/")
def frontend():

    return FileResponse(
        os.path.join(frontend_path, "index.html")
    )