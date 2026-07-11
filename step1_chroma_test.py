import chromadb

# Persistent client - stores data in ./chroma_db
client = chromadb.PersistentClient(path="./chroma_db")

# Cosine space is REQUIRED for the 0.87 similarity threshold
collection = client.get_or_create_collection(
    name="terriergpt_cache",
    metadata={"hnsw:space": "cosine"}
)

# Smoke test: add a doc, query it back
collection.upsert(
    ids=["test_001"],
    documents=["Where is the sustainability office at BU?"],
    metadatas=[{"cached_response": "685 Commonwealth Ave"}]
)

results = collection.query(
    query_texts=["Where is the sustainability office at BU?"],
    n_results=1
)

print("Collection count:", collection.count())
print("Query result:", results["documents"])
print("Distance (0 = identical):", results["distances"])
print("✅ ChromaDB working" if results["ids"][0] else "❌ Something failed")
