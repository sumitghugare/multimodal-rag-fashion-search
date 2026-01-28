import requests

import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def ask_model(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Groq API Error: {e}"
