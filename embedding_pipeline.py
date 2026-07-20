from sentence_transformers import SentenceTransformer
import chromadb
from typing import Optional, Dict, List
import time

# Import Prometheus metrics
from prometheus_metrics import (
    record_cache_hit,
    record_cache_miss,
    record_embedding_latency,
    update_cache_size
)

class TerrierGPTCache:
    """
    Embedding-based caching system for TerrierGPT.
    Stores and retrieves cached responses using semantic similarity.
    Instrumented with Prometheus metrics for monitoring.
    """
    def __init__(self, chroma_path: str = "./chroma_db", similarity_threshold: float = 0.75):
        """
        Initialize the cache with a ChromaDB persistent client and embedding model.
        Args:
            chroma_path: Directory to persist ChromaDB data
            similarity_threshold: Cosine similarity cutoff (0-1, higher = stricter match)
        """
        self.threshold = similarity_threshold
        self.client = chromadb.PersistentClient(path=chroma_path)
        
        # Get or create collection with cosine similarity
        self.collection = self.client.get_or_create_collection(
            name="terriergpt_cache",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load embedding model (all-MiniLM-L6-v2)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize cache size metric
        update_cache_size(self.collection.count())

    def cache_response(self, query: str, response: str, metadata: Optional[Dict] = None) -> str:
        """
        Store a query-response pair in the cache.
        Args:
            query: User query text
            response: Cached response text
            metadata: Optional dict with additional info (e.g., {"source": "FAQ"})
        Returns:
            Generated document ID
        """
        if metadata is None:
            metadata = {}
        # Generate a simple ID (in production, use UUID)
        doc_id = f"doc_{self.collection.count() + 1}"
        self.collection.upsert(
            ids=[doc_id],
            documents=[query],
            metadatas=[{**metadata, "cached_response": response}]
        )
        
        # Update cache size metric after insertion
        update_cache_size(self.collection.count())
        
        return doc_id

    def query_cache(self, query: str, model: str = "claude-3-sonnet") -> Optional[Dict]:
        """
        Query the cache for a similar cached response.
        Args:
            query: User query text
            model: Model name for metrics tracking (e.g., "claude-3-sonnet")
        Returns:
            Dict with keys: 'response', 'similarity', 'metadata' if match above threshold,
            None if no match found
        """
        # ===== EMBEDDING LATENCY INSTRUMENTATION =====
        start_time = time.time()
        results = self.collection.query(
            query_texts=[query],
            n_results=1
        )
        embedding_time = time.time() - start_time
        record_embedding_latency(embedding_time)
        
        # No results in collection
        if not results["ids"] or not results["ids"][0]:
            # ===== CACHE MISS =====
            record_cache_miss()
            return None
        
        # Extract similarity (convert distance to similarity: similarity = 1 - distance)
        distance = results["distances"][0][0]
        similarity = 1 - distance
        
        # Check against threshold
        if similarity < self.threshold:
            # ===== CACHE MISS (below threshold) =====
            record_cache_miss()
            return None
        
        # ===== CACHE HIT =====
        record_cache_hit(model=model)
        
        # Return the cached response
        cached_response = results["metadatas"][0][0].get("cached_response")
        return {
            "response": cached_response,
            "similarity": similarity,
            "metadata": results["metadatas"][0][0]
        }

    def get_cache_stats(self) -> Dict:
        """Return basic stats about the cache."""
        return {
            "total_cached": self.collection.count(),
            "threshold": self.threshold,
            "model": "all-MiniLM-L6-v2"
        }