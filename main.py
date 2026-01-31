from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI(title="Gemini Chatbot API")

# Allow all origins (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

model = None

@app.on_event("startup")
def startup_event():
    global model
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY missing")
        return

    genai.configure(api_key=api_key)

    # ✅ Use a valid model from your list
    model = genai.GenerativeModel("models/gemini-flash-latest")
    print("Gemini model initialized successfully")

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: ChatRequest):
    if model is None:
        return {"reply": "AI model not ready"}

    try:
        response = model.generate_content(data.message)
        return {"reply": response.text}
    except Exception as e:
        print("Gemini error:", e)
        return {"reply": "Sorry, something went wrong.", "error": str(e)}

@app.get("/models")
def list_models():
    return [m.name for m in genai.list_models()]
