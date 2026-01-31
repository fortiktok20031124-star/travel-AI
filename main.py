import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 1. SECURITY FIX: Get the key from the environment variable NAME, not the value itself.
# In Railway, you will create a variable named GEMINI_API_KEY.
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
        raise HTTPException(status_code=500, detail="API Key not configured in Railway settings.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-1.5-flash:generateContent"
        f"?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [{"text": req.message}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Check for HTTP errors
        
        data = response.json()
        # Extracting the text response safely
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"reply": reply}
        
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    # Railway provides the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
