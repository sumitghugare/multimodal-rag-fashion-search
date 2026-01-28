Multimodal RAG E‑Commerce Assistant — LLaMA‑3.2‑1B (Option A)


Summary: Local multimodal retrieval-augmented generation (RAG) app. Uses OpenCLIP + Sentence-Transformers for embeddings, FAISS (or NumPy fallback) for search, and LLaMA‑3.2‑1B GGUF via llama-cpp-python for on-device answers. Includes Streamlit UI.


Windows setup (brief):
1. Create virtualenv: python -m venv venv
2. Activate: venv\Scripts\activate
3. pip install -r requirements.txt
4. Download LLaMA‑3.2‑1B GGUF, set env var:
set LLAMA_GGUF_PATH=C:\path\to\llama-3.2-1b.gguf
5. Run demo ingestion: python ingest.py
6. Run app: streamlit run app.py

E:/multimodal_rag_project/venv/Scripts/Activate.ps1 
Resume bullets and more details in the top-level project README.