---
name: rfc9001-0rtt-replay-protection
description: Audit whether QUIC implementations enforce 0-RTT anti-replay protection per RFC 9001 §9.2 (MUST implement and use TLS 1.3 anti-replay) and §5.6 (application protocols MUST define a 0-RTT profile) — the same 0-RTT flight accepted twice by the same instance, or a non-idempotent request executed twice, is the replay attack surface (related quiche issue#2678 confirmed: 0-RTT exact-flight replay accepted twice, violating the RFC 8446 §8 at-most-once-per-instance MUST; anchor RFC 9114 §10.9 requires H3 to apply RFC 8470 anti-replay)
zh-signals: 审计 QUIC 实现 0-RTT 反重放保护是否按 RFC 9001 §9.2（必须实现并使用 TLS1.3 反重放）与 §5.6（应用协议必须定义 0-RTT profile）——同实例重复接受同一 0-RTT flight、非幂等请求被执行两次即重放攻击面（关联 quiche issue#2678 已确认：0-RTT exact-flight 重放被接受两次，违反 RFC 8446 §8 每实例至多一次 MUST；锚点 RFC 9114 §10.9 要求 H3 必须应用 RFC 8470 反重放）
rfc: RFC 9001 §9.2（Replay Attacks with 0-RTT）/ §5.6（0-RTT 使用限制）/ RFC 8446 §8（anti-replay at-most-once）/ RFC 9114 §10.9 + RFC 8470（H3 反重放义务）
license: Apache-2.0
---

# RFC 9001 §9.2 0-RTT Anti-Replay Protection Audit

## 1. Normative Clauses (Original Sources)

RFC 9001 §9.2 (original text):
> Endpoints MUST implement and use the replay protections described in [TLS13], however it is recognized that these protections are imperfect.

RFC 8446 §8 (cited by quiche issue#2678 as the judgment basis):
> The server MUST ensure that any instance of it ... would accept 0-RTT for the same 0-RTT handshake at most once. (At-most-once acceptance per server instance for the same 0-RTT handshake is MUST-level.)

RFC 9001 §5.6 (original text):
> An application protocol that uses QUIC MUST include a profile that defines acceptable use of 0-RTT; otherwise, 0-RTT can only be used to carry QUIC frames that do not carry application data.
> A client therefore MUST NOT use 0-RTT for application data unless specifically requested by the application that is in use.

RFC 9114 §10.9 (key point): HTTP/3 MUST use the HTTP Early Data anti-replay mitigation mechanism defined in RFC 8470 — i.e. the server MUST apply reject/buffer policy to non-idempotent requests in 0-RTT.

Core pattern in one sentence: **0-RTT trades "replayability" for "saving one RTT" — all keys come from an old ticket and the server has no cryptographic way to distinguish replay from the original. So the RFC splits responsibility into layers: the transport layer MUST provide anti-replay (§9.2), the application layer MUST define what may use 0-RTT (§5.6 profile), and HTTP/3 MUST implement RFC 8470 (§10.9). Miss any one layer, and a captured 0-RTT flight is a cheque that can be cashed repeatedly.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| ZR-1 | Capture the full Initial + 0-RTT flight (ticket included) and replay it verbatim twice on the **same server instance** | Both accepted and application data processed → violates the RFC 8446 §8 at-most-once-per-instance MUST (same as confirmed quiche#2678) |
| ZR-2 | Send a non-idempotent request in 0-RTT (POST / GET with side effects, e.g. GET /api/charge?amount=50) | Server executes it without RFC 8470 reject/buffer-until-handshake-confirmation → violates RFC 9114 §10.9 |
| ZR-3 | Check whether the target implements and enables TLS 1.3 anti-replay (single-use tickets / age window / PSK dedup table) | Ticket reusable across many connections with no dedup state → §9.2 mechanism missing |
| ZR-4 | Check whether the application protocol carried over QUIC has a 0-RTT profile (H3: RFC 8470 implementation; custom protocols: documentation) | No profile yet 0-RTT application data accepted → violates §5.6 |
| ZR-5 | Client behavior after 0-RTT rejection: is the data retried in 1-RTT? | Client not retrying is a client issue; server rejecting but still partially processing 0-RTT data before handshake completion → server violation |

Method: aioquic dual connections reusing the same ticket + byte-for-byte flight replay; application-layer observation (side-effect counters on non-idempotent endpoints).

## 3. Attack-Surface Hypotheses

- **Request replay**: ZR-1/ZR-2 — captured early data cashed repeatedly: duplicate orders, duplicate transfers, duplicate state changes (the classic "GET with side effects" pitfall family)
- **Cross-instance replay**: no shared anti-replay state among instances behind a load balancer → one ticket replays across the whole cluster (deployment-level amplification of ZR-3)
- **Denial of service**: floods of forged 0-RTT exhaust server PSK dedup tables and the early-data processing pipeline

## 4. Related Historical CVEs

| CVE / Evidence | Implementation | Root cause |
|---|---|---|
| **quiche issue#2678** (2026-08-31, Cloudflare quiche, Confirmed) | quiche | 0-RTT exact-flight replay accepted twice on two fresh connections sharing the same Config/TLS context — violates the TLS 1.3 per-instance anti-replay MUST; the issue cites RFC 9001 §9.2 + RFC 8446 §8 as the normative basis |
| TLS 1.3 0-RTT replay research family | Generic | The structural weakness of 0-RTT (no cryptographic replay distinction) has been explicit since RFC 8446; all mitigation lives in the mechanism layer (single-use ticket / freshness window / dedup table) — a missing mechanism means running naked |
| RFC 8470 violation pattern | HTTP stacks | H3 endpoints that do not implement "reject or buffer non-idempotent early data" wrongly push idempotency responsibility onto the client |

## 5. Differential Verification

Control group: fixed quiche with anti-replay enabled / nginx with single-use tickets + age window (OpenSSL 3.5.1+ ssl_early_data).
Comparison fields: ZR-1 second-acceptance verdict, ZR-2 non-idempotent rejection rate, ZR-3 ticket reuse count, ZR-4 profile documentation existence.
False-positive exclusion: replay across **different** server instances falls within the RFC-acknowledged "imperfect protection" scope — mark as known residual risk, not a violation; judge only same-instance double-acceptance and complete mechanism absence.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `tlsfuzzer-fuzz` (TLS early data / resumption replay tests), `fuzzowski-network-fuzz` (flight replay and variant fuzz)
- Tool layer (with what): aioquic (ticket export + flight capture/replay), curl (--tlsv1.3 early-data variants), application side-effect counter scripts (ZR-2 verdict)
- Post-hit actions: confirm same-instance replay → locate the missing dedup state (ticket reuse / PSK table) → forensics on ZR-2 non-idempotent execution (side-effect logs) → output the "replay window" measurement (ticket lifetime × instance count)
