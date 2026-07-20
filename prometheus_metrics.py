"""
Prometheus metrics for terrierGPT-cache monitoring.
Instruments cache hits/misses, embedding latency, Bedrock API calls avoided, and cache size.
"""

from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from typing import Optional

# Create isolated registry for this module
REGISTRY = CollectorRegistry()

# Counters
cache_hit_total = Counter(
    name="cache_hit_total",
    documentation="Total number of cache hits",
    registry=REGISTRY
)

cache_miss_total = Counter(
    name="cache_miss_total",
    documentation="Total number of cache misses",
    registry=REGISTRY
)

bedrock_calls_avoided_total = Counter(
    name="bedrock_calls_avoided_total",
    documentation="Total number of Bedrock API calls avoided due to cache hits",
    labelnames=["model"],
    registry=REGISTRY
)

# Histogram
embedding_latency_seconds = Histogram(
    name="embedding_latency_seconds",
    documentation="Embedding generation latency in seconds",
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0),
    registry=REGISTRY
)

# Gauge
cache_size_entries = Gauge(
    name="cache_size_entries",
    documentation="Current number of entries in cache",
    registry=REGISTRY
)


def record_cache_hit(model: Optional[str] = None):
    """Record a cache hit event."""
    cache_hit_total.inc()
    if model:
        bedrock_calls_avoided_total.labels(model=model).inc()


def record_cache_miss():
    """Record a cache miss event."""
    cache_miss_total.inc()


def record_embedding_latency(duration_seconds: float):
    """Record embedding generation latency."""
    embedding_latency_seconds.observe(duration_seconds)


def update_cache_size(size: int):
    """Update current cache size."""
    cache_size_entries.set(size)


def get_metrics() -> bytes:
    """Return Prometheus-formatted metrics."""
    return generate_latest(REGISTRY)