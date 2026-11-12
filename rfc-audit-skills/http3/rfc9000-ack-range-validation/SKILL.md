---
name: rfc9000-ack-range-validation
description: Audit whether QUIC implementations validate ACK-frame acknowledgment ranges per RFC 9000 §13.1/§21.4 — acknowledging unsent packets, malformed ACK ranges, or undetected optimistic ACKs become a congestion-control-deception DDoS-amplification primitive (related CVE-2025-4820/CVE-2025-4821 quiche < 0.24.4; ANRW 2025: 11 of 16 Interop implementations vulnerable)
zh-signals: 审计 QUIC 实现对 ACK 帧确认范围的校验是否按 RFC 9000 §13.1/§21.4——确认未发送的包、ACK 范围畸形、乐观确认（Optimistic ACK）未检测即拥塞控制被欺骗的 DDoS 放大原语（关联 CVE-2025-4820/CVE-2025-4821 quiche < 0.24.4；ANRW 2025：16 个 Interop 实现中 11 个脆弱）
rfc: RFC 9000 §13.1 / §21.4（ACK 处理与乐观确认攻击）/ RFC 9002 §6（拥塞控制信号）
license: Apache-2.0
---

# RFC 9000 §13.1 ACK Acknowledgment-Range Validation Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §13.1 (verbatim):
> An endpoint SHOULD treat receipt of an acknowledgment for a packet it did not send as a connection error of type PROTOCOL_VIOLATION, if it is able to detect the condition.

RFC 9000 §21.4 (key points):
> An endpoint that acknowledges packets it has not received might cause a congestion controller to permit sending at rates beyond what the network supports. An endpoint MAY skip packet numbers when sending packets to detect this behavior. An endpoint can then immediately close the connection with a connection error of type PROTOCOL_VIOLATION.

IETF draft-chen-quic-logical-vuln-mitigations (reinforcement): ACK ranges SHOULD be validated as well-formed, non-overlapping, and strictly decreasing before they mutate loss-recovery state; the same packet number must not flip acknowledgment state repeatedly just because it appears multiple times in malformed ACKs.

Core pattern in one sentence: **ACK is the only feedback signal for congestion control — acknowledging "packets never sent" is forging a "network is fine" measurement, pushing the congestion window above the network's true capacity, and turning the server into an accomplice of its own traffic-amplification DoS.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| AK-1 | Server has sent up to PN=N; send an ACK range [0, N+50] acknowledging unsent packets | Connection not closed (PROTOCOL_VIOLATION) → violation (same class as quiche CVE-2025-4821) |
| AK-2 | Craft malformed ACK ranges: overlapping / duplicate packet numbers / arithmetic underflow (multiple First Ranges + overlapping Gaps) | Loss-recovery state flipped repeatedly / crash → violation; normalized handling per draft-chen → compliant |
| AK-3 | Optimistic ACK: preemptively acknowledge not-yet-arrived packets following the predicted packet-number rhythm (fine-grained pacing timing) | Send rate artificially pushed high with no detection → violation (RFC requires gap detection; §21.4 is MAY-level but Cloudflare proved it mandatory) |
| AK-4 | Check whether the implementation performs **random packet-number skipping** and associates "ghost packets" (skip PN + dummy packet) | No gap mechanism → no defense against AK-3, flagged as a high-risk gap |
| AK-5 | Timing combination: ACK frames acknowledging packets already declared lost and retransmitted seconds ago; detect congestion-window regression anomalies from duplicate acknowledgments | Abnormal cwnd shrink/inflation → accounting violation |

Method: aioquic custom client with precise ACK-timing control; measure server send-rate changes (control group: no-attack baseline rate).

## 3. Attack-Surface Hypotheses

- **Congestion-control deception → outbound-amplification DDoS**: AK-1/AK-3 — a single client pushes the server's send rate up severalfold; concurrent clients form a DDoS vector (Cloudflare's assessment)
- **ACK-parse crash surface**: AK-2 — range underflow/overlap is a high-frequency fuzz hit area in loss-recovery code
- **Bandwidth theft**: the attack connection squeezes the bandwidth of other connections on the same egress (unfair competition)

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2025-4821** | Cloudflare quiche < 0.24.4 | Missing ACK-range validation: a client could acknowledge large ranges of server packet numbers never sent (0-100), paving the way for optimistic-ACK attacks. Fix: enforce validation against the highest sent packet number and close violating connections |
| **CVE-2025-4820** | Cloudflare quiche < 0.24.4 | Optimistic-ACK attack could bypass validation by predicting the packet-number rhythm, falsely reporting low RTT to push the send rate up. Fix: dynamic CWND-aware gap frequency |
| ANRW 2025 paper (UCLouvain) | **11 of 16** QUIC Interop Runner implementations (quic-go, ngtcp2, mvfst, quiche, kwik, picoquic, aioquic, nginx, lsquic, quinn, s2n-quic, some versions) | No packet-number gaps or no ACK-correctness validation → vulnerable to OACK attacks — a textbook case of an "MAY-level clause that is actually mandatory" in RFC 9002/9000, an ecosystem-level blind spot |

## 5. Differential Verification

Control group: quiche ≥ 0.24.4 (patched), latest quic-go (gaps + validation).
Comparison fields: whether AK-1 closes the connection, AK-2 state-machine consistency, AK-4 gap-mechanism existence, send-rate ratio before/after attack.
False-positive exclusion: an implementation that only processes ACKs within the sent range (dropping the excess) and cannot detect the condition falls under the "unable to detect" exemption, but must be flagged as missing gap defense; only flag "acknowledgment of unsent packets accepted" and "no gaps and no validation".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (rate-deception timing patterns), `fuzzowski-network-fuzz` (ACK-range grammar fuzzing)
- Tool layer (what to attack with): aioquic (byte-level ACK-frame control), rate-measurement scripts
- Post-hit actions: quantify the send-rate amplification ratio → assess multi-connection DDoS feasibility → minimize the AK-2 crash path separately
