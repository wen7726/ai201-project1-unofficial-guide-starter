import os
from dotenv import load_dotenv
from groq import Groq

from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client_groq = Groq(api_key=GROQ_API_KEY)

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "housing_reviews"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client_chroma = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client_chroma.get_collection(name=COLLECTION_NAME)


def retrieve(query, k=5):
    query_embedding = embedding_model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results


def ask(question):
    results = retrieve(question)

    retrieved_docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(retrieved_docs)

    sources = list(set(meta["source"] for meta in metadatas))

    prompt = f"""
You are a housing review assistant.

Answer the question using ONLY the provided context.

If the context does not contain enough information, say:
"I don't have enough information from the provided documents."

Context:
{context}

Question:
{question}
"""

    response = client_groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Answer only from retrieved context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    question = "What do residents say about maintenance problems?"

    result = ask(question)

    print("\nANSWER:\n")
    print(result["answer"])

    print("\nSOURCES:\n")
    for source in result["sources"]:
        print("-", source)