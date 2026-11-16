---
name: rfc9000-connection-id-retirement
description: Audit QUIC implementations' handling of Connection ID lifecycle obligations (NEW_CONNECTION_ID / RETIRE_CONNECTION_ID / active_connection_id_limit) for symmetry — asymmetric obligations create a memory-exhaustion attack surface (related CVE-2024-22189, 7.5 HIGH)
zh-signals: 审计 QUIC 实现对 Connection ID 生命周期（NEW_CONNECTION_ID / RETIRE_CONNECTION_ID / active_connection_id_limit）义务的处理是否对称——义务不对称即存在内存耗尽攻击面（关联 CVE-2024-22189，7.5 HIGH）
rfc: RFC 9000 §5.1（Connection IDs）/ §19（Frame 处理规则）
license: Apache-2.0
---

# RFC 9000 §5.1 Connection ID Lifecycle Obligation-Symmetry Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §5.1.2: after an endpoint sends NEW_CONNECTION_ID, the peer may use RETIRE_CONNECTION_ID to request retirement; **the endpoint receiving RETIRE_CONNECTION_ID must stop using that CID and confirm with a RETIRE_CONNECTION_ID (the frame obligations come in pairs)**.

RFC 9000 §5.1.1: the `active_connection_id_limit` transport parameter limits how many CIDs the peer may keep active; **no new NEW_CONNECTION_ID may be issued before the limit is reached headroom-wise**.

§19.16: a RETIRE_CONNECTION_ID frame referencing a CID still in use, or one never issued by the peer, must be treated as a protocol error (FRAME_ENCODING_ERROR).

Core pattern in one sentence: **the protocol defines paired "allocate-use-retire" obligations for state objects; asymmetric obligations (one side must maintain state while the other can trigger it at low cost) get weaponized.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| CI-1 | Rapidly send a large number of NEW_CONNECTION_IDs and immediately RETIRE them, forcing the peer to maintain response state per retirement | Peer memory grows monotonically with iteration count and has no cap → vulnerability |
| CI-2 | Suppress the peer's congestion window via selective ACK + RTT manipulation so its RETIRE_CONNECTION_ID responses queue (CVE-2024-22189 precise timing) | Response obligations back up, state grows unbounded → vulnerability |
| CI-3 | Send enough NEW_CONNECTION_IDs to push the peer's active CID count beyond its declared `active_connection_id_limit` | Not handled as a protocol error / limit not enforced → violation |
| CI-4 | RETIRE references a currently active CID or one the peer never issued | FRAME_ENCODING_ERROR not returned → lax frame validation |

Method: aioquic frame-level scripts; observe the peer's memory curve and connection error codes.

## 3. Attack-Surface Hypotheses

Unauthenticated remote memory exhaustion: attack cost = a small-volume frame sequence; target cost = one unreleasable CID state per iteration (CVE-2024-22189 measured exhaustion achievable). The lax validation in CI-3/CI-4 is an independent attack surface (state-machine confusion) and often combines with CI-1.

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2024-22189** (7.5 HIGH) | Multiple QUIC implementations (disclosed with quic-go as the representative) | The attacker floods NEW_CONNECTION_ID and retires old CIDs; the receiver must return RETIRE_CONNECTION_ID per retirement; the attacker uses selective ACKs to crush the peer's congestion window and manipulates RTT so responses cannot be sent; state piles up without bound until memory exhaustion |

## 5. Differential Verification

Control group: quic-go patched version (≥0.43), ngtcp2.
Comparison fields: memory-curve slope over 1k/10k/100k CI-1 iterations; response latency under CI-2 timing suppression; error codes for CI-3/CI-4.
False-positive exclusion: an implementation optionally rate-limiting CID issuance proactively is compliant hardening; only flag implementations where "obligation asymmetry can be forced".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (state-machine differential), `slowhttptest-dos` (resource-exhaustion verification; both in tool-skills/)
- Tool layer (what to attack with): aioquic (primary frame-level timing control), quic-go client as control
- Post-hit actions: quantify state accumulation per iteration → give a time estimate for memory exhaustion at N iterations → output the affected version surface
