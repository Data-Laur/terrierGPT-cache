from embedding_pipeline import TerrierGPTCache

cache = TerrierGPTCache(similarity_threshold=0.75)

# Cache the original query
query_1 = "Where is the sustainability office at BU?"
response_1 = "The Office of Sustainability is located at 685 Commonwealth Ave"
cache.cache_response(query_1, response_1, metadata={"source": "FAQ"})

# Query with paraphrase
paraphrase = "Where can I find the sustainability office?"

results = cache.collection.query(
    query_texts=[paraphrase],
    n_results=1
)

distance = results["distances"][0][0]
similarity = 1 - distance

print(f"Query: {paraphrase}")
print(f"Distance: {distance}")
print(f"Similarity: {similarity:.6f}")
print(f"Threshold: {cache.threshold}")
print(f"Match? {similarity >= cache.threshold}")
