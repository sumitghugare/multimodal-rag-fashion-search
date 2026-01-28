# import faiss
# import numpy as np
# import json

# # Load product DB
# with open("products.json", "r") as f:
#     products = json.load(f)

# # Load FAISS index
# index = faiss.read_index("vector.index")

# def search_similar(query_vector, k=3):
#     distances, indices = index.search(np.expand_dims(query_vector, 0), k)
#     results = []

#     for idx in indices[0]:
#         if idx < len(products):
#             results.append(products[idx])

#     return results
import faiss
import numpy as np
import json
import os

# -------------------------------------
# Load product database
# -------------------------------------
PRODUCTS_FILE = "products.json"    # updated!
INDEX_FILE = "vector.index"

if not os.path.exists(PRODUCTS_FILE):
    raise FileNotFoundError("❌ products.json not found. Run extract_mens_5000.py first.")

with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
    products = json.load(f)

# -------------------------------------
# Load FAISS index
# -------------------------------------
if not os.path.exists(INDEX_FILE):
    raise FileNotFoundError("❌ vector.index missing. Run build_vectors.py first.")

index = faiss.read_index(INDEX_FILE)


# -------------------------------------
# Search function
# -------------------------------------
def search_similar(query_vector, k=6):
    """
    Given an image vector, return top-k similar products.
    """

    # Ensure correct shape
    q = np.expand_dims(query_vector.astype("float32"), axis=0)

    distances, indices = index.search(q, k)

    results = []

    for idx in indices[0]:
        if idx < len(products):
            item = products[idx]

            # Build correct local image path
            full_image_path = os.path.join(item["folder"], item["image"])

            item["image_path"] = full_image_path
            results.append(item)

    return results


