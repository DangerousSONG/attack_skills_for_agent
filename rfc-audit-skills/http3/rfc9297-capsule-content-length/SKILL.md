---
name: rfc9297-capsule-content-length
description: Audit whether HTTP Datagrams / Capsule Protocol implementations strictly follow RFC 9297 §3.2/§3.3/§3.5 — capsule coexisting with Content-Length and other headers, truncated capsules, and unknown capsule-type handling errors are an HTTP-smuggling same-family attack surface (same family: an undisclosed sharing-session smuggling case, CVE-2025-64702 pattern)
zh-signals: 审计 HTTP Datagrams / Capsule Protocol 实现是否严格按 RFC 9297 §3.2/§3.3/§3.5——capsule 与 Content-Length 等头共存、截断 capsule、未知 capsule 类型处理错误即 HTTP 走私同族攻击面（同族：分享会未公开走私案例、CVE-2025-64702 模式）
rfc: RFC 9297 §2（HTTP Datagrams）/ §3.2（与 Content-Length 等头的互斥）/ §3.3（capsule 解析）/ §3.5（未知类型与中介行为）
license: Apache-2.0
---

# RFC 9297 §3 Capsule Protocol Mutual Exclusivity & Parsing Completeness Audit

## 1. Normative Clauses (Original Sources)

RFC 9297 §3.2 (original text, key points):
> The Capsule Protocol MUST NOT be used with messages that contain Content-Length, Content-Type, or Transfer-Encoding header fields.
> A receiver that observes a violation MUST treat the HTTP message as malformed.

(Under HTTP/3, Content-Length vs DATA-frame-length consistency is additionally governed by RFC 9114 §4.1.3; see `rfc9114-content-length-data-mismatch`.)

RFC 9297 §3.3: capsule length fields with redundant non-canonical varint encodings must be self-consistent (coexisting canonical + non-canonical encodings count as malformed); a truncated capsule on a clean FIN (declared length exceeding actually-arrived bytes) must be treated as malformed.

RFC 9297 §3.5: unknown capsule types must be **silently discarded** (skipped by declared length); an intermediary that does not recognize the Capsule-Protocol negotiation MUST NOT re-encode/convert between DATAGRAM frames and capsules; oversized capsules (theoretical limit 2^62-1) should be discarded without buffering by receivers.

RFC 9297 §2: HTTP Datagrams may only associate with requests/responses that explicitly declare support for them; datagrams appearing in a context without datagram association must, under HTTP/3, abort the stream with H3_DATAGRAM_ERROR (0x33).

Supplementary trap (common at implementation level): repeating the `Capsule-Protocol` header makes the field parse as a list and therefore be **treated as absent** — capability negotiation silently fails, entering a "declared supported but not negotiated" split state.

Core pattern in one sentence: **the capsule protocol layers "datagram semantics" on top of "byte-stream semantics"; the two length systems (in-capsule length vs outer Content-Length / stream end) need only fail to be mutually exclusive or self-consistent at one point to become the classic HTTP message-boundary-split smuggling.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| CP-1 | Send a response carrying both `Capsule-Protocol: ?1` and `Content-Length`; observe whether intermediaries and endpoints reject it as malformed | Either side accepts and keeps parsing → smuggling surface confirmed (same family as the undisclosed sharing-session case) |
| CP-2 | Send a capsule length in redundant non-canonical varint encoding (e.g. 0x40 0x2A for 42); observe whether it is treated as malformed | Accepting non-canonical encoding → parsing-split surface |
| CP-3 | Declare a capsule length then a clean FIN (actual bytes < declared length) | Not treated as malformed → truncation smuggling surface |
| CP-4 | Inject unknown capsule types (including an oversized length declaration of 2^62-1) | Not silently discarded but buffered/crashed → memory surface; an oversized value buffered is a DoS primitive |
| CP-5 | Send/receive DATAGRAM frames / capsules on a connection without Capsule-Protocol negotiation | Stream not aborted / not discarded → association violation |
| CP-6 | Repeat the Capsule-Protocol header and observe negotiation state | Negotiation silently fails while the data plane continues → split state |

Method: aioquic custom peer constructing capsule byte streams; h3i constructing malformed H3 messages; compare verdict differences between the two parsers (e.g. proxy vs origin) on the same malformed message.

## 3. Attack-Surface Hypotheses

- **HTTP smuggling (message-boundary split)**: CP-1/CP-3 — the frontend splits by Content-Length while the backend splits by capsule boundary; injected requests/responses interpreted under different boundaries, isomorphic to CL.TE smuggling
- **Cache poisoning**: hidden semantics smuggled out can be injected into shared-cache response-parsing paths
- **Memory exhaustion**: CP-4 — an oversized capsule length gets buffered waiting to be filled; a single connection can exhaust memory
- **Downgrade attack via failed capability negotiation**: CP-6 — inject datagram semantics after entering an undefined negotiation state

## 4. Related Historical CVEs

| CVE / Case | Implementation | Root cause |
|---|---|---|
| Undisclosed sharing-session case (same family, Capsule-Protocol smuggling) | A gateway implementation | Frontend/backend parsing split when capsule coexists with Content-Length — isomorphic to this Skill's CP-1 verdict condition, validating the realism of this audit surface |
| **CVE-2025-64702** (same-family pattern reference) | quic-go QPACK state machine | Compression/encapsulation-layer state machine failed to enforce capacity constraints — same "unenforced accounting/boundary obligation in a layered-semantics layer" pattern |

Note: the Capsule Protocol was only standardized in 2022; implementations are immature and public CVEs are extremely rare — a high-priority audit surface of "new protocol + explicit MUSTs".

## 5. Differential Verification

Control group: quic-go, aioquic (two independent capsule implementations); nginx-quic / Cloudflare quiche if available.
Comparison fields: reject/accept/crash tri-state for CP-1~CP-6 individually; the verdict difference between a frontend proxy and a backend origin on the same malformed message (necessary and sufficient condition for smuggling).
False-positive exclusion: an implementation returning 400 on seeing Capsule-Protocol coexisting with Content-Length is compliant; flag only "accepts and parses" and "two parsers' verdicts split".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `smuggler-desync` (message-boundary-split methodology directly reusable), `http2smugl-desync` (HTTP/2→HTTP/3 downgrade chains), `fuzzowski-network-fuzz` (capsule byte-stream fuzz)
- Tool layer (with what): aioquic, h3i
- Post-hit actions: confirm frontend/backend verdict split → construct end-to-end smuggling sequences → assess cache-poisoning/request-hijacking feasibility
