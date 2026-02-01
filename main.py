from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai

app = FastAPI(title="Gemini Travel Agent API")

# Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Initialize Gemini client
client = genai.Client()

# 🔒 Travel Agent System Prompt (Backend controlled)
TRAVEL_AGENT_PROMPT = """
You are a professional travel agent AI.

Your role:
- Help users choose travel destinations
- Ask clarifying questions if needed
- Consider budget, vibe, safety, and crowd level
- Give realistic and safe recommendations
- Explain WHY you recommend a place

Rules:
- Do not act as a general chatbot
- Do not answer unrelated questions
- Be friendly and helpful
"""

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(data: ChatRequest):
    try:
        # 🧠 Combine system prompt + user message
        full_prompt = f"""
{TRAVEL_AGENT_PROMPT}

User request:
{data.message}

Respond as a travel agent.
"""

        response = client.models.generate_content(
            model="models/gemini-3-flash-preview",
            contents=full_prompt
        )

        return {"reply": response.text}

    except Exception as e:
        return {
            "reply": "Sorry, something went wrong.",
            "error": str(e)
        }

@app.get("/models")
def list_models():
    models = client.models.list()
    return [m.name for m in models]
