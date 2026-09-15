from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests
import os


app = FastAPI(
    title="SivoAI",
   description="Personal AI assistant powered by Qwen 2.5 3B",
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
# Ollama
# =========================

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

MODEL = "qwen2.5:3b"


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
        "message": "AfriAI API is running!",
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

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": data.question,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return {
        "question": data.question,
        "answer": result["response"]
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