# models.py
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# -----------------------------------------------------
# 🔥 ONLY CHANGE YOU MUST DO IN THE ENTIRE PROJECT
# -----------------------------------------------------
client = OpenAI(api_key="YOUR_API_KEY_HERE")
# -----------------------------------------------------

# Load CLIP model for image/text embedding
image_encoder = SentenceTransformer("clip-ViT-B-32")


def embed_text(text: str):
    """
    Convert any input to string to avoid:
    ValueError: text input must be of type `str`
    """
    if not isinstance(text, str):
        text = str(text)

    return image_encoder.encode([text], convert_to_numpy=True)[0]


def embed_image(image_path: str):
    """
    Convert image file to CLIP embedding.
    """
    img = Image.open(image_path).convert("RGB")
    return image_encoder.encode([img], convert_to_numpy=True)[0]


def generate_answer(context: str, question: str):
    """
    Use OpenAI model to generate the final answer.
    """

    prompt = f"""
    You are an AI assistant for a clothing store.
    Use the context to answer the question.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    Respond clearly and helpfully.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message["content"]
