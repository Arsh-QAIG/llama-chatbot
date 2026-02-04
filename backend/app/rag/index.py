from .loader import load_docs
from .embeddings import embed
from .store import collection
import uuid

def index_docs(force=False):
    if not force and collection.count() > 0:
        return

    docs = load_docs()
    if not docs:
        print("No documents found to index.")
        return

    for doc in docs:
        collection.add(
            documents=[doc["text"]],
            embeddings=[embed(doc["text"])],
            metadatas=[{"source": doc["source"]}],
            ids=[str(uuid.uuid4())]
        )

if __name__ == "__main__":
    index_docs()
    print("Docs indexed")
