# rag/ingest_doc.py

import os
from dotenv import load_dotenv
from utils import load_docs, split_docs, embed_docs, fetch_wikipedia_summary



load_dotenv()  # Load API keys from .env file

if __name__ == "__main__":
    source_dir = "../data/rag_docs"
    persist_dir = "data/vectorstore"

    print("📥 Loading documents...")
    docs = load_docs(source_dir)

    print(f"📚 Loaded {len(docs)} documents. Splitting into chunks...")
    chunks = split_docs(docs)

    print(f"🧠 Total chunks: {len(chunks)}. Generating embeddings...")
    embed_docs(chunks, persist_dir=persist_dir)

    print(f"✅ Embeddings saved to: {persist_dir}")
