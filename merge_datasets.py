import pandas as pd
import json
import os

# ------------------------------
# Dataset paths
# ------------------------------
KAGGLE_CSV = "fashion-dataset/styles.csv"
KAGGLE_IMAGES = "fashion-dataset/images"

MYNTRA_CSV = "fashion-dataset/myntradataset/styles.csv"
MYNTRA_IMAGES = "fashion-dataset/myntradataset/images"

OUTPUT_FILE = "products.json"

products = []

# ------------------------------
# Function to process a dataset
# ------------------------------
def load_dataset(csv_path, images_folder):
    df = pd.read_csv(csv_path, on_bad_lines="skip")
    dataset_products = []

    for _, row in df.iterrows():
        image_file = f"{row['id']}.jpg"
        image_path = os.path.join(images_folder, image_file)

        if not os.path.exists(image_path):
            continue

        product = {
            "name": str(row.get("productDisplayName", "Unknown")),
            "price": int(row.get("price", 0)) if not pd.isna(row.get("price")) else 0,
            "description": str(row.get("productDescription", "")),
            "image": image_file,
            "folder": images_folder   # IMPORTANT: store full folder path
        }
        dataset_products.append(product)

    return dataset_products

# ------------------------------
# Load Kaggle dataset
# ------------------------------
print("Processing Kaggle dataset...")
products += load_dataset(KAGGLE_CSV, KAGGLE_IMAGES)

# ------------------------------
# Load Myntra dataset
# ------------------------------
print("Processing Myntra dataset...")
products += load_dataset(MYNTRA_CSV, MYNTRA_IMAGES)

# ------------------------------
# Save merged products.json
# ------------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

print("✔ products.json created!")
print(f"Total products merged: {len(products)}")
