## Building an AI-Aware Campus: Using TerrierGPT for a More Sustainable Grid

Boston University Campus Climate Lab · Summer–Fall 2026

## What We're Building
A framework to measure, reduce, and communicate the environmental 
footprint of TerrierGPT — BU's campus AI chatbot platform running 
on Amazon Bedrock (Claude Sonnet + Haiku models).

## The Three Tracks
- **Quantification**: Real AWS Scope 2 carbon data + EPA eGRID methodology 
  to calculate energy, water, and CO₂ per query by model (Jan–May 2026)
- **Reduction**: Vector database response caching system to eliminate 
  redundant queries — piloting with Earth House (~20 students, Sept 2026)
- **Communication**: Power BI dashboard modeled on URI's "How Hungry is AI?" - student education on model selection (Haiku = ~half the CO₂ of Sonnet)

  ## Tech Stack
## Tech Stack
- **Python** — core language for vector DB build
- **ChromaDB** — vector database for response caching
- **sentence-transformers + PyTorch** — query embedding (all-MiniLM-L6-v2)
- **AWS Bedrock** — TerrierGPT AI inference (Claude Sonnet 4.6, Haiku 4.5)
- **Power BI + Power Query** — sustainability dashboard + data pipeline
- **EPA eGRID + AWS Scope 2 LBM** — carbon quantification methodology
- **MGHPCC RHOAI** — deployment target (Red Hat OpenShift AI sandbox)
- **GitHub** — version control

## Key Finding So Far
Switching students from Sonnet to Haiku for simple tasks could reduce 
TerrierGPT's carbon emissions by ~30–50% with zero infrastructure changes.

## Team
Lauren — Data engineering, dashboard, vector DB, calculations
Kiko Yoshihira — Survey design, policy, AWS liaison  
Dakota Wang — Computer engineering, RHOAI prototype
Professor Nathan Phillips — Faculty advisor, ISO New England, MGHPCC board

## Goal
Reduce carbon emissions of TerrierGPT LLM queries
Create awareness about methods on how to utilize LLMs in a more sustainable way
Publish in Emerald Review or peer-reviewed policy journal.
Framework generalizable to any university running campus AI.

## Quick Start: Using the Cache

### Installation

```bash
python -m venv venv
source venv/bin/activate
pip install chromadb sentence-transformers
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

All tests should pass:
- ✅ Caching works
- ✅ Identical queries match (similarity 1.0)
- ✅ Paraphrases match (similarity ~0.83 at 0.75 threshold)
- ✅ Unrelated queries rejected
- ✅ Cache stats correct

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

## Privacy & Security Model

This is a **standalone prototype**, not integrated with live TerrierGPT production.

**Why standalone?**
- Professor John Byers (AIDA) identified cache timing attacks: even blinded queries leak info via response speed (cache hit = fast, cache miss = slow API call)
- BU IS&T will not approve systems inspecting live user queries directly
- Solution: prototype on MGHPCC RHOAI, test with Earth House pilot using consent-based query logging

**Deployment Plan:**
- July–August: Finalize spec, deploy to MGHPCC sandbox
- Sept 22–Oct 31: Earth House trial (20 students, real query data with consent)
cat README.md
cat > README.md << 'EOF'
## Building an AI-Aware Campus: Using TerrierGPT for a More Sustainable Grid

Boston University Campus Climate Lab · Summer–Fall 2026

## What We're Building

A framework to measure, reduce, and communicate the environmental 
footprint of TerrierGPT — BU's campus AI chatbot platform running 
on Amazon Bedrock (Claude Sonnet + Haiku models).

## The Three Tracks

- **Quantification**: Real AWS Scope 2 carbon data + EPA eGRID methodology 
  to calculate energy, water, and CO₂ per query by model (Jan–May 2026)
- **Reduction**: Vector database response caching system to eliminate 
  redundant queries — piloting with Earth House (~20 students, Sept 2026)
- **Communication**: Power BI dashboard modeled on URI's "How Hungry is AI?" - student education on model selection (Haiku = ~half the CO₂ of Sonnet)

## Tech Stack

- **Python** — core language for vector DB build
- **ChromaDB** — vector database for response caching
- **sentence-transformers** — query embedding (all-MiniLM-L6-v2)
- **AWS Bedrock** — TerrierGPT AI inference (Claude Sonnet 4.6, Haiku 4.5)
- **Power BI + Power Query** — sustainability dashboard + data pipeline
- **EPA eGRID + AWS Scope 2 LBM** — carbon quantification methodology
- **MGHPCC RHOAI** — deployment target (Red Hat OpenShift AI sandbox)
- **GitHub** — version control

## Quick Start: Using the Cache

### Installation

```bash
python -m venv venv
source venv/bin/activate
pip install chromadb sentence-transformers
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

## Team

Lauren — Data engineering, dashboard, vector DB, calculations
Kiko Yoshihira — Survey design, policy, AWS liaison  
Dakota Wang — Computer engineering, RHOAI prototype
Professor Nathan Phillips — Faculty advisor, ISO New England, MGHPCC board

## Goal

Reduce carbon emissions of TerrierGPT LLM queries
Create awareness about methods on how to utilize LLMs in a more sustainable way
Publish in Emerald Review or peer-reviewed policy journal.
Framework generalizable to any university running campus AI.
