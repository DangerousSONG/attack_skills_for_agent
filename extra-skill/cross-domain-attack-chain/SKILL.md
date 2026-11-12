---
name: cross-domain-attack-chain
description: |
  Cross-domain attack chain methodology for Web and AI. Trigger when the target system contains both traditional web applications and AI/LLM components,
  and you need to assess how Web vulnerabilities affect the AI system or how AI vulnerabilities affect the Web system.
  Covers bidirectional attack chains: Web→AI (XSS conversation theft/SSRF to model APIs/SQLi RAG poisoning/file upload RAG poisoning)
  and AI→Web (injection-generated stored XSS/Agent SQL command execution/tool-based sensitive file reads/sandbox escape RCE).
zh-signals: "串联 Web 与 AI 组件的双向攻击链，将两个领域的低危漏洞组合为高危影响。信号:跨域攻击,Web安全,AI安全,攻击链,RAG投毒"
when-to-use: "Use when a target combines traditional web applications with AI/LLM components and you need to assess Web-to-AI or AI-to-Web attack chains such as prompt injection, RAG poisoning, or sandbox escape."
metadata:
  tags: cross domain, web to ai, ai to web, attack chain, rag poisoning, xss ai, ssrf model api, agent sql injection, sandbox escape
  category: ai-security
---

# Web/AI Cross-Domain Attack Chain Methodology

## Overview

In modern systems, web services and AI/LLM components share data pipelines and infrastructure. A low-severity web-layer flaw (such as a restricted SSRF) can be upgraded to prompt injection once it reaches internal model APIs; conversely, prompt injection that writes back to the database through the Agent toolchain can produce stored XSS. The value of cross-domain attack chains lies in chaining "medium/low severity" issues from both domains into "high/critical severity" outcomes.

## Overview of Cross-Domain Attack Paths

| Direction | ID | Entry vulnerability | Cross-domain pivot | Final impact |
|------|------|----------|----------|----------|
| Web→AI | W2A-1 | XSS | hijack the AI conversation endpoint | steal conversation content/inject malicious context |
| Web→AI | W2A-2 | SSRF | reach internal model APIs | obtain embeddings/directly execute prompts |
| Web→AI | W2A-3 | SQLi | modify vector store records | poison RAG retrieval results |
| Web→AI | W2A-4 | file upload | upload documents with hidden instructions | RAG poisoning/indirect injection |
| Web→AI | W2A-5 | broken access control | unauthenticated admin endpoints | tamper with the System Prompt/model configuration |
| AI→Web | A2W-1 | Prompt injection | model output not escaped | generate stored XSS payloads |
| AI→Web | A2W-2 | Agent hijacking | SQL/command tools | execute arbitrary SQL queries or system commands |
| AI→Web | A2W-3 | tool abuse | file read tools | read sensitive server files |
| AI→Web | A2W-4 | code execution | sandbox escape | reverse shell/RCE |
| AI→Web | A2W-5 | MCP poisoning | external callback tools | data exfiltration to the attacker server |

## Phase 0: Attack Surface Mapping

- Identify all interaction points between the web and AI components in the system: RAG data sources (databases, file storage, CMS), model API endpoints, shared caches/queues
- Draw a data flow diagram marking which web user inputs eventually reach the LLM context (directly or through RAG retrieval)
- Confirm the paths where AI output is written back to the web layer: whether it is rendered directly onto pages, stored in the database, or triggers backend actions

## Phase 1: Web→AI Attack Paths

**1.1 XSS → steal AI conversations/inject context**
Use XSS to hijack the user's WebSocket or API session with the AI, then steal the conversation history or inject malicious context (GAARM.0040.001). The key is whether the AI chat interface renders Markdown/HTML img tags as real requests, so that session content leaks through `img src`.

**1.2 SSRF → call internal model APIs**
If the web-layer SSRF can reach internal model endpoints, it can directly send prompt requests, obtain embeddings, or modify parameters. The Agent's own network access capability may also become an SSRF pivot (GAARM.0041.001).

**1.3 SQLi → poison the RAG vector store**
When the RAG system stores document chunks or metadata in a relational database, SQL injection can modify retrieved content, indirectly injecting malicious instructions into the LLM context and achieving persistent indirect prompt injection.

**1.4 File upload → RAG poisoning**
Upload documents containing hidden instructions (white text in PDFs, hidden paragraphs in DOCX, text in image EXIF); once the document is indexed by the RAG pipeline, the hidden instructions are injected into the model context at retrieval time.

**1.5 Broken access control → modify the System Prompt/model configuration**
If admin endpoints lack authentication or suffer from IDOR, an attacker can directly modify the System Prompt, adjust model temperature parameters, and switch the underlying model version, fundamentally changing the AI's behavioral boundaries.

## Phase 2: AI→Web Attack Paths

**2.1 Prompt injection → generate stored XSS**
Trick the model into generating HTML fragments containing `<script>` or event handlers; if the web layer does not apply output encoding to AI output, the payload is stored and executes when other users browse the page.

**2.2 Agent hijacking → execute SQL/system commands**
Use indirect injection to hijack the Agent's objectives, making it call database query tools to execute `DROP TABLE` or call shell tools to run system commands (GAARM.0041.002), directly impacting the web backend infrastructure.

**2.3 Tool abuse → read sensitive files**
Hijack the Agent's filesystem tools to read server-sensitive files such as `.env`, database credentials, and TLS private keys, then exfiltrate the content through conversation output or a callback mechanism.

**2.4 Sandbox escape → reverse shell**
If a code-executing Agent has insufficient sandbox isolation, prompt injection can induce generation and execution of an escape payload, gaining shell access on the host and completing the penetration from the AI layer to the infrastructure layer.

**2.5 MCP poisoning → data exfiltration**
Poison the tool descriptions of a malicious MCP Server so that the Agent, while calling legitimate tools, also performs a data exfiltration action, sending user conversations or internal data to the attacker server via an HTTP callback.

## Attack Chain Combination Decisions

| Available entry point | Recommended combination path | Expected severity |
|----------|-------------|-----------|
| XSS + AI chat interface | W2A-1 → steal conversations → extract internal information | High |
| SSRF + internal model endpoint | W2A-2 → direct prompt → information disclosure/follow-on injection | Critical |
| File upload + RAG pipeline | W2A-4 → RAG poisoning → A2W-1 stored XSS | Critical |
| SQLi + vector store | W2A-3 → persistent injection → A2W-2 Agent command execution | Critical |
| Prompt injection + Agent tools | A2W-2/A2W-3 → read credentials → lateral movement | Critical |
| Third-party MCP Server | A2W-5 → data exfiltration + A2W-2 command execution | High |

## Detection Checklist

```
1. [ ] Have all interaction points between web and AI components been fully mapped? Are data flow directions marked?
2. [ ] Is there an injection point on the path from web user input to the LLM context?
3. [ ] Is output encoding and sanitization applied when AI output is written back to the web layer?
4. [ ] Are RAG data sources (database/file storage) access-controlled for writes?
5. [ ] Are internal model APIs restricted by network source?
6. [ ] Do Agent tool calls have parameter validation and permission isolation?
7. [ ] Does the file upload to RAG indexing pipeline detect hidden instructions?
8. [ ] Are cross-domain attack chain combination paths included in threat modeling?
```
