---
name: ai-data-security
description: |
  AI system data security testing methodology. Triggered when you need to assess the data leakage risk of LLM/AI systems, training data security,
  or RAG/vector store data integrity. Covers: System Prompt leakage (meta prompt/role-play/keyword location),
  training data inference and extraction, membership inference attacks, model inversion attacks, RAG data poisoning, API information disclosure,
  cascading hallucination attacks, external data source information leakage.
zh-signals: "AI 系统数据安全测试方法论，覆盖提示泄露、训练数据提取、RAG 投毒等风险。信号:AI数据安全,数据泄露,训练数据提取,模型反演,RAG投毒"
when-to-use: >-
  Use when assessing data leakage risk in LLM or AI systems, including training
  data safety, RAG/vector store integrity, and prompt or API information exposure.
metadata:
  tags: ai data security, data leakage, prompt leakage, training data extraction, membership inference, model inversion, rag poisoning, data exfiltration, training data, membership inference, model inversion, data poisoning, api disclosure
  category: ai-security
---

# AI Data Security Testing Methodology

## Attack Surface Overview

| Layer | Attack Type | Target |
|------|---------|------|
| Application layer | System Prompt leakage, API information disclosure, PII theft | Configuration/interfaces/user data |
| Model layer | Training data inference, membership inference, model inversion | Training data/model parameters |
| Deployment layer | RAG poisoning, vector store broken access control, cache leakage | Knowledge base/infrastructure |

### Boundary with prompt-leak

`prompt-leak` focuses on the 6 categories of System Prompt leakage techniques (direct request, formatting, indirect inducement, reflection, side channel, multi-turn extraction). This skill treats prompt leakage as one of the application-layer attack surfaces and focuses on broader data security issues such as training data, the model layer, and RAG data pipelines. Call `prompt-leak` directly when you need to go deeper into prompt leakage.

---

## Phase 0: Data Asset Identification

Before testing, map out the data asset boundaries of the AI system:

- **Training data** — pretraining corpora, fine-tuning datasets, RLHF annotation data
- **RAG knowledge base** — document stores, vector databases, retrieval indexes
- **API endpoints** — inference interfaces, management interfaces, internal debug endpoints
- **Caches and logs** — conversation history, intermediate reasoning results, audit logs

## Phase 1: Application-Layer Data Leakage

- **System Prompt leakage** — see the `prompt-leak` skill, not expanded here
- **API information disclosure** — craft prompts that induce the model to output API endpoints, model versions, and parameter configurations; probe common endpoints such as `/v1/models`, `/debug`, `/health` for exposed internal information
- **Privacy data theft** — extract PII (names, phone numbers, email addresses) from the conversation context; assume business scenarios to make the model recite other users' interactions; pay attention to context isolation flaws in multi-tenant scenarios

## Phase 2: Model-Layer Data Attacks

- **Training data inference** — prefix completion: provide a plausible prefix of training data and let the model complete it ("My social security number is..."); divergence attacks: ask the model to repeat a word indefinitely — once the model deviates from the normal distribution it may spit out training samples
- **Membership inference attacks** — train a shadow model that mimics the target model's behavior; compare the output probability differences of the target model on "in-training" versus "out-of-training" data; high-confidence outputs usually mean the data appeared in the training set
- **Model inversion attacks** — in the white-box setting, recover input features from model outputs via gradient optimization; in the black-box setting, reconstruct the input distribution through large numbers of API queries (e.g. face reconstruction attacks)

## Phase 3: Data Poisoning and Tampering

- **RAG knowledge base poisoning** — inject malicious documents into public data sources and wait for the RAG system to index them so they influence retrieval results; manipulate embeddings so the malicious content is semantically close to high-frequency queries
- **Conversation corpus poisoning** — if the system fine-tunes on user feedback, inject specific conversation patterns to pollute the training set
- **Cascading hallucination attacks** — induce the model to generate incorrect information, triggering data-pipeline-level errors when downstream systems rely on that output

## Phase 4: Deployment-Layer Data Security

- **Unauthorized vector database access** — check the authentication configuration and network exposure of vector stores such as Milvus / Pinecone / Weaviate
- **Backup/log/cache leakage** — conversation history stored in plaintext, inference logs containing sensitive prompts, model snapshots stored unencrypted

---

## Detection Checklist

- [ ] Can the System Prompt be leaked by any method
- [ ] Do API endpoints expose model versions/parameters/internal configuration
- [ ] Does the model leak training data fragments in its output
- [ ] Is conversation context isolated in multi-tenant scenarios
- [ ] Can RAG data sources be poisoned externally
- [ ] Does the vector database have authentication and access control
- [ ] Do logs/caches contain sensitive data and remain unencrypted

## Further Reading

- Detailed technical steps and payloads for each attack type → [references/data-attack-techniques.md](references/data-attack-techniques.md)
