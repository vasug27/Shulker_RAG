import os
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=API_KEY)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


def generate_quiz(summary: str):
    model_gem = genai.GenerativeModel("gemini-flash-latest")

    prompt = (
        "You are an AI meeting assistant. Based on the following meeting summary, "
        "generate exactly 5 multiple-choice poll questions to test comprehension. "
        "Each question must have exactly 4 distinct, realistic options and one correct answer. "
        "Return your response ONLY in valid JSON with this structure:\n\n"
        "{\n"
        '  \"questions\": [\n'
        "    {\n"
        '      \"question\": \"string\",\n'
        '      \"options\": [\"string\", \"string\", \"string\", \"string\"],\n'
        '      \"answer_text\": \"string\"\n'
        "    }\n"
        "  ],\n"
        '  \"count\": 5\n'
        "}\n\n"
        "Do NOT include any explanations, markdown, or extra text outside JSON.\n\n"
        f"Meeting Summary:\n{summary}"
    )

    response = model_gem.generate_content(prompt)
    raw_output = response.text.strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        cleaned = re.sub(r"```json|```", "", raw_output).strip()
        return json.loads(cleaned)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Quiz Generator API is running.",
        "endpoint": "/generate-quiz",
        "input_format": "Raw text (summary)"
    })


@app.route("/generate-quiz", methods=["POST"])
def quiz_route():
    summary = request.data.decode("utf-8").strip()
    if not summary:
        return jsonify({"error": "Empty summary"}), 400

    try:
        quiz_data = generate_quiz(summary)
        return jsonify(quiz_data)
    except Exception as e:
        print(f"[ERROR] Quiz generation failed: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)