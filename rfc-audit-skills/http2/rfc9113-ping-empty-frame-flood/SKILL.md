---
name: rfc9113-ping-empty-frame-flood
description: Audit whether HTTP/2 implementations bound the processing cost of mandatory-response frames (PING) and empty frames (DATA/HEADERS/CONTINUATION/PUSH_PROMISE) — PING forces a per-frame ACK (CVE-2019-9512 Ping Flood: sustained PING inflates the response queue, exhausting CPU/memory); empty frames bypass flow control with asymmetric per-frame cost (CVE-2019-9518 Empty Frame Flood, disclosed with Envoy security-team acknowledgment); zero-length header memory residency (CVE-2019-9516 Header Leak); RFC 9113 §6.7/§6.1 give the semantics but no cost guardrails
zh-signals: 审计 HTTP/2 实现对强制应答帧（PING）与空载帧（DATA/HEADERS/CONTINUATION/PUSH_PROMISE）的处理代价是否有界——PING 强制逐帧 ACK 应答（CVE-2019-9512 Ping Flood：持续 PING 造成应答队列膨胀 CPU/内存耗尽）；空载帧不吃流控、单帧处理成本不对称（CVE-2019-9518 Empty Frame Flood，Envoy 安全团队致谢披露）；0 长度头字段内存驻留（CVE-2019-9516 Header Leak）；RFC 9113 §6.7/§6.1 给了语义没给成本护栏
rfc: RFC 9113 §6.7（PING）/ §6.1（DATA）/ §6.2（HEADERS）/ §6.6（PUSH_PROMISE）
license: Apache-2.0
---

# RFC 9113 §6.7/§6.1 PING and Empty-Frame Cost-Asymmetry Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §6.7 (key points):
> On receiving a PING frame, an endpoint **must** return a PING response with the ACK flag set (payload copied byte for byte); PING is not flow-controlled.

Core pattern in one sentence: **PING and empty frames share one property — "nearly free on the wire, mandatory work off it": PING forces a per-frame ACK, and empty DATA/HEADERS frames bypass flow control yet traverse the full frame-parsing pipeline. The RFC's response obligation is rigid; the guardrails (per-connection frame-rate caps, minimum payload, throttling) are the implementation's obligation. The audit target is "is the slope of the mandatory work clamped."**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| PF-1 | Sustain PING on a single connection (no ACK waiting, backpressure saturated) | No per-connection PING rate limit; ACK response queue grows unbounded → same class as CVE-2019-9512 |
| PF-2 | PING on a stream with non-zero stream ID | Not handled as a connection error → §6.7 stream-orientation validation missing (fingerprint point) |
| PF-3 | Empty DATA frame flood (len=0, no END_STREAM) | Per-frame processing cost / attack bandwidth ratio > 100x with no frame-rate circuit breaker → same class as CVE-2019-9518 |
| PF-4 | Empty HEADERS/CONTINUATION frame flood (len=0, no END_HEADERS) | Same as above → explicitly listed frame class in CVE-2019-9518 |
| PF-5 | Sustained zero-length header name + zero-length header value (optionally Huffman-encoded to 1 byte) | Allocated on every occurrence and resident until session end → same class as CVE-2019-9516 Header Leak |

Method: frame-level client stress-testing PING and empty frames against baselines; observe CPU, memory residency, and normal-request P99; control group is the idle-connection baseline.

## 3. Attack-Surface Hypotheses

- **CPU/memory-exhaustion DoS**: PF-1/PF-3/PF-4 — all three are asymmetric drains with "KB-level attack bandwidth, MB-level processing cost"
- **Connection keepalive abuse**: PF-1 — a PING storm keeps idle connections from ever being reclaimed (combine with slow connections to fill the connection table)
- **Memory-residency leak**: PF-5 — zero-length headers trigger allocations that are never released (for the session lifetime), amplified across many streams

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2019-9512** | Full stack, multiple implementations (batch fixes RHSA-2019:2692/2745 series) | Ping Flood: mandatory per-frame ACK obligation + no rate limit → response-queue inflation; Cloudflare later mitigated with GOAWAY+ENHANCE_YOUR_CALM (the Hyper adaptive-window false-positive incident also traces to this) |
| **CVE-2019-9518** | Multiple implementations (RHSA-2019:2925/2939/2955/3892; netty 4.1.13 entire series affected) | Empty-frame flood: per-frame processing cost of empty DATA/HEADERS/CONTINUATION/PUSH_PROMISE far exceeds their bandwidth share; disclosed with Envoy security-team acknowledgment |
| **CVE-2019-9516** | nginx (fix commit 6dfbc8b1c211), Node.js, IBM products | 0-Length Headers Leak: zero-length header name/value allocations remain resident until session death; CVSS 7.5/6.5 |

## 5. Differential Verification

Control group: patched nginx (1.17.x 2019-08 batch); Cloudflare edge behavior (high-rate PING → GOAWAY ENHANCE_YOUR_CALM) as the "mitigation benchmark".
Comparison fields: PF-1 circuit-breaker threshold (frames/second), PF-3/4 per-frame cost ratio, PF-5 memory-residency slope.
False-positive exclusion: an implementation with a per-connection total frame-rate cap shared by PING and empty frames → passes; an implementation that merely delays ACKs but keeps the queue bounded → passes.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (slow PING/empty-frame streams), `fuzzowski-network-fuzz` (frame-type/payload combination mutation)
- Tool layer (what to attack with): Python h2 frame-level construction, CPU/memory sampling
- Post-hit actions: PF-1 confirmed → measure the threshold frame rate that saturates ACK production per connection → baseline against Cloudflare's ENHANCE_YOUR_CALM threshold; PF-5 confirmed → measure per-session residency ceiling and multi-stream amplification factor
