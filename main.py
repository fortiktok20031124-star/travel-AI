import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

@app.post("/chat")
async def chat(req: ChatRequest):
    if not GEMINI_API_KEY:
        return {"reply": "API Key missing in Railway Variables."}

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": req.message}]
            }
        ]
    }

    try:
        response = requests.post(
            GEMINI_URL,
            json=payload,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        return {
            "reply": data["candidates"][0]["content"]["parts"][0]["text"]
        }

    except requests.exceptions.HTTPError as e:
        return {"reply": f"Gemini API error: {response.text}"}

    except Exception as e:
        return {"reply": f"Connection error: {str(e)}"}
