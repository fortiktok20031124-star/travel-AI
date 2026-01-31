from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.get("/models")
def list_models():
    models = genai.list_models()
    return [m.name for m in models]

@app.post("/chat")
def chat(data: ChatRequest):
    try:
        # Suppose we pick a valid model below
        chosen_model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = chosen_model.generate_content(data.message)
        return {"reply": response.text}
    except Exception as e:
        return {"reply": "Error", "error": str(e)}
