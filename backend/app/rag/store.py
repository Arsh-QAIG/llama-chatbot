from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection("product_docs")

# .\.venv\Scripts\Activate.ps1 