---
name: rfc9114-qpack-decoded-size-limit
description: Audit whether HTTP/3 targets limit only the compressed QPACK frame length but not the decoded field-section size — no decoded-size limit means a compression-amplification memory-exhaustion attack surface (thousands-fold amplification per connection possible; related CVE-2025-64702/CVE-2026-40898 quic-go, CVE-2026-12523 quiche, CVE-2025-13945 Wireshark)
zh-signals: 审计 HTTP/3 目标是否只对 QPACK 压缩后帧长限长、而未对解压后字段区块限长——未限长即存在压缩放大内存耗尽攻击面（单连接可达数千倍放大；关联 CVE-2025-64702/CVE-2026-40898 quic-go、CVE-2026-12523 quiche、CVE-2025-13945 Wireshark）
rfc: RFC 9114 §4.1.1 + RFC 9204（QPACK）
license: Apache-2.0
---

# RFC 9114 §4.1.1 / RFC 9204 Decoded Field-Section Size Limit Audit (QPACK Compression Amplification)

## 1. Normative Clauses (Original Sources)

RFC 9114 §4.1.1: HTTP/3 implementations impose a limit on field-section size; exceeding it must abort with `H3_EXCESSIVE_LOAD`.

RFC 9204 (QPACK): dynamic tables let a small compressed payload decode into many large fields — **the limit must apply to the decoded field section, not the on-wire compressed frame**.

Root-cause pattern in one sentence: **limiting the on-wire frame length ≠ limiting the decoded content length**; compression ratios can reach hundreds to thousands-fold, exhausting memory with a single connection.

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| QS-1 | Send a HEADERS frame compressed to ≈1KB that decodes to ≈1~10MB (many unique field names / large values via QPACK dynamic-table compression) | Target process memory rises significantly without aborting the stream → violation; stream reset with H3_EXCESSIVE_LOAD → compliant |
| QS-2 | Same as QS-1, but place the large fields in the **trailer section** (HEADERS frame after DATA) | Trailers are a common blind spot (CVE-2026-40898 attack vector); judged separately |
| QS-3 | Observe the target's limit granularity: per-entry decode-and-check, or decode-everything-then-check | Decode-all-then-check is equally exhaustible under large payloads (the fixed quic-go 0.59.1 approach is per-entry decode + per-entry check) |

Method: h3i / aioquic to construct QPACK dynamic-table-compressed frames; observe target RSS / OOM behavior.

## 3. Attack-Surface Hypotheses

Unauthenticated remote DoS: a single connection forces the server to allocate large memory with small traffic (CWE-770), potentially taking down any downstream product relying on the library (Caddy / Traefik / cloudflared etc.). Symmetrically exists on the client side (malicious server attacks the client).

## 4. Related Historical CVEs (same pattern reproduced across implementations — the core value of this Skill)

| CVE | Implementation | Note |
|---|---|---|
| **CVE-2025-64702** | quic-go ≤0.56.0 | Header section: only the compressed frame was length-limited (`maxHeaderBytes` compared `hf.Length`); no decoded-size limit. Fixed in 0.57.0 |
| **CVE-2026-40898** | quic-go <0.59.1 | Same pattern in the trailer section. Fix: enforce the RFC 9114 decoded field-section limit on trailers too, per-entry decode + per-entry check |
| **CVE-2026-12523** | Cloudflare quiche <0.29.3 | Same pattern found in batch by FoxIO (public PoC, 2026-10) |
| **CVE-2025-13945** | Wireshark <4.6.2/4.4.12 | Same pattern (parser side) |
| Unfixed | Bun, h3 (Rust), aioquic | Still unpatched at FoxIO's report; Bun has a variant where a counter overflow drives CPU to 100% |

## 5. Differential Verification

Control group: quic-go 0.59.1 (compliant baseline), quiche 0.29.3.
Comparison fields: target memory delta under QS-1/QS-2, whether the stream is aborted and with which error code, amplification factor.
False-positive exclusion: a target declaring an extremely large field-section limit and working as documented is a configuration issue, not an implementation vulnerability — mark separately.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (protocol fuzzing framework), `slowhttptest-dos` (DoS verification approach; both in tool-skills/)
- Tool layer (with what): h3i, FoxIO QPACK PoC (public since 2026-10), aioquic
- Post-hit actions: report along the dependency chain (library → downstream products Caddy/Traefik/cloudflared/LiteSpeed), output amplification factor and impact assessment
