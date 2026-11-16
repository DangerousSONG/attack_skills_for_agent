---
name: rfc9113-settings-frame-flood
description: Audit whether HTTP/2 implementations bound SETTINGS-frame processing — repeatedly sending SETTINGS frames with an excessive entry count exhausts CPU (CVE-2020-11080 nghttp2 <1.41.0: a 14,400-byte frame with 2,400 entries repeated saturates the CPU, impacting the entire ecosystem including Node.js/Oracle MySQL); the RFC only requires the length-multiple-of-6 check and in-order processing — an entry-count cap is the implementation's obligation (blind-spot clause)
zh-signals: 审计 HTTP/2 实现 SETTINGS 帧处理是否有界——超大条目数 SETTINGS 帧反复发送即 CPU 耗尽（CVE-2020-11080 nghttp2 <1.41.0：14400 字节 2400 条目反复发送打满 CPU，波及 Node.js/Oracle MySQL 等全生态）；RFC 仅要求长度 6 的倍数校验与按序处理，条目数上限属实现义务（盲区条款）
rfc: RFC 9113 §6.5（SETTINGS 帧）/ §6.5.1 / RFC 7540 §6.5.2（设置项语义）
license: Apache-2.0
---

# RFC 9113 §6.5 SETTINGS-Frame Resource-Consumption Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §6.5 (key points):
> A SETTINGS-frame length **must be a multiple of 6**, otherwise treat as a connection error (FRAME_SIZE_ERROR);
> Values in a SETTINGS frame MUST be processed in the order they appear;
> SETTINGS affect connection state and do not rely on flow control.

Core pattern in one sentence: **SETTINGS is a connection-level control frame — it bypasses flow control and takes effect without ACK — the RFC gives format constraints but no entry-count cap, and that blank space is exactly CVE-2020-11080's room. The audit target is not "which RFC MUST is violated" but "did you build your own wall where the RFC left it blank."**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| SF-1 | Send a 14,400-byte SETTINGS frame (2,400 entries, legal multiple-of-6 length) in a loop | CPU climbs linearly with send rate and no circuit breaker → same class as CVE-2020-11080 |
| SF-2 | SETTINGS frame length not a multiple of 6 | Not disconnected with FRAME_SIZE_ERROR → §6.5 format validation missing |
| SF-3 | High-frequency SETTINGS (one frame per packet, values randomly changing) | Server applies each frame in full with no rate/count cap → unbounded processing surface |
| SF-4 | SETTINGS containing unknown identifiers | Not ignored (error/disconnect) → §6.5.2 tolerance obligation missing (compatibility breakpoint) |
| SF-5 | SETTINGS frame on a stream other than stream 0 | Not handled as a connection error → stream-orientation validation missing |

Method: h2 client sending in a loop; observe target CPU/event-loop latency; control group is the no-attack baseline throughput.

## 3. Attack-Surface Hypotheses

- **CPU-exhaustion DoS**: SF-1/SF-3 — low bandwidth saturates the event loop; the Node.js ecosystem fully impacted via its embedded nghttp2
- **Connection-state churn**: SF-3 — every SETTINGS frame changes connection parameters (e.g., window size), triggering recomputation across all downstream streams
- **Compatibility fingerprint/breakpoint**: SF-4 — erroring on unknown identifiers exposes the stack version and blocks future extensions

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2020-11080** | nghttp2 <1.41.0 (CVSS 7.5, CWE-400) | A 14,400-byte (2,400-entry) SETTINGS frame sent repeatedly → 100% CPU; no entry-count cap. Impacts the entire downstream ecosystem: Node.js, Oracle MySQL, GraalVM, etc. |
| Blind-spot declaration | Same family, TBD | The RFC does not specify an entry cap, and implementations set wildly different caps — this skill is flagged as a **high-recurrence blind spot**: must-check when auditing any new H2 stack |

## 5. Differential Verification

Control group: nghttp2 ≥1.41.0 (patched version includes entry-processing caps).
Comparison fields: SF-1 CPU curve, SF-3 frame-rate circuit-breaker threshold, SF-2/4/5 error-code correctness.
False-positive exclusion: a server ACKing after applying SETTINGS is normal behavior — judgment only considers "is the processing cost bounded"; an implementation declaring an "entry cap" that is absurdly high (e.g., 2^30) is still marked as a violation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (low-rate SETTINGS stream mode), `fuzzowski-network-fuzz` (SETTINGS-variant fuzzing)
- Tool layer (what to attack with): Python h2 (frame-level SETTINGS construction), CPU sampling scripts
- Post-hit actions: SF-1 confirmed → measure single-connection CPU amplification factor → assess the downstream impact list of embedded stacks like Node.js
