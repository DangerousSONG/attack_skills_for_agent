# assessing-vector-and-embedding-weaknesses — 详细参考（由 SKILL.md 拆分）

# Query as tenant B; expect ONLY tenant_id == "B" results.
from qdrant_client.models import Filter, FieldCondition, MatchValue

vec = model.encode(["confidential salary information"])[0].tolist()
hits = client.search(
    collection_name="docs",
    query_vector=vec,
    limit=10,
    query_filter=Filter(must=[FieldCondition(key="tenant_id", match=MatchValue(value="B"))]),
)
leaked = [h for h in hits if h.payload.get("tenant_id") != "B"]
print("CROSS-TENANT LEAK" if leaked else "isolation OK", "->", len(leaked), "foreign rows")

# Critical test: repeat WITHOUT the filter to confirm the server, not the client,
# enforces isolation. If unfiltered queries return tenant A data, isolation is client-side only.
hits_nofilter = client.search(collection_name="docs", query_vector=vec, limit=10)
print("server-side isolation FAILS" if any(h.payload.get("tenant_id") != "B" for h in hits_nofilter) else "OK")
```

### Step 5: Knowledge-base poisoning (test collection only)

Insert a benign poisoned chunk crafted to be retrieved for many unrelated queries, then measure how often it appears in `top_k`.

```python
from qdrant_client.models import PointStruct

# Benign marker payload (no real injection) to measure retrieval dominance.
poison = "POISON-CANARY. " + " ".join(
    ["password reset billing refund account login support error help"] * 8
)
client.upsert("docs_test", points=[
    PointStruct(id=999999, vector=model.encode([poison])[0].tolist(),
                payload={"tenant_id": "B", "source": "poison-test"})
])

queries = ["how do I get a refund", "reset my password", "what is the weather"]
for q in queries:
    hits = client.search("docs_test", model.encode([q])[0].tolist(), limit=5)
    dominated = any(h.payload.get("source") == "poison-test" for h in hits)
    print(f"{'POISON in top5' if dominated else 'clean'}: {q}")
```

### Step 6: Detect indirect prompt injection in retrieved chunks

Scan retrieved chunk text for injection markers before it is concatenated into the prompt.

```python
import re
INJECTION_PATTERNS = [
    r"ignore (all|previous|the above) instructions",
    r"system prompt", r"you are now", r"disregard", r"</?(system|instructions)>",
]
def chunk_is_injection(text):
    low = text.lower()
    return [p for p in INJECTION_PATTERNS if re.search(p, low)]

for hit in client.search("docs", model.encode(["help"])[0].tolist(), limit=10):
    flags = chunk_is_injection(hit.payload.get("text", ""))
    if flags:
        print("INDIRECT INJECTION in chunk", hit.id, flags)
```

### Step 7: Report and remediate

- **Inversion/membership:** rate-limit and authenticate the embedding endpoint; avoid returning raw similarity scores; restrict who can query embeddings.
- **Cross-tenant:** enforce tenant filters server-side (separate collections/namespaces per tenant where feasible); never rely on client-supplied filters.
- **Poisoning:** validate and provenance-tag every ingested chunk; scan inputs for injection; cap any single source's share of retrieval.
- **Indirect injection:** sanitize retrieved chunks and apply output guardrails (see `defending-llms-with-guardrails`).

## Tools and Resources

| Tool | Purpose | Primary Source |
|------|---------|----------------|
| OWASP LLM08 | Vector and Embedding Weaknesses guidance | https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ |
| sentence-transformers | Embedding generation for testing | https://www.sbert.net/ |
| Qdrant client | Vector store + filtered search | https://qdrant.tech/documentation/ |
| Chroma / Weaviate / Pinecone | Alternative vector stores | https://docs.trychroma.com/ |
| vec2text | Embedding-inversion research baseline | https://github.com/jxmorris12/vec2text |
| MITRE ATLAS | AML.T0024 Exfiltration via ML Inference API | https://atlas.mitre.org/ |

## Validation Criteria

- [ ] RAG pipeline inventoried (embedding model, store, tenancy, metric, top_k, filters).
- [ ] Embedding-inversion exposure measured and rated.
- [ ] Membership-inference delta computed for in-corpus vs control items.
- [ ] Multi-tenant isolation tested both with and without client filters (server-side enforcement confirmed).
- [ ] Poisoning dominance measured in a test collection only.
- [ ] Retrieved chunks scanned for indirect-injection content.
- [ ] Findings reported with remediation for each weakness class.
- [ ] No production corpus modified during the assessment.
