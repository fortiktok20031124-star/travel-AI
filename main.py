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

Your mission:
- Recommend travel destinations based on user preferences
- Be concise, friendly, and practical
- Focus on decision-making, not long essays

Rules:
- If essential information is missing, ask ONLY ONE clarifying question at a time
- Recommend at most 3 destinations
- For each destination, give:
  • One-line vibe
  • One main reason it fits
- Avoid unnecessary storytelling
- Stay strictly within travel-related topics

Response format:
1. Short greeting (1 line)
2. Recommendations (bullet points)
3. ONE clarifying question at the end
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
