---
name: rfc9000-stream-reset-cancel
description: Audit whether QUIC stream reset/cancel (RESET_STREAM/STOP_SENDING) state-machine validation and cost symmetry comply with RFC 9000 §3.4/§3.5 — Final Size invariants, missing STREAM_STATE_ERROR on state mismatch, and cancellation cost far below server processing cost (H3 Rapid Reset DoS surface; related CVE-2023-44487 same-pattern in HTTP/2, H3 stacks advised to mitigate proactively; 2025 MadeYouReset variant proves the family keeps evolving)
zh-signals: 审计 QUIC 流重置/取消（RESET_STREAM/STOP_SENDING）的状态机校验与成本对称性是否按 RFC 9000 §3.4/§3.5——Final Size 不变量、状态错配未判 STREAM_STATE_ERROR、取消成本远低于服务端处理成本即 H3 版 Rapid Reset DoS 面（关联 CVE-2023-44487 HTTP/2 Rapid Reset 同模式，H3 栈被建议主动缓解；2025 年 MadeYouReset 变体证实该族持续演化）
rfc: RFC 9000 §3.4 / §3.5（Solicited State Transitions / Stream Final Size）/ §19.4 / §19.5（RESET_STREAM、STOP_SENDING 帧）/ RFC 9114 §4.1（H3 流取消语义）
license: Apache-2.0
---

# RFC 9000 §3.4/§3.5 Stream Reset & Cancel Cost Symmetry Audit

## 1. Normative Clauses (Original Sources)

RFC 9000 §3.4 (key points):
- RESET_STREAM / STOP_SENDING request the peer to abort a stream; upon receipt the receiver stops processing/releases resources for that direction;
- Receiving RESET_STREAM for an **already-closed / nonexistent stream** MUST be treated as STREAM_STATE_ERROR (except the exempt scenario where the stream never existed and silent discard is allowed) — state-machine mismatch is not "harmless".

RFC 9000 §3.5 / §4.5 (Final Size invariants, key points):
- Once a stream closes, its Final Size is fixed and cannot change;
- A received RESET_STREAM whose Final Size field is smaller than the number of bytes already acknowledged received, or larger than the flow-control limit, MUST close the connection with FLOW_CONTROL_ERROR.

RFC 9000 §19.4 (RESET_STREAM frame format obligations, key points):
- Two fields: Error Code (varint) + Final Size (varint); the frame may only appear in the direction in which the sender has send rights for that stream.

Core pattern in one sentence: **Cancelling a stream costs the sender a dozen bytes and zero waiting — if the server still pays full parse/schedule cost for a stream that was opened then cancelled, the concurrency cap is a paper number. HTTP/2 Rapid Reset (CVE-2023-44487) already proved this cost asymmetry can take down Google/Cloudflare/AWS; H3 moves the same cancellation machinery (RESET_STREAM/STOP_SENDING) into QUIC, making this clause a mandatory question for H3 stacks.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| RS-1 | In an H3 scenario, open a request stream and immediately RESET_STREAM/STOP_SENDING (canonical Rapid Reset port); measure server CPU/allocation rate | Cancellation path still fully parses HEADERS/QPACK/scheduling → cost asymmetry holds, flag as H3 Rapid Reset surface |
| RS-2 | Inject RESET_STREAM into a nonexistent/closed/read-only stream | No STREAM_STATE_ERROR (silent, or wrongly releases live-stream resources) → §3.4 violation |
| RS-3 | Craft RESET_STREAM with Final Size smaller than bytes already received, or larger than the flow-control limit | Connection not closed with FLOW_CONTROL_ERROR → §3.5/§4.5 violation (flow-control accounting can be poisoned by reset frames) |
| RS-4 | Variant cadence: batch open streams — delayed batch cancel (bypasses pure rate thresholds), open beyond-limit streams relying on per-item server rejection | No connection-level work budget / no forced close → neither variant 1 nor variant 2 of 2023-44487 is mitigated |
| RS-5 | STOP_SENDING × RESET_STREAM cross-timing (simultaneous bidirectional cancel, data frames arriving after cancel) | Half-closed state-machine assertion failure/resource leak → state-machine defect |

Method: aioquic client frame-level control; control group = per-request server CPU and allocation curves before/after the attack; connection-level metrics (close rate / work budget), not per-request metrics.

## 3. Attack-Surface Hypotheses

- **H3 Rapid Reset DoS**: RS-1/RS-4 — a single connection saturates server CPU; the concurrency cap is void (the H2 version caused one of the largest L7 DDoS events in history)
- **Flow-control accounting poisoning**: RS-3 — forged Final Size corrupts the connection-level flow-control ledger, causing window inflation/deflation
- **Half-closed state confusion**: RS-5 — resource-release race under bidirectional cancel (UAF/leak family; chain with the close-state audit)

## 4. Related Historical CVEs

| CVE / Evidence | Implementation | Root cause |
|---|---|---|
| **CVE-2023-44487** | Entire HTTP/2 ecosystem (nghttp2 <1.57, Netty, Envoy, Go x/net, nginx, Caddy, F5, etc.) | Rapid Reset: RST_STREAM closes a stream immediately without consuming a concurrency slot, yet the server pays parse/schedule cost for every cancelled request. Official conclusion: no evidence of H3 impact, but **H3 stacks are advised to implement similar mitigations proactively** — this Skill is the audit embodiment of that advice |
| **MadeYouReset (2025 variant evidence)** | Residual HTTP/2 ecosystem | Implementations mitigating only on "reset frequency" were bypassed by behavioral variants — lesson: mitigation must be a connection-level work budget, not frame counting |
| RFC 9113 §5.1.2 pattern replication | QUIC stream concurrency model | H2's structural weakness ("only open/half-closed streams count toward the concurrency cap") is isomorphic in the QUIC stream state machine (§3); audit H3 stacks against the same pattern |

## 5. Differential Verification

Control group: H3 stacks with connection-level work budgets (e.g. recent nghttp3 with rapid-reset mitigation), latest quic-go.
Comparison fields: RS-1 per-connection request-processing rate ceiling, RS-2/RS-3 error-code correctness, whether GOAWAY/close is forced under RS-4 variants.
False-positive exclusion: a server that releases reset streams immediately with no application-layer side effects is compliant; RS-1 must be judged on "total server work grows linearly with cancel rate", not on "cancellation is allowed" itself; architectures where an HTTP gateway still needs to fetch from origin after cancellation should be annotated "mitigation at gateway layer", shifting the audit target to the gateway.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (H3 cancel-storm timing patterns), `fuzzowski-network-fuzz` (RESET/STOP_SENDING state-machine fuzz)
- Tool layer (with what): aioquic (frame-level cancel timing control), h3 load generator (RS-1 throughput comparison), quic-interop-runner
- Post-hit actions: measure max per-connection server cost-injection rate → re-test mitigation effectiveness under variants 1/2 → run RS-3 ledger poisoning as a separate flow-control ledger diff → merge evidence into the DDoS primitive library
