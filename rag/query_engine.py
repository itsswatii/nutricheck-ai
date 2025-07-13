# import os
# from dotenv import load_dotenv
# load_dotenv()

# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.chains.question_answering import load_qa_chain
# from langchain_huggingface import HuggingFaceEndpoint

# def load_vectorstore(persist_dir="data/vectorstore"):
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-albert-small-v2")
#     vectorstore = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
#     return vectorstore

# def ask_question(query, k=4):
#     print("🔎 Searching for relevant context...")
#     vectorstore = load_vectorstore()
#     docs = vectorstore.similarity_search(query, k=k)
#     if not docs:
#         return "⚠️ No relevant information found."
#     print(f"📄 Found {len(docs)} relevant chunks.")

#     # Replace with your model on HF Hub, e.g. "google/flan-t5-small" or a HF endpoint url
#     #hf_endpoint_url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
#     #hf_endpoint_url = "https://api-inference.huggingface.co/models/google/flan-t5-base"
#     hf_endpoint_url = "https://api-inference.huggingface.co/models/bigscience/bloom-560m"



#     llm = HuggingFaceEndpoint(
#         endpoint_url=hf_endpoint_url,
#         huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
#         temperature=0.2,
#         max_new_tokens=256,
#     )

#     chain = load_qa_chain(llm, chain_type="stuff")

#     result = chain.invoke({"input_documents": docs, "question": query})
#     return result

# if __name__ == "__main__":
#     user_query = input("🔍 Ask about an ingredient: ")
#     answer = ask_question(user_query)
#     print(f"\n💡 Answer: {answer}")



import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import InferenceClient

# --- Helper function for chat completion ---
def hf_chat_completion(system, user, model="HuggingFaceTB/SmolLM3-3B"):
    client = InferenceClient(
        model=model,
        provider="hf-inference",
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.6
    )
    return res.choices[0].message["content"]

# --- Load the vectorstore ---
#def load_vectorstore(persist_dir="data/vectorstore"):
# def load_vectorstore(persist_dir="rag/data/vectorstore"):
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-albert-small-v2")
#     vectorstore = FAISS.load_local(persist_dir, embeddings, allow_dangerous_deserialization=True)
#     return vectorstore

def load_vectorstore():
    from pathlib import Path
    base_dir = Path(__file__).resolve().parent  # points to rag/
    persist_dir = base_dir / "data/vectorstore"

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-albert-small-v2")
    vectorstore = FAISS.load_local(str(persist_dir), embeddings, allow_dangerous_deserialization=True)
    return vectorstore


# --- Main Question Answering Function ---
def ask_question(query, k=4):
    print("🔎 Searching for relevant context...")
    vectorstore = load_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)

    if not docs:
        return "⚠️ No relevant information found."

    print(f"📄 Found {len(docs)} relevant chunks.")
    context_text = "\n\n".join([doc.page_content for doc in docs])

    # Messages
    system_message = (
        "You are a helpful assistant knowledgeable about food ingredients. "
        "Use the provided context to answer the user's question."
    )
    user_message = f"Context:\n{context_text}\n\nQuestion: {query}"

    # 🔁 Use the helper function
    answer = hf_chat_completion(system_message, user_message)

    # Clean up <think> tags for nicer output
    answer = answer.replace("<think>", "").replace("</think>", "").strip()
    return answer

# --- CLI entry point ---
if __name__ == "__main__":
    user_query = input("🔍 Ask about an ingredient: ")
    answer = ask_question(user_query)
    print(f"\n💡 Answer: {answer}")
