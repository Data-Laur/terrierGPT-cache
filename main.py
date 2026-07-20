"""
FastAPI app for TerrierGPT-cache with Prometheus metrics endpoint.
Integrates with the embedding-based cache and exposes metrics at /metrics.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from typing import Optional, Dict
import logging

from embedding_pipeline import TerrierGPTCache
from prometheus_metrics import get_metrics

# Initialize FastAPI app
app = FastAPI(
    title="TerrierGPT Cache",
    description="Embedding-based semantic caching system with Prometheus instrumentation",
    version="1.0.0"
)

# Initialize cache
cache = TerrierGPTCache(chroma_path="./chroma_db", similarity_threshold=0.75)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "cache_size": cache.get_cache_stats()["total_cached"]}


@app.post("/cache/store")
async def store_response(query: str, response: str, metadata: Optional[Dict] = None):
    """
    Store a query-response pair in the cache.
    
    Args:
        query: User query text
        response: Cached response text
        metadata: Optional metadata dict
        
    Returns:
        Document ID and confirmation
    """
    try:
        doc_id = cache.cache_response(query, response, metadata)
        logger.info(f"Stored response for query: {query[:50]}... (doc_id: {doc_id})")
        return {
            "doc_id": doc_id,
            "status": "cached",
            "message": "Response stored successfully"
        }
    except Exception as e:
        logger.error(f"Error storing response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cache/query")
async def query_response(q: str, model: str = "claude-3-sonnet"):
    """
    Query the cache for a semantically similar cached response.
    
    Args:
        q: Query string
        model: Model name for metrics tracking
        
    Returns:
        Cached response if match found above threshold, null otherwise
    """
    try:
        result = cache.query_cache(q, model=model)
        if result:
            logger.info(f"Cache hit for query: {q[:50]}...")
            return {
                "status": "hit",
                "response": result["response"],
                "similarity": result["similarity"],
                "metadata": result["metadata"]
            }
        else:
            logger.info(f"Cache miss for query: {q[:50]}...")
            return {
                "status": "miss",
                "response": None,
                "message": "No similar cached response found"
            }
    except Exception as e:
        logger.error(f"Error querying cache: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics."""
    stats = cache.get_cache_stats()
    return {
        "stats": stats,
        "message": "Cache statistics"
    }


@app.get("/metrics")
async def metrics():
    """
    Prometheus metrics endpoint.
    Exposes cache_hit_total, cache_miss_total, embedding_latency_seconds, 
    bedrock_calls_avoided_total, and cache_size_entries.
    """
    return Response(get_metrics(), media_type="text/plain; version=0.0.4")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)