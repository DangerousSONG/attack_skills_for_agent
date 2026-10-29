---
name: testing-prompt-injection-in-rag-pipelines
description: "Probes RAG pipelines for indirect prompt injection. Signals: supply chain, CI/CD, pipeline attack."
zh-signals: "Probes Retrieval-Augmented Generation pipelines for indirect prompt injection 信号:供应链,cicd,流水线攻击。"
when-to-use: Probes Retrieval-Augmented Generation pipelines for indirect prompt injection
  via poisoned retrieved documents and embedding-space manipulation, using NVIDIA garak,
  Promptfoo red-team plugins, and Microsoft PyRIT against vector stores like FAISS,
  Chroma, Pinecone, or pgvector. Use when security-testing a RAG chatbot or document-Q&A
  system, validating retrieval guardrails, or gating CI/CD on prompt-template/retriever changes.
domain: cybersecurity
subdomain: ai-security
tags:
- ai-security
- prompt-injection
- rag
- llm-red-teaming
- garak
- promptfoo
- pyrit
- owasp-llm
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
atlas_techniques:
- AML.T0051
---
# Testing Prompt Injection in RAG Pipelines

> **Authorized-use-only notice:** This skill describes offensive testing techniques against Retrieval-Augmented Generation (RAG) systems. Run these probes only against applications you own or have explicit written authorization to test. Adversarial inputs that exfiltrate documents or hijack a model can cause real harm to production systems and downstream users. Always test in a non-production environment first and follow your engagement rules of engagement (RoE).

## Overview

Retrieval-Augmented Generation (RAG) pipelines combine a large language model (LLM) with a retrieval layer (a vector store such as FAISS, Chroma, Pinecone, Milvus, or pgvector) so the model can answer questions over private documents. The retrieval layer is an *injection surface*: any text that the retriever returns is concatenated into the model's context window and is treated by the model as authoritative. An attacker who can influence the document corpus (a poisoned PDF, a malicious wiki edit, a planted support ticket, a crafted email) can plant instructions that the model will follow when that chunk is retrieved. This is **indirect prompt injection** delivered through the retrieval channel, and it maps to MITRE ATLAS **AML.T0051 (LLM Prompt Injection)** and OWASP **LLM01:2025 Prompt Injection**.

Beyond text-level injection, RAG pipelines are vulnerable at the *embedding* layer. An attacker who understands the embedding model can craft text that lands near high-value queries in vector space ("embedding manipulation" / retrieval poisoning), guaranteeing that the malicious chunk is retrieved for a target query even when it is not semantically relevant to a human. This skill walks through systematically probing both surfaces using NVIDIA **garak**, **Promptfoo** red-team plugins, and Microsoft **PyRIT**, with verified, runnable commands from each tool's documentation.

## When to Use

- When security-testing a RAG chatbot, internal knowledge assistant, or document-Q&A product before or after release.
- When validating that retrieval guardrails (input/output filtering, context sandboxing) actually block injected instructions.
- During an AI red-team engagement scoped to test the LLM application layer (OWASP LLM Top 10 coverage).
- When you ingest user-controllable or third-party content into a vector store and need to prove the blast radius of a poisoned document.
- As a regression gate in CI/CD: re-run the probe suite on every prompt-template or retriever change.

## Prerequisites

- Python 3.10-3.13 and a virtual environment.
- Network access to the target RAG application (HTTP API, or a local harness you control).
- Authorization / signed RoE for the target.
- Install the tooling:

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# NVIDIA garak — LLM vulnerability scanner
python -m pip install -U garak

# Microsoft PyRIT — Python Risk Identification Tool (Python 3.10-3.13)
pip install pyrit

# Promptfoo — declarative red-team / eval CLI (Node.js 18+)
npm install -g promptfoo
# or run ad hoc with: npx promptfoo@latest
```

- For local embedding-poisoning experiments: `pip install sentence-transformers faiss-cpu numpy`.

## Objectives

- Enumerate the retrieval surface of the target RAG pipeline and identify where untrusted content enters the corpus.
- Run automated injection probes with garak (`promptinject`, `latentinjection`, `leakreplay`) and capture pass/fail rates.
- Author Promptfoo red-team configs using the `indirect-prompt-injection` and `rag-document-exfiltration` plugins.
- Drive multi-turn injection campaigns with PyRIT orchestrators against the target endpoint.
- Demonstrate embedding-space retrieval poisoning so a benign-looking query reliably retrieves an attacker chunk.
- Produce evidence (transcripts, retrieved chunks, scorer output) and map each finding to OWASP LLM01 and ATLAS AML.T0051.

## MITRE ATT&CK Mapping

This skill is anchored in MITRE ATLAS (the AI-specific companion to ATT&CK). Names below are the official ATLAS technique names.

| ID | Official Name | Relevance |
|----|---------------|-----------|
| AML.T0051 | LLM Prompt Injection | Core technique — instructions injected via retrieved context override system intent |
| AML.T0051.001 | LLM Prompt Injection: Indirect | Injection delivered through documents the RAG retriever ingests, not direct user input |
| AML.T0057 | LLM Data Leakage | Goal of many RAG injections — exfiltrate other tenants' or system documents |
| AML.T0024 | Exfiltration via ML Inference API | Document exfiltration channel through model responses |

## Workflow

### 1. Map the retrieval surface
Identify every path by which content reaches the vector store, and confirm the target endpoint contract. Capture a baseline benign request.

```bash
# Baseline request to the RAG chat endpoint (adjust to the target's API)
curl -s -X POST https://target.example.com/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RAG_API_TOKEN" \
  -d '{"message":"Summarize the onboarding policy.","session":"recon-1"}' | jq .
```

### 2. Run garak prompt-injection probes against the target
garak ships dedicated probes for prompt injection. `promptinject` implements the Agency Enterprise PromptInject framework; `latentinjection` covers injection planted in retrieved/latent context; `leakreplay` tests for verbatim training/context leakage.

```bash
# List available probes to confirm module names on your installed version
python -m garak --list_probes | grep -E "promptinject|latentinjection|leakreplay|xss"

# Run injection + latent-injection + leak probes against an OpenAI-compatible target
export OPENAI_API_KEY="sk-..."
python -m garak \
  --model_type openai \
  --model_name gpt-4o-mini \
  --probes promptinject,latentinjection,leakreplay \
  --generations 5 \
  --report_prefix rag_injection_run

# Target a REST endpoint you control via garak's rest generator
python -m garak \
  --model_type rest \
  --generator_option_file rest_target.json \
  --probes latentinjection
```

A minimal `rest_target.json` for garak's REST generator (maps the request/response to the target API):

```json
{
  "rest": {
    "RestGenerator": {
      "uri": "https://target.example.com/api/chat",
      "method": "post",
      "headers": {"Authorization": "Bearer $RAG_API_TOKEN", "Content-Type": "application/json"},
      "req_template_json_object": {"message": "$INPUT", "session": "garak"},
      "response_json": true,
      "response_json_field": "answer"
    }
  }
}
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
