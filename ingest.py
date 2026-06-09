import re
from pathlib import Path

RAW_DIR = Path("data/raw")


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


def chunk_text(text):
    """
    Split each document by Review sections.
    This works better for review-style housing documents because each review
    is usually one self-contained student experience.
    """
    parts = re.split(r"\n\s*Review\s+\d+\s*:", text)

    header = parts[0].strip()
    reviews = parts[1:]

    chunks = []

    for i, review in enumerate(reviews, start=1):
        review = review.strip()

        if len(review) < 40:
            continue

        chunk = f"{header}\n\nReview {i}:\n{review}"
        chunks.append(chunk)

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

    print(f"Found {len(docs)} documents")
    print(f"Total chunks: {len(all_chunks)}")

    for chunk in all_chunks[:8]:
        print("\n" + "=" * 60)
        print(f"Source: {chunk['source']}")
        print(f"Chunk ID: {chunk['chunk_id']}")
        print(chunk["text"][:700])