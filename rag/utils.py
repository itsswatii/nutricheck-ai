import os
import wikipedia
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def fetch_wikipedia_summary(term, sentences=2):
    """
    Fetch a short Wikipedia summary for a given term.
    """
    try:
        results = wikipedia.search(term)
        if not results:
            return "No summary found."
        summary = wikipedia.summary(results[0], sentences=sentences)
        return summary
    except Exception as e:
        return f"⚠️ Error fetching summary: {e}"

def load_docs(folder_path="data/rag_docs"):
    """
    Load all text documents from a folder into a list of LangChain Documents.
    """
    docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(folder_path, filename))
            docs.extend(loader.load())
    return docs

def split_docs(docs, chunk_size=1000, chunk_overlap=100):
    """
    Split documents into smaller chunks for better embedding.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(docs)

def embed_docs(docs, persist_dir="rag_store"):
    """
    Create vector embeddings for documents using HuggingFace and build a FAISS index.
    Save the index to disk.
    """
    #embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-albert-small-v2")
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    vectorstore.save_local(persist_dir)
    print(f"✅ Embeddings saved to: {persist_dir}")
    return vectorstore
