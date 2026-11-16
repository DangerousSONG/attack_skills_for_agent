---
name: rfc9000-flow-control-accounting
description: Audit QUIC implementations' stream-level/connection-level flow-control accounting and limit enforcement per RFC 9000 §4 — accounting errors open memory-exhaustion or integer-wraparound attack surfaces (related CVE-2024-22189, CVE-2023-49295)
zh-signals: 审计 QUIC 实现对流级/连接级流量控制的记账与上限处理是否严格按 RFC 9000 §4——记账错误即存在内存耗尽或整数回绕攻击面（关联 CVE-2024-22189、CVE-2023-49295）
rfc: RFC 9000 §4（Flow Control）/ §2.1（整数编码与算术）
license: Apache-2.0
---

# RFC 9000 §4 Flow-Control Accounting and Limit Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §4.1: the receiver **must** limit the offset the sender may send at both connection and stream level (MAX_DATA / MAX_STREAM_DATA); the sender **must not** send data beyond the limit, and the receiver **must not** allocate memory for data beyond the limit.

RFC 9000 §2.1: protocol integer fields are 62-bit (varint); implementations must guard against overflow and wraparound when doing arithmetic.

Core pattern in one sentence: **flow control is a multi-layer state machine (connection level + per-stream level + send buffer + receive window); an accounting error or limit-handling defect at any layer can be remotely amplified into memory exhaustion.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| FC-1 | Keep sending data up to the MAX_DATA limit; observe whether the peer disconnects at the limit instant (CONNECTION_ERROR: FLOW_CONTROL_ERROR) or keeps buffering | Continues buffering / no error → accounting error |
| FC-2 | Interleave MAX_DATA increments with consumption (concurrent multi-stream read/write); detect window accounting that "over-counts consumed" (legitimate streams get stuck — availability surface) or "under-counts consumed" (limit exceeded — memory surface) | Either class counts as a violation |
| FC-3 | Do boundary arithmetic near the varint ceiling (2^62-1) (MAX_STREAM_DATA = 2^62-1 then +1) | Wraparound / abnormal crash → violation |
| FC-4 | Are window updates on half-closed streams (FIN sent/received) still accounted correctly | Accounting ignored → window leak, accumulates into memory occupancy |

Method: aioquic/quic-go custom clients with precise frame-timing control; observe connection error codes and peer memory.

## 3. Attack-Surface Hypotheses

- **Memory exhaustion**: buffering data beyond the limit at the receiver (FC-1) — an unauthenticated DoS primitive
- **Integer wraparound**: arithmetic errors at the 2^62 boundary (FC-3) can invert window judgment (illusion of "0 used") → unbounded buffering
- **Availability destruction**: over-counting kills legitimate connections (FC-2) — in adversarial scenarios this can selectively cut target connections

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2024-22189** (7.5 HIGH) | Multiple QUIC ecosystem implementations (quic-go et al. affected) | Related pattern: NEW_CONNECTION_ID flooding + RETIRE_CONNECTION_ID response suppression forces the peer to maintain state per retired CID until memory exhaustion — essentially asymmetric multi-layer state accounting and response obligations |
| **CVE-2023-49295** | quic-go | Path-validation state machine can be induced into DoS (same "protocol state obligations not enforced" pattern) |

Note: flow-control-accounting-class vulnerabilities are rarely disclosed, which is not evidence of safety — timing surfaces like FC-2/FC-4 require differential fuzzing to expose. These are "constrained but CVE-less" blind-spot clauses, which by the methodology is exactly the signal worth targeted auditing.

## 5. Differential Verification

Control group: quic-go ≥0.60, ngtcp2 (two independent implementations should behave identically).
Comparison fields: error-code consistency for FC-1~FC-4, behavior at the exceed instant, boundary-value handling.
False-positive exclusion: an implementation declaring a more conservative local window cap is compliant; only flag "over-limit still buffered" and "arithmetic errors".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (protocol state-machine fuzzing), `grammarinator-gen-fuzz` (custom QUIC frame-grammar generation; both in tool-skills/)
- Tool layer (what to attack with): aioquic (frame-level control), quic-go debug client, self-developed frame-timing scripts
- Post-hit actions: minimize the reproducing sequence → classify as "accounting error / wraparound / leak" → assess the DoS amplification ratio
