import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Railway will look for this in your 'Variables' tab
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

@app.post("/chat")
async def chat(req: ChatRequest):
    if not GEMINI_API_KEY:
        return {"reply": "API Key missing in Railway Variables."}

    # UPDATE: Using the 2026 stable Gemini 3 Flash model
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-3-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [{"parts": [{"text": req.message}]}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 404:
            # Fallback for older projects that might still use 2.5
            return {"reply": "Model error. Try changing 'gemini-3-flash' to 'gemini-2.5-flash' in your code."}
            
        response.raise_for_status()
        data = response.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}
        
    except Exception as e:
        return {"reply": f"Connection Error: {str(e)}"}



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

