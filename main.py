from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI(title="Gemini Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
def startup_event():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found")

    genai.configure(api_key=api_key)

    global model
    model = genai.GenerativeModel("gemini-pro")  # ✅ FIXED MODEL

@app.get("/")
def health():
    return {"status": "Gemini API running"}



@app.post("/chat")
def chat(data: ChatRequest):
    try:
        response = model.generate_content(data.message)
        return {"reply": response.text}
    except Exception as e:
        return {
            "reply": "Sorry, something went wrong.",
            "error": str(e)
        }
