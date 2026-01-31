from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

# Configure Gemini
genai.configure(api_key=os.getenv("AIzaSyBPs15dhNtHHc1uxOty9_Jln7iAIsIurY4"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat_with_ai():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response = chat.send_message(user_message)
    return jsonify({"reply": response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

