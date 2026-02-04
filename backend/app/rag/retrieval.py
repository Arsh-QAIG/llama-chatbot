from .embeddings import embed
from .store import collection

def query_docs(question, k=2):
    if collection.count() == 0:
        return []

    q_emb = embed(question)
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k
    )
    return results.get("documents", [[]])[0]
