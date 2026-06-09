from sentence_transformers import SentenceTransformer
import chromadb
from ingest import load_documents, chunk_text

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "housing_reviews"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def build_vector_store():
    docs = load_documents()

    ids = []
    texts = []
    metadatas = []

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['source']}_{i}"
            ids.append(chunk_id)
            texts.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "chunk_id": i
            })

    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Added {len(texts)} chunks to ChromaDB")


def retrieve(query, k=5):
    query_embedding = model.encode([query]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results


if __name__ == "__main__":
    build_vector_store()

    test_queries = [
        "What do residents say about noise complaints?",
        "What problems do residents mention about maintenance?",
        "What advice do people give about moving out for the first time?"
    ]

    for query in test_queries:
        print("\n" + "=" * 80)
        print(f"Query: {query}")

        results = retrieve(query)

        for i, doc in enumerate(results["documents"][0]):
            print("\n--- Result", i + 1, "---")
            print("Source:", results["metadatas"][0][i]["source"])
            print("Distance:", results["distances"][0][i])
            print(doc[:700])