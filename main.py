import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os


client = genai.Client(api_key=os.getenv("AIzaSyBFjbtrTgI-EjTroTkKb8hokDUpxJErntM"))

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-1.5-flash:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": req.message}]
            }
        ]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        return {"reply": "Error talking to Gemini API"}

    data = response.json()
    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    return {"reply": reply}
