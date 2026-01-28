# import streamlit as st
# from PIL import Image
# import numpy as np
# import os

# from image_encoder import encode_image
# from vector_store import search_similar
# from rag_engine import rag_answer


# # -------------------------------
# # PAGE CONFIG
# # -------------------------------
# st.set_page_config(
#     page_title="AI Fashion Search",
#     page_icon="🛍️",
#     layout="wide"
# )

# # -------------------------------
# # GLOBAL CSS (Professional UI)
# # -------------------------------
# st.markdown("""
# <style>

# body {
#     background: #f5f5f5;
#     font-family: 'Inter', sans-serif;
# }

# /* Header Title */
# .title {
#     text-align: center;
#     font-size: 48px;
#     font-weight: 700;
#     padding-top: 10px;
#     background: linear-gradient(90deg, #ff6f61, #ff3b3b);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
# }

# /* Product Grid */
# .product-card {
#     background: rgba(255,255,255,0.9);
#     border-radius: 18px;
#     padding: 18px;
#     margin-bottom: 25px;
#     text-align: center;
#     box-shadow: 0px 8px 20px rgba(0,0,0,0.1);
#     transition: 0.3s;
# }
# .product-card:hover {
#     transform: scale(1.04);
#     box-shadow: 0px 10px 28px rgba(0,0,0,0.18);
# }

# /* Product Image */
# .product-img {
#     border-radius: 12px;
#     width: 240px;
#     height: 260px;
#     object-fit: cover;
# }

# /* Chat Bubbles */
# .chat-container {
#     margin-top: 25px;
# }
# .chat-bubble-user {
#     background: #d1ffd6;
#     padding: 14px;
#     border-radius: 12px;
#     margin-bottom: 8px;
#     width: fit-content;
#     max-width: 60%;
# }
# .chat-bubble-ai {
#     background: #ffe2db;
#     padding: 14px;
#     border-radius: 12px;
#     margin-bottom: 8px;
#     width: fit-content;
#     max-width: 60%;
# }

# /* Buttons */
# .stButton>button {
#     background: #ff6f61;
#     color: white;
#     padding: 10px 15px;
#     border-radius: 10px;
#     font-weight: 600;
#     transition: 0.2s;
# }
# .stButton>button:hover {
#     background: #ff3b3b;
# }

# </style>
# """, unsafe_allow_html=True)


# # -------------------------------
# # HEADER
# # -------------------------------
# st.markdown("<h1 class='title'>AI Fashion Search Assistant 👗🛍️</h1>", unsafe_allow_html=True)
# st.write("")


# # -------------------------------
# # SIDEBAR
# # -------------------------------
# with st.sidebar:
#     st.header("📌 How it works")
#     st.write("""
#     - Upload any product image  
#     - System finds the most similar products  
#     - Ask questions like  
#       *“Is there a cheaper option?”*  
#       *“Show similar hoodies.”*  
#     - AI will answer smartly  
#     """)
#     st.markdown("---")
#     st.info("Powered by CLIP + FAISS + Groq LLaMA-3")


# # -------------------------------
# # MAIN INPUTS
# # -------------------------------
# uploaded = st.file_uploader("📤 Upload fashion product image", type=["jpg", "png", "jpeg"])

# user_query = st.text_input("💬 Ask about this product or similar products")


# # -------------------------------
# # MAIN LOGIC
# # -------------------------------
# if uploaded:

#     img = Image.open(uploaded).convert("RGB")
#     st.image(img, caption="Uploaded Image", width=300)

#     img_np = np.array(img)

#     # 1️⃣ Encode image
#     with st.spinner("🔍 Extracting image features..."):
#         img_vector = encode_image(img_np)

#     # 2️⃣ Search similar products
#     with st.spinner("📦 Finding visually similar products..."):
#         results = search_similar(img_vector)

#     # 3️⃣ Render results
#     if not results:
#         st.error("No similar products found.")
#     else:
#         st.subheader("✨ Recommended Products")

#         cols = st.columns(3)

#         for idx, item in enumerate(results):
#             col = cols[idx % 3]
#             with col:
#                 st.markdown("<div class='product-card'>", unsafe_allow_html=True)

#                 image_path = os.path.join(item["folder"], item["image"])
#                 if os.path.exists(image_path):
#                     product_img = Image.open(image_path)
#                     st.image(product_img, width=240)
#                 else:
#                     st.image("https://via.placeholder.com/240", width=240)

#                 st.markdown(f"### {item['name']}")
#                 st.markdown(f"**₹ {item.get('price', 0)}**")

#                 with st.expander("📜 Description"):
#                     st.write(item.get("description", ""))

#                 st.button("Select Product", key=f"p_{idx}")

#                 st.markdown("</div>", unsafe_allow_html=True)

#     # 4️⃣ RAG Response
#     if user_query and results:
#         st.markdown("### 🤖 AI Assistant Response")

#         retrieved_text = "\n".join(
#             f"{r['name']} - {r.get('description', '')}" for r in results
#         )

#         with st.spinner("Thinking..."):
#             answer = rag_answer(user_query, retrieved_text)

#         st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
#         st.markdown(f"<div class='chat-bubble-user'>You: {user_query}</div>", unsafe_allow_html=True)
#         st.markdown(f"<div class='chat-bubble-ai'>AI: {answer}</div>", unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)
# app.py
import streamlit as st
from PIL import Image
import numpy as np
import os

from image_encoder import encode_image
from vector_store import search_similar
from rag_engine import rag_answer

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="🛒 Multimodal Product Search",
    layout="wide",
    page_icon="🛍️",
)

# -----------------------
# Global Dark Theme + Neon
# -----------------------
st.markdown(
    """
<style>
/* ===== Global Background ===== */
body {
    background: radial-gradient(circle at top, #1e293b 0, #020617 55%, #020617 100%) !important;
    color: #e5e7eb !important;
}

/* Streamlit main container */
.main {
    background: transparent !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
    color: #e5e7eb;
    border-right: 1px solid #1f2937;
}

/* Input labels */
label, .stTextInput label, .stFileUploader label {
    color: #e5e7eb !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    border: 1px dashed #334155 !important;
    padding: 1rem;
    border-radius: 0.75rem;
    background: rgba(15,23,42,0.8);
}

/* Text input */
input[type="text"] {
    background: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 0.5rem !important;
    border: 1px solid #1f2937 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #22d3ee, #fb923c);
    color: #020617 !important;
    border-radius: 999px;
    padding: 0.5rem 1.2rem;
    border: none;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 0 10px rgba(34, 211, 238, 0.4);
}
.stButton>button:hover {
    transform: translateY(-1px) scale(1.02);
    box-shadow: 0 0 18px rgba(34, 211, 238, 0.7);
}

/* ===== Product Cards ===== */
.product-card {
    background: radial-gradient(circle at top, #0f172a, #020617);
    padding: 14px;
    border-radius: 18px;
    text-align: center;
    transition: transform 0.25s, box-shadow 0.25s, border 0.25s;
    box-shadow: 0 12px 30px rgba(15,23,42,0.7);
    border: 1px solid rgba(148,163,184,0.2);
    height: 100%;
}
.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(15,23,42,0.9);
    border-color: #22d3ee;
}

/* Product title */
.product-title {
    font-weight: 600;
    font-size: 0.95rem;
    color: #e5e7eb;
    margin-top: 0.5rem;
}

/* Price */
.product-price {
    color: #22c55e;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

/* Description expander */
details summary {
    color: #a5b4fc;
}

/* Ensure all product images have similar size */
.product-img img {
    border-radius: 12px;
    object-fit: cover;
    width: 100% !important;
    height: 210px !important;
}

/* ===== Chat bubbles ===== */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    margin-top: 1rem;
}
.chat-bubble {
    padding: 0.75rem 1rem;
    border-radius: 16px;
    max-width: 80%;
    font-size: 0.95rem;
    line-height: 1.4;
}
.chat-bubble-user {
    background: rgba(34,211,238,0.12);
    border: 1px solid rgba(34,211,238,0.5);
    align-self: flex-end;
}
.chat-bubble-ai {
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(148,163,184,0.5);
    box-shadow: 0 10px 25px rgba(15,23,42,0.8);
}

/* Section title underline */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e5e7eb;
    border-bottom: 1px solid #1f2937;
    padding-bottom: 0.3rem;
    margin-bottom: 0.8rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------
# Header
# -----------------------
st.markdown(
    """
<div style="text-align:center; margin-bottom: 0.4rem;">
  <h1 style="color:#e5e7eb; margin-bottom:0.2rem;">
    🛒 Multimodal Fashion Search & AI Stylist
  </h1>
  <p style="color:#9ca3af; font-size:0.95rem;">
    Upload a product image and get visually similar recommendations powered by CLIP + FAISS + LLaMA-3.1.
  </p>
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("---")

# -----------------------
# Sidebar
# -----------------------
with st.sidebar:
    st.subheader("How to use")
    st.markdown(
        """
1. Upload a **fashion product image** (T-shirt, hoodie, shoes, etc.).  
2. Optionally, ask a question like:  
   - *"Suggest cheaper similar options"*  
   - *"Show similar hoodies under 1500"*  
3. The system will retrieve **top similar items** and an **AI explanation**.
        """
    )


# -----------------------
# Main Inputs
# -----------------------
col_left, col_right = st.columns([1, 2])

with col_left:
    uploaded = st.file_uploader(
        "📷 Upload a product image", type=["jpg", "jpeg", "png"]
    )
    user_query = st.text_input(
        "💬 Ask about this product or similar products", placeholder="e.g., Show similar blue T-shirts under 800"
    )

with col_right:
    if uploaded:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, caption="Uploaded Image", use_container_width=False, width=320)

# We only proceed if image is uploaded
if uploaded:
    img_np = np.array(img)

    # --------------------------
    # Encode Image
    # --------------------------
    with st.spinner("🔍 Extracting image features..."):
        img_vector = encode_image(img_np)

    # --------------------------
    # FAISS Search
    # --------------------------
    with st.spinner("📦 Searching visually similar products..."):
        results = search_similar(img_vector, k=6)  # show up to 6

    if not results:
        st.error("No matching products found in the index. Try another image.")
    else:
        st.markdown('<div class="section-title">Recommended Products</div>', unsafe_allow_html=True)

        num_cols = 3
        cols = st.columns(num_cols)
        placeholder_url = "https://via.placeholder.com/300x210?text=No+Image"

        for idx, item in enumerate(results):
            col = cols[idx % num_cols]
            with col:
                st.markdown('<div class="product-card">', unsafe_allow_html=True)

                # Image resolution
                image_filename = item.get("image")
                # Support both small demo and Myntra dataset with 'folder' key
                folder = item.get("folder", "images")
                full_path = os.path.join(folder, image_filename) if image_filename else ""

                # Image block
                st.markdown('<div class="product-img">', unsafe_allow_html=True)
                try:
                    if full_path and os.path.exists(full_path):
                        img_item = Image.open(full_path)
                        st.image(img_item, caption=None, use_container_width=True)
                    else:
                        st.image(placeholder_url, caption=None, use_container_width=True)
                except Exception:
                    st.image(placeholder_url, caption=None, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Text info
                name = item.get("name", "Unnamed Product")
                price = item.get("price", 0)
                desc = item.get("description", "No description available.")

                st.markdown(f'<div class="product-title">{name}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="product-price">₹{price}</div>', unsafe_allow_html=True)

                with st.expander("View Description"):
                    st.write(desc)

                # small action button (no backend yet)
                st.button("Select Product", key=f"btn_{idx}")

                st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------
    # RAG Answer using Groq LLaMA-3.1
    # --------------------------
    if user_query and results:
        retrieved_info = "\n".join(
            [f"{r['name']} — {r.get('description', '')} — ₹{r.get('price', 0)}" for r in results]
        )

        with st.spinner("🤖 AI Stylist is thinking..."):
            answer = rag_answer(user_query, retrieved_info)

        st.markdown('<div class="section-title">AI Stylist Response</div>', unsafe_allow_html=True)

        # Chat-style bubbles
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="chat-bubble chat-bubble-user">You: {user_query}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="chat-bubble chat-bubble-ai">AI: {answer}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👆 Upload a product image to start searching similar items.")
