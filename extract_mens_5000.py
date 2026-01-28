# extract_mens_1000.py

import pandas as pd
import os
import json
import random

# -----------------------------
# YOUR DATASET FOLDERS
# -----------------------------
FOLDERS = [
    {
        "csv": "fashion-dataset/styles.csv",
        "images": "fashion-dataset/images"
    },
    {
        "csv": "fashion-dataset/myntradataset/styles.csv",
        "images": "fashion-dataset/myntradataset/images"
    }
]

OUTPUT_FILE = "products.json"
TARGET_COUNT = 1000  # ONLY 1000 PRODUCTS


# -----------------------------
# MEN'S KEYWORDS
# -----------------------------
MEN_KEYWORDS = [
    "Men", "Men's", "mens", "MEN", "men", "man", "t-shirt", "shirt",
    "hoodie", "jacket", "sweatshirt", "kurta", "jeans"
]


def is_men_product(name):
    if not isinstance(name, str):
        return False
    return any(keyword.lower() in name.lower() for keyword in MEN_KEYWORDS)


all_products = []

# -----------------------------
# READ BOTH DATASETS
# -----------------------------
for folder in FOLDERS:
    csv_path = folder["csv"]
    image_folder = folder["images"]

    if not os.path.exists(csv_path):
        print(f"❌ Missing CSV: {csv_path}")
        continue

    print(f"📄 Reading dataset: {csv_path}")

    df = pd.read_csv(csv_path, encoding="utf-8", on_bad_lines="skip")

    print(f"🔍 Total rows: {len(df)}")

    # Ensure image column exists
    if "id" not in df.columns and "filename" not in df.columns:
        print(f"❌ CSV missing image column: {csv_path}")
        continue

    # Some datasets use id, some use filename
    image_key = "id" if "id" in df.columns else "filename"

    # Filter men's products
    df_men = df[df["productDisplayName"].apply(is_men_product)]
    print(f"🧔 Men’s products found: {len(df_men)}")

    # Process each row
    for _, row in df_men.iterrows():
        img_name = str(row[image_key]) + ".jpg"
        img_path = os.path.join(image_folder, img_name)

        if not os.path.exists(img_path):
            continue

        product = {
            "name": str(row["productDisplayName"]),
            "price": int(row["price"]) if "price" in df.columns and not pd.isna(row["price"]) else 0,
            "description": str(row["productDisplayName"]),
            "image": img_name,
            "folder": image_folder
        }

        all_products.append(product)


print(f"\n✅ Total men’s products found (before filtering): {len(all_products)}")

# -----------------------------
# LIMIT TO 1000 PRODUCTS
# -----------------------------
random.shuffle(all_products)
final_products = all_products[:TARGET_COUNT]

print(f"🎯 Final product count: {len(final_products)}")

# -----------------------------
# SAVE products.json
# -----------------------------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_products, f, indent=4)

print(f"\n🎉 Saved {len(final_products)} products to {OUTPUT_FILE}")
 