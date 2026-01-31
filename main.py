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
        raise HTTPException(status_code=500, detail="API Key not found in Railway Variables.")

    # Using the STABLE v1 endpoint for 2026
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"

    # Moving the key to headers (Fixes 404 and is more secure)
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": req.message}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # If Google says 404, it might be the model name. Let's handle it.
        if response.status_code == 404:
            return {"reply": "Error: Model not found. Please verify your Google AI Studio project permits gemini-1.5-flash."}
            
        response.raise_for_status() 
        
        data = response.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}
        
    except Exception as e:
        # We don't return 'e' directly to avoid leaking the URL/Key in errors
        return {"reply": "The AI is currently unavailable. Please check your Railway logs for details."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
