from fastapi import FastAPI
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

app = FastAPI()

@app.post("/chat")
async def chat(user_message: str):

    # Step 1: Extract preferences
    extract_prompt = f"""
    Extract travel preferences and return JSON only.

    Message: {user_message}
    """

    model = genai.GenerativeModel("gemini-pro")
    prefs = model.generate_content(extract_prompt).text

    # Step 2: Recommend
    recommend_prompt = f"""
    You are a travel agent.

    User preferences:
    {prefs}

    Available destinations:
    {DESTINATION_DATA}

    Recommend top 3 destinations with reasons.
    """

    response = model.generate_content(recommend_prompt)

    return {"reply": response.text}
