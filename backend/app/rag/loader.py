from pathlib import Path

def load_docs():
    docs_path = Path("backend/data")
    documents = []

    for file in docs_path.glob("*.md"):
        text = file.read_text(encoding="utf-8")
        documents.append({
            "text": text,
            "source": file.name
        })

    return documents
