from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def chunk_text(text, chunk_size=300, overlap=60):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def load_docs():
    docs_path = DATA_DIR
    documents = []

    for file in docs_path.glob("*.md"):
        text = file.read_text(encoding="utf-8")
        for i, chunk in enumerate(chunk_text(text)):
            documents.append({
                "text": chunk,
                "source": f"{file.name}#chunk{i}"
            })

    return documents
