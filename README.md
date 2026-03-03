# 🧠 Shulker RAG - AI Quiz Generator API
A lightweight, production-ready Flask backend that transforms meeting summaries into structured multiple-choice quizzes using Google Gemini AI. Designed as a microservice to plug into the Shulker meeting ecosystem.

💡 **Made by [Vasu Goel](https://github.com/vasug27)**

---

## ✅ Overview

A production-ready **Python + Flask backend** for AI-powered quiz generation:
- Accepts plain-text meeting summaries via REST API
- Generates **5 MCQs** with 4 options and a correct answer each
- Powered by **Google Gemini** (`gemini-flash-latest`)
- Returns clean, structured **JSON** ready for frontend consumption
- CORS-enabled for seamless frontend integration

---

## 🛠 Tech Stack

| Category | Technologies Used |
|---|---|
| Backend | Python, Flask 3.0.3 |
| AI Model | Google Gemini (`gemini-flash-latest`) |
| AI SDK | google-generativeai 0.8.3 |
| CORS | Flask-Cors 4.0.0 |
| Environment | python-dotenv 1.0.1 |
| Production Server | Gunicorn 23.0.0 |

---

## 📁 Folder Structure

```
Shulker_RAG/
├── api.py              # Flask app - routes and Gemini quiz generation logic
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed)
├── .gitignore          # Ignores venv, .env, __pycache__
└── README.md
```

---

## ⚙️ Setup Guide

**1. Clone the repository**
```bash
git clone https://github.com/Shulker-000/Shulker_RAG.git
cd Shulker_RAG
```

**2. Create and activate a virtual environment**
```bash
python -m venv myenv

# macOS/Linux
source myenv/bin/activate

# Windows
myenv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment**

Create a `.env` file in the root directory and add your key:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```
Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

**5. Start the server**
```bash
# Development
python api.py

# Production
gunicorn -w 4 -b 0.0.0.0:5050 api:app
```
Server runs at `http://localhost:5050`

---

## 📌 API Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check - confirms API is running |
| POST | `/generate-quiz` | Accepts plain-text summary, returns 5 MCQs with 4 options and correct answer each |

**POST `/generate-quiz`**
- **Content-Type:** `text/plain`
- **Response structure:**
```json
{
  "questions": [
    {
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer_text": "string"
    }
  ],
  "count": 5
}
```
- **Errors:** `400` empty body · `500` generation failed


## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`feature/new-feature`)
3. Commit changes & push
4. Open a PR 🎉

---

## 🧑 Author

**Vasu Goel**

[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:vasugoel2754@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vasugoel503/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vasug27)

---
*Built for Shulker (AI Video Conferencing Assistant) - A focused microservice extension of the [Shulker_AI](https://github.com/Shulker-000/Shulker_AI) repository.*
