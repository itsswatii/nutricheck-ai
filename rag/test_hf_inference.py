import os
from huggingface_hub import InferenceClient

def hf_chat_completion(system, user, model="HuggingFaceTB/SmolLM3-3B"):
    client = InferenceClient(
        model=model,
        provider="hf-inference",
        token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
    )
    res = client.chat.completions.create(
        model=model,
        messages=[{"role":"system","content":system}, {"role":"user","content":user}],
        temperature=0.6
    )
    return res.choices[0].message["content"]

if __name__ == "__main__":
    system = "You are a helpful assistant."
    user = input("Ask about an ingredient: ")
    ans = hf_chat_completion(system, user)
    print("\n💡 Answer:", ans)

