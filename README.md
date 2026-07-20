## Building an AI-Aware Campus: Using TerrierGPT for a More Sustainable Grid

Boston University Campus Climate Lab · Summer–Fall 2026

## What We're Building

A framework to measure, reduce, and communicate the environmental 
footprint of TerrierGPT — BU's campus AI chatbot platform running 
on Amazon Bedrock (Claude Sonnet + Haiku models).

## The Four Reduction Tracks

- **Response Caching** *(this repo)*: Vector database semantic cache to eliminate redundant Bedrock queries — piloting with Earth House (~20 students, Sept 2026)
- **Local LLM Inference** *(→ [terrierGPT-ollama-harness](https://github.com/Data-Laur/terrierGPT-ollama-harness) — coming soon)*: Ollama + Pi agent harness to produce the first quantified local-vs-cloud AI energy comparison for a university campus (laptop → MGHPCC → AWS Bedrock three-way comparison)
- **Model Selection Optimization**: Student education on model switching — Haiku = ~half the CO₂ of Sonnet for simple queries, zero infrastructure changes required
- **Quantification Baseline**: Real AWS Scope 2 LBM carbon data + EPA eGRID methodology to calculate energy, water, and CO₂ per query by model (Jan–May 2026)

## Tech Stack

**Core**
- **Python 3.9** — core language
- **ChromaDB** — vector database for semantic response caching
- **sentence-transformers** — query embedding (all-MiniLM-L6-v2, 384-dim)
- **PyTorch** — embedding model inference

**API & Deployment**
- **FastAPI** — REST API for cache operations
- **uvicorn** — ASGI server
- **AWS Bedrock** — TerrierGPT AI inference (Claude Sonnet 4.6, Haiku 4.5)

**Monitoring & Observability**
- **Prometheus** — metrics collection and monitoring
- **prometheus_client** — instrumentation (cache hit/miss, embedding latency, cache size)

**Analytics & Reporting**
- **Power BI + Power Query** — sustainability dashboard + data pipeline
- **EPA eGRID + AWS Scope 2 LBM** — carbon quantification methodology

**Infrastructure**
- **MGHPCC RHOAI** — deployment target (Red Hat OpenShift AI sandbox)
- **KServe** — model serving on OpenShift AI (InferenceService + HPA)
- **Ansible** — infrastructure provisioning (systemd service, Prometheus config)
- **GitHub** — version control

## Companion Projects

| Repo | Track | Status |
|------|-------|--------|
| [terrierGPT-cache](https://github.com/Data-Laur/terrierGPT-cache) | Response caching (this repo) | ✅ Active |
| [terrierGPT-ollama-harness](https://github.com/Data-Laur/terrierGPT-ollama-harness) | Local LLM inference (Ollama + Pi) | 🔜 Coming soon |

## Quick Start: Using the Cache

### Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt
```

### Python API (for integration)

```python
from embedding_pipeline import TerrierGPTCache

cache = TerrierGPTCache(similarity_threshold=0.75)

# Cache a response
cache.cache_response(
    query="Where is the sustainability office?",
    response="685 Commonwealth Ave",
    metadata={"source": "FAQ"}
)

# Query the cache
result = cache.query_cache("Where can I find the sustainability office?")
if result:
    print(f"Cache hit! Similarity: {result['similarity']:.3f}")
    print(f"Response: {result['response']}")
```

### FastAPI Server

```bash
python main.py
```

Server runs at `http://localhost:8000`

#### Endpoints

- `GET /health` — Health check
- `POST /cache/store?query=...&response=...` — Store cached response
- `GET /cache/query?q=...` — Query cache
- `GET /cache/stats` — Cache statistics
- `GET /metrics` — Prometheus metrics (cache hits, misses, latency)

#### Example: Query Cache via API

```bash
curl "http://localhost:8000/cache/query?q=Where%20is%20the%20sustainability%20office"
```

Response:
```json
{
  "status": "hit",
  "response": "685 Commonwealth Ave",
  "similarity": 0.92,
  "metadata": {"source": "FAQ"}
}
```

#### Prometheus Metrics

```bash
curl http://localhost:8000/metrics
```

Metrics exposed:
- `cache_hit_total` — Total cache hits
- `cache_miss_total` — Total cache misses
- `embedding_latency_seconds` — Query embedding latency (histogram)
- `bedrock_calls_avoided_total` — Bedrock API calls avoided via cache
- `cache_size_entries` — Current cache size

### Command Line (for testing)

```bash
# Cache a response
python cache_cli.py cache \
  --query "Where is the sustainability office?" \
  --response "685 Commonwealth Ave" \
  --source "FAQ"

# Query the cache
python cache_cli.py query --query "Where can I find the sustainability office?"

# Show stats
python cache_cli.py stats
```

### Testing

```bash
python test_step2_embedding.py
```

Expected results:
- ✅ Caching works
- ✅ Identical queries match (similarity 1.0)
- ✅ Paraphrases match (similarity ~0.83 at 0.75 threshold)
- ✅ Unrelated queries rejected
- ✅ Cache stats correct
- ✅ Prometheus metrics recorded

## Key Finding So Far

Switching students from Sonnet to Haiku for simple tasks could reduce 
TerrierGPT's carbon emissions by ~30–50% with zero infrastructure changes.

## Design Decisions

**Similarity Threshold (0.75):**
- Tuned empirically from test results
- Catches legitimate paraphrases ("Where can I find..." vs "Where is...")
- Rejects unrelated queries
- Lower = more cache hits but more false positives; higher = fewer hits but better precision

**Embedding Model (all-MiniLM-L6-v2):**
- 384-dimensional vectors, optimized for semantic search
- ~33M parameters, fast CPU inference
- Normalized output: cosine similarity is the natural distance metric

**Persistent Storage (ChromaDB):**
- Local disk storage in `./chroma_db/`
- Survives restarts, inspectable, no external dependencies
- Scales to millions of queries

**Metrics & Monitoring:**
- Prometheus instrumentation at cache operations (query, store, hit/miss)
- Embedding latency tracked via histogram with 0.01–5.0s buckets
- Cache size gauge updated on every operation
- Bedrock API calls avoided tracked by model

## Privacy & Security Model

This is a **standalone prototype**, not integrated with live TerrierGPT production.

**Why standalone?**
- Professor John Byers (AIDA) identified cache timing attacks: even blinded queries leak info via response speed (cache hit = fast, cache miss = slow API call)
- BU IS&T will not approve systems inspecting live user queries directly
- Solution: prototype on MGHPCC RHOAI, test with Earth House pilot using consent-based query logging

**Deployment Plan:**
- July–August: Finalize spec, deploy to MGHPCC sandbox
- Sept 22–Oct 31: Earth House trial (20 students, real query data with consent)
- Nov–Dec: Measure cache hit rate, energy savings, publish findings

## Deployment with Ansible

See `ansible/` directory for automated provisioning:

```bash
ansible-playbook -i ansible/hosts.ini ansible/provision.yml
```

This handles:
- System dependency installation
- Python venv setup
- Service deployment (systemd)
- Prometheus scrape configuration
- Health check verification

See `ansible/ANSIBLE_README.md` for details.

## Team

Lauren — Data engineering, dashboard, vector DB, calculations, Prometheus instrumentation
Kiko Yoshihira — Survey design, policy, AWS liaison  
Dakota Wang — Computer engineering, RHOAI prototype
Professor Nathan Phillips — Faculty advisor, ISO New England, MGHPCC board

## Goal

- Reduce carbon emissions of TerrierGPT LLM queries
- Create awareness about methods for utilizing LLMs sustainably
- Publish in Emerald Review or peer-reviewed policy journal
- Framework generalizable to any university running campus AI