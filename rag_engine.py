# rag_engine.py
import os
import requests

# ✅ Hardcoded API key (keep it private!)
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


if GROQ_API_KEY.strip() == "":
    raise ValueError("❌ Missing GROQ_API_KEY. Please add your key inside rag_engine.py")

API_URL = "https://api.groq.com/openai/v1/chat/completions"


def rag_answer(user_query, retrieved_text):
    """
    Combines user's query + retrieved product details
    and sends it to Groq's LLaMA-3 model for final answer.
    """

    prompt = f"""
You are an expert product assistant.
The user uploaded an image and wants information.

User Question:
{user_query}

Retrieved Product Information:
{retrieved_text}

Give a short, helpful answer.
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": "llama3-8b-8192.2",   # ✅ Updated model (error solved)
        # Or use: "llama3-70b-8192"
        "messages": [
            {"role": "system", "content": "You are a helpful shopping assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code != 200:
        return f"❌ Groq API Error: {response.text}"

    return response.json()["choices"][0]["message"]["content"]
