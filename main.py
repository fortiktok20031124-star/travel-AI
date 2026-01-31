from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from google import genai

app = FastAPI(title="Gemini Chatbot API (New Client)")

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class ChatRequest(BaseModel):
    message: str

# Initialize Gemini client
client = genai.Client()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: ChatRequest):
    try:
        # Use a valid current model from your list
        response = client.models.generate_content(
            model="models/gemini-3-flash-preview",
            contents=data.message
        )
        return {"reply": response.text}
    except Exception as e:
        return {
            "reply": "Sorry, something went wrong.",
            "error": str(e)
        }

@app.get("/models")
def list_models():
    # List available models
    models = client.models.list()
    return [m.name for m in models]
