from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# FastAPI app
app = FastAPI(title="Gemini Chatbot API")

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class ChatRequest(BaseModel):
    message: str

# Response schema
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(data: ChatRequest):
    try:
        response = model.generate_content(data.message)
        return ChatResponse(reply=response.text)
    except Exception as e:
        return ChatResponse(reply=f"Error: {str(e)}")

# Health check
@app.get("/")
def root():
    return {"status": "Gemini API is running"}
