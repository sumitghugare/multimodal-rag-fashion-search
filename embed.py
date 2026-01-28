import os
import pickle
from PIL import Image
from models import get_text_embedding, get_image_embedding
import faiss
import numpy as np

DATA_DIR = "data"
TEXT_DIR = f"{DATA_DIR}/texts"
IMAGE_DIR = f"{DATA_DIR}/images"

embeddings = []
metadata = []

# Texts
for file in os.listdir(TEXT_DIR):
    if file.endswith(".txt"):
        text = open(f"{TEXT_DIR}/{file}", "r", encoding="utf-8").read()
        emb = get_text_embedding(text)
        embeddings.append(emb)
        metadata.append({"type": "text", "path": f"{TEXT_DIR}/{file}", "content": text})

# Images
for file in os.listdir(IMAGE_DIR):
    if file.lower().endswith(("jpg", "png")):
        img = Image.open(f"{IMAGE_DIR}/{file}")
        emb = get_image_embedding(img)
        embeddings.append(emb)
        metadata.append({"type": "image", "path": f"{IMAGE_DIR}/{file}", "content": img})

# Convert
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

with open("embeddings/vector_store.pkl", "wb") as f:
    pickle.dump({"index": index, "metadata": metadata}, f)

print("Vector store created ✔")
