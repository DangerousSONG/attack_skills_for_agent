---
name: rfc9000-close-draining-state
description: Audit QUIC implementations' frame-handling obligations during the closing/draining states per RFC 9000 §10.2 — the closing state may only retransmit CONNECTION_CLOSE; the draining state MUST send nothing and process nothing; violations open the connection-close state machine as an attack surface (related CVE-2024-45396 Quicly draining-state ACK handling assertion failure, QUIC-FUZZ empirical; xquic Stateless Reset / VN log NULL dereference; nginx QUIC CVE-2024-31079/32760/34161/35200 single-session worker-crash family)
zh-signals: 审计 QUIC 实现在 closing/draining 关闭状态期间的帧处理义务是否按 RFC 9000 §10.2——closing 状态只可重发 CONNECTION_CLOSE、draining 状态 MUST 不发包不处理，违反即关闭状态机攻击面（关联 CVE-2024-45396 Quicly draining 态处理 ACK 断言失败 QUIC-FUZZ 实证；xquic Stateless Reset/VN 日志 NULL 解引用；nginx QUIC CVE-2024-31079/32760/34161/35200 单会话 worker 崩溃族）
rfc: RFC 9000 §10.2 / §10.2.1 / §10.2.2（Immediate Close、closing 与 draining 状态）/ §10.3（无状态重置，对照）
license: Apache-2.0
---

# RFC 9000 §10.2 Close and Draining State Frame-Handling Obligations Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §10.2 (key points):
> An immediate close terminates the connection via a CONNECTION_CLOSE frame; the sender enters the closing state and **retransmits** CONNECTION_CLOSE (to handle loss) until it receives the peer's CONNECTION_CLOSE or times out into draining.

RFC 9000 §10.2.1 (closing-state obligations, key points):
- In the closing state an endpoint may **only send CONNECTION_CLOSE frames**, no other frame types;
- In the closing state, receiving any frame **other than** CONNECTION_CLOSE MUST be answered with another CONNECTION_CLOSE (confirming the peer is alive / continuing to respond under attack-induced loss);
- After receiving the peer's CONNECTION_CLOSE or waiting out the timeout, enter draining.

RFC 9000 §10.2.2 (draining-state obligations, key points):
- In the draining state an endpoint **MUST NOT send any packets**;
- Received packets are silently discarded, **no frames may be processed** (including ACKs);
- After the draining period expires, all connection state is released.

Core pattern in one sentence: **close states are the area of a protocol state machine most easily written wrong under the "it's already over, just handle it casually" mindset — processing one ACK in draining, answering one STREAM in closing, turns a half-dead connection into a crash entry point.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| CD-1 | Drive the server into draining (send CONNECTION_CLOSE to induce peer close, then observe; or probe via timeout rates), then inject an ACK frame from the peer | Server processes the ACK and mutates state / crashes → violates §10.2.2 (same class as CVE-2024-45396) |
| CD-2 | Keep injecting non-CONNECTION_CLOSE frames (STREAM/ACK/PING) while in closing state; observe server responses | Responds with non-CC frames (e.g., ACK/STREAM) → violates §10.2.1; responds with nothing at all → retransmission obligation missing (under loss the peer never receives the close signal) |
| CD-3 | Measure closing retransmission cadence: count CC retransmissions and intervals in a lossy environment | Sent only once, never retransmitted → close signal lost to packet loss leaves ghost half-open connections (obligation missing; not a crash surface but bloats the state table) |
| CD-4 | Inject Stateless Reset packets and Version-Negotiation packets during close; observe logging and handling paths | Triggers NULL dereference / logging crash → same class as xquic (QUIC-FUZZ empirical) |
| CD-5 | Concurrent-close race: both ends send CONNECTION_CLOSE simultaneously (CC collision) | Assertion failure / state-machine deadlock → bidirectional-close handling defect |

Method: aioquic scripted close timing (CC → state observation → frame injection); crash surfaces paired with a process-liveness probe.

## 3. Attack-Surface Hypotheses

- **Close-state crash DoS**: CD-1/CD-4 — draining/closing code paths are naturally weak in test coverage; a high-frequency fuzz-hit area (2 of the QUIC-Fuzz targets' CVEs come from the close family)
- **Half-open connection accumulation**: CD-3 — CC not retransmitted + never received by the peer → two-sided state inconsistency, the server state table drained slowly
- **Close-hijack surface**: accepting and responding to non-CC frames in closing state leaves a door open for a "still alive after close" covert channel

## 4. Related Historical CVEs

| CVE / Empirical Finding | Implementation | Root Cause |
|---|---|---|
| **CVE-2024-45396** | Fastly quicly (found by QUIC-Fuzz) | Processing an ACK frame on a draining connection triggers an assertion failure — the textbook empirical case of a draining-obligation violation |
| **CVE-2024-45402** | Picotls (found by QUIC-Fuzz) | Double free on unexpected public-key length — close/handshake cross-path memory-error family |
| QUIC-Fuzz additional findings | XQUIC (Alibaba) | NULL-pointer dereference when handling Stateless Reset packets and Version-Negotiation logging |
| **CVE-2024-31079 / 32760 / 34161 / 35200** | nginx ngx_http_v3_module (1.25.0–1.25.5, 1.26.0) | A single malicious QUIC session crashes the worker / leaks memory — H3 session-termination path defect family; must-check for close-state audits |

## 5. Differential Verification

Control group: latest quic-go (draining strictly discards without processing), quiche (CC retransmission cadence per §10.2).
Comparison fields: CD-1 state leakage, CD-2 frame-type whitelist, CD-3 retransmission count (≥2 in a lossy environment), CD-5 dual-CC race.
False-positive exclusion: transitioning to draining immediately upon receiving the peer's CC in closing state is a compliant transition; an implementation keeping an extremely short ACK-only window before draining (disputable but defensible) is marked a "policy divergence" rather than a violation — CD-1 crash-class judgments take priority.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (close-timing frame-sequence fuzzing), `grammarinator-gen-fuzz` (CC-collision/timing variant generation)
- Tool layer (what to attack with): aioquic (scripted CONNECTION_CLOSE timing), process-liveness probe (crash determination), quic-interop-runner (lossy environment for CD-3)
- Post-hit actions: minimize and extract the crashing frame sequence → measure half-open connection accumulation rate for CD-3 → merge close-family defects into the "state-machine weakness" evidence chain
