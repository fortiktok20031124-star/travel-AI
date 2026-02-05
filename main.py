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
You are a travel planning API.

Return ONLY valid JSON.
No explanations.
No markdown.
No extra text.

Schema:
{
  "trip": [
    {
      "day": number,
      "city": string,
      "places": [
        {
          "name": string,
          "type": string,
          "imageQuery": string,
          "description": string
        }
      ]
    }
  ]
}



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
