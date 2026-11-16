---
name: rfc9000-handshake-done-timing
description: Audit QUIC server handling of HANDSHAKE_DONE frame send-timing and receipt processing per RFC 9000 §19.20 and RFC 9001 §4.9.2 — timing and key-discard-order errors can be triggered by a malicious server/peer into assertion crashes (related CVE-2025-59530 quic-go, observed in the wild)
zh-signals: 审计 QUIC 服务端对 HANDSHAKE_DONE 帧的发送时机与接收处理是否严格按 RFC 9000 §19.20 与 RFC 9001 §4.9.2——时序与密钥丢弃顺序错误可被恶意服务端/对端触发断言崩溃（关联 CVE-2025-59530 quic-go，野外已观测）
rfc: RFC 9000 §19.20（HANDSHAKE_DONE）/ RFC 9001 §4.9.2（密钥丢弃）
license: Apache-2.0
---

# RFC 9000 §19.20 HANDSHAKE_DONE Timing and Key-Discard Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §19.20 (verbatim):
> Servers MUST NOT send a HANDSHAKE_DONE frame before completing the handshake.
> A server MUST treat receipt of a HANDSHAKE_DONE frame as a connection error of type PROTOCOL_VIOLATION.

That is, two obligations: the **sender** (server role) must not send HANDSHAKE_DONE before the handshake completes; the **receiver** (server role) must terminate the connection with PROTOCOL_VIOLATION on receiving HANDSHAKE_DONE.

RFC 9001 §4.9.2: after handshake confirmation, Initial keys / Handshake keys must be discarded in the prescribed order; any "too early" or "missed" discard timing breaks the subsequent frame-decryption state machine.

Core pattern in one sentence: **HANDSHAKE_DONE is the only signal frame of "handshake confirmed"; its send timing and the key-discard order after receipt together form the resource lifecycle of the handshake period — either obligation loosened can be crashed remotely.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| HD-1 | As a malicious server, send HANDSHAKE_DONE early — before the handshake completes (client has not confirmed server-certificate verification / keys not ready) — and observe the peer client | Client enters assertion / NULL-pointer crash → violates the peer-side assumption of the §19.20 send obligation |
| HD-2 | As a client, send a HANDSHAKE_DONE frame to the server (a legitimate client must never send one) and observe the server | Server does not terminate with PROTOCOL_VIOLATION → violates the §19.20 receipt obligation |
| HD-3 | After receiving HANDSHAKE_DONE, verify whether the implementation **immediately** discards Initial keys (the quic-go CVE-2025-59530 fix) or only discards them when Handshake keys should be dropped | Discard order inconsistent with §4.9.2 → key-lifecycle vulnerability |
| HD-4 | Inject duplicate HANDSHAKE_DONE frames out of order during the handshake / interleaved with NewSessionTicket timing | State-machine deadlock or double-processing crash → violation |

Method: aioquic custom peer with precise control of HANDSHAKE_DONE send timing; quic-go debug logs to observe key-discard events.

## 3. Attack-Surface Hypotheses

- **Remote assertion crash (unauthenticated)**: HD-1 — a malicious server can crash any application using the client library during the handshake phase (the quic-go case was observed in the wild against Solana Firedancer)
- **Protocol-state confusion**: HD-2 — a client forges HANDSHAKE_DONE to push the server into a "handshake confirmed" state, skipping the handshake verification that should have continued
- **Key-lifecycle misalignment**: HD-3 — Initial keys surviving too long means a longer attack window for forged handshake-phase packets; discarding too early kills legitimate retransmissions (availability surface)

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2025-59530** (7.5 HIGH, CWE-617 Reachable Assertion) | quic-go < 0.49.0 / 0.54.1 / 0.55.0 | The client receives a HANDSHAKE_DONE sent early by the server before handshake confirmation, triggering an assertion crash; attacks observed in the wild. Fix PR #5354: discard Initial keys immediately on receiving HANDSHAKE_DONE, eliminating the assertion path under wrong timing |

Note: HD-2/HD-4 are blind-spot clauses with "constraints but no public CVE yet" — most implementations only fixed the crash path (HD-1) without verifying the receipt obligation and out-of-order timing; worth targeted auditing.

## 5. Differential Verification

Control group: quic-go ≥ 0.55.0 (patched), msquic / ngtcp2.
Comparison fields: HD-1 crash or not, HD-2 PROTOCOL_VIOLATION or not, HD-3 key-discard event timing, HD-4 out-of-order tolerance.
False-positive exclusion: an implementation choosing a more conservative "log and ignore instead of asserting immediately" strategy is compliant; only flag "reachable assertion / connection not terminated / wrong key order".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (handshake-phase frame-timing fuzzing), `grammarinator-gen-fuzz` (QUIC handshake frame-sequence grammar generation; both in tool-skills/)
- Tool layer (what to attack with): aioquic (frame-level timing control as malicious server/client)
- Post-hit actions: minimize the triggering frame sequence → confirm reachable assertion or key-lifecycle misalignment → assess the impact surface (client library → all downstream applications)
