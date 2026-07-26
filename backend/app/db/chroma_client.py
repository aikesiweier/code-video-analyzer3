import chromadb
from chromadb.config import Settings

chroma_client = chromadb.PersistentClient(
    path="./data/chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

collection = chroma_client.get_or_create_collection(
    name="coding_behaviors",
    metadata={"hnsw:space": "cosine"}
)