from embedding_pipeline import TerrierGPTCache

# Initialize cache
cache = TerrierGPTCache(similarity_threshold=0.75)

print("=" * 60)
print("STEP 2: Embedding Pipeline Test")
print("=" * 60)

# Test 1: Cache a response
print("\n[Test 1] Caching a response...")
query_1 = "Where is the sustainability office at BU?"
response_1 = "The Office of Sustainability is located at 685 Commonwealth Ave"
doc_id = cache.cache_response(query_1, response_1, metadata={"source": "FAQ"})
print(f"✅ Cached: {doc_id}")

# Test 2: Query with identical text (should match)
print("\n[Test 2] Query with IDENTICAL text (should match)...")
result = cache.query_cache("Where is the sustainability office at BU?")
if result:
    print(f"✅ Match found!")
    print(f"   Similarity: {result['similarity']:.6f}")
    print(f"   Response: {result['response']}")
else:
    print("❌ No match (unexpected)")

# Test 3: Query with similar but different text (should match if above threshold)
print("\n[Test 3] Query with SIMILAR text...")
result = cache.query_cache("Where can I find the sustainability office?")
if result:
    print(f"✅ Match found!")
    print(f"   Similarity: {result['similarity']:.6f}")
    print(f"   Response: {result['response']}")
else:
    print("❌ No match (below threshold or no results)")

# Test 4: Query with unrelated text (should NOT match)
print("\n[Test 4] Query with UNRELATED text (should NOT match)...")
result = cache.query_cache("What is the weather today?")
if result:
    print(f"⚠️  Unexpected match (similarity: {result['similarity']:.6f})")
else:
    print("✅ Correctly rejected (below threshold)")

# Test 5: Cache stats
print("\n[Test 5] Cache stats...")
stats = cache.get_cache_stats()
print(f"✅ Stats: {stats}")

print("\n" + "=" * 60)
print("STEP 2: All tests complete!")
print("=" * 60)
