import os
import json
import numpy as np
import faiss
from PIL import Image
from image_encoder import encode_image

PRODUCTS_FILE = "products.json"

with open(PRODUCTS_FILE, "r") as f:
    products = json.load(f)

vectors = []
valid_products = []

for item in products:
    img_path = os.path.join(item["folder"], item["image"])

    if not os.path.exists(img_path):
        print(f"⚠ Missing image: {img_path}")
        continue

    img = Image.open(img_path).convert("RGB")
    vec = encode_image(img)

    vectors.append(vec)
    valid_products.append(item)

vectors = np.array(vectors).astype("float32")

np.save("vectors.npy", vectors)

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

faiss.write_index(index, "vector.index")

with open("products_clean.json", "w") as f:
    json.dump(valid_products, f, indent=4)

print("✔ Vector index built!")
print(f"Products encoded: {len(valid_products)}")
