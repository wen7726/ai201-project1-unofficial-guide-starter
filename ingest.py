from pathlib import Path

RAW_DIR = Path("data/raw")

CHUNK_SIZE = 800
OVERLAP = 100


def load_documents():
    files = list(RAW_DIR.glob("*.txt"))

    documents = []

    for file in files:
        text = file.read_text(encoding="utf-8")

        documents.append({
            "source": file.name,
            "text": text
        })

    return documents


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    docs = load_documents()

    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["text"])

        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": i,
                "text": chunk
            })

    print(f"\nTotal chunks: {len(all_chunks)}")

    for chunk in all_chunks[:5]:
        print("\n" + "=" * 60)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"][:500])