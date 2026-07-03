import os
import json
import re
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
import uvicorn

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

genai.configure(api_key=API_KEY)

app = FastAPI(title="Shulker RAG - AI Quiz Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/")
def home():
    return {
        "message": "Quiz Generator API is running.",
        "endpoint": "/generate-quiz",
        "input_format": "Raw text (summary)"
    }


@app.post(
    "/generate-quiz",
    openapi_extra={
        "requestBody": {
            "content": {
                "text/plain": {
                    "schema": {
                        "type": "string",
                        "description": "Raw meeting summary text"
                    }
                }
            },
            "required": True
        }
    }
)
async def quiz_route(request: Request):
    body = await request.body()
    summary = body.decode("utf-8").strip()
    if not summary:
        raise HTTPException(status_code=400, detail="Empty summary")

    try:
        quiz_data = generate_quiz(summary)
        return quiz_data
    except Exception as e:
        print(f"[ERROR] Quiz generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)