---
name: rfc9113-flow-control-window-stall
description: Audit the symmetry and boundedness of HTTP/2 flow-control-window (WINDOW_UPDATE) implementations — window manipulation forcing the server to queue data at 1-byte granularity is Data Dribble (CVE-2019-9511, CVSS 7.5); zero-increment WINDOW_UPDATE is an illegal frame, and a server that answers each with RST_STREAM enables the MadeYouReset resource-consumption chain (CVE-2025-5115 Jetty GHSA-mmxm-8w33-wc4h); INITIAL_WINDOW_SIZE=0 plus trickle WINDOW_UPDATE Slowloris holds form the hold half of the HTTP/2 Bomb (CVE-2026-49975/47774); RFC 9113 §5.2/§6.9 define window semantics but the "stalled-stream lifecycle budget" is left blank
zh-signals: 审计 HTTP/2 流控窗口（WINDOW_UPDATE）实现的对称性与有界性——窗口操纵强制服务端以 1 字节粒度排队即 Data Dribble（CVE-2019-9511，CVSS 7.5）；零增量 WINDOW_UPDATE 属非法帧，服务端逐帧回 RST_STREAM 即 MadeYouReset 资源消耗链（CVE-2025-5115 Jetty GHSA-mmxm-8w33-wc4h）；INITIAL_WINDOW_SIZE=0 + 涓流 WINDOW_UPDATE 的 Slowloris 持有是 HTTP/2 Bomb（CVE-2026-49975/47774）的半条链；RFC 9113 §5.2/§6.9 给了窗口语义但"stalled 流生命周期预算"是留白
rfc: RFC 9113 §5.2（流控原则）/ §6.9（WINDOW_UPDATE）/ §6.5.2（INITIAL_WINDOW_SIZE）
license: Apache-2.0
---

# RFC 9113 §5.2/§6.9 Flow-Control Window Manipulation and Stalled-Stream Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §6.9 (key points):
> A WINDOW_UPDATE increment of 0 must be handled as a **stream error** (PROTOCOL_ERROR); a window can only be increased by WINDOW_UPDATE; the sender must not rely on behavior other than the peer's window shrinking.

RFC 9113 §5.2 (key points):
> Flow control applies only to DATA frames; HEADERS are not flow-controlled.

Core pattern in one sentence: **H2 flow control is a credit system where "the sender reads the receiver's mood" — attackers reverse it: grant full credit to make the server produce data frantically, then claw it back at the smallest granularity (or with illegal zero-increment frames), and the server's queues store the memory on the attacker's behalf. The RFC defines the disposition of illegal frames (0 increment → stream error), but gives no answer to "how long can a stalled stream freeload" — which is exactly why the 2026 HTTP/2 Bomb pierced five major implementations at once.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| FW-1 | Request large objects on multiple streams, recovering credit with 1-byte WINDOW_UPDATE trickles per stream | Server queues slices at minimum granularity; CPU/memory amplify with stream count → same class as CVE-2019-9511 Data Dribble |
| FW-2 | Send zero-increment WINDOW_UPDATE (stream-level + connection-level) | Not answered with RST_STREAM as a stream error / no disconnect → §6.9 illegal-frame disposition missing (doubling as a fingerprint) |
| FW-3 | Advertise INITIAL_WINDOW_SIZE=0 in SETTINGS, then trickle extremely slowly | Server holds allocated response buffers indefinitely → HTTP/2 Bomb hold half-chain holds |
| FW-4 | Stack new requests while streams remain stalled | No stalled-stream lifecycle budget / no cap → buffers accumulate without bound |
| FW-5 | Window-overflow construction: send DATA beyond the available window | Not disconnected with FLOW_CONTROL_ERROR → §5.2 window accounting missing |
| FW-6 | Connection-level window exhausted while stream-level window is sufficient (or vice versa) | Stream/connection two-level window accounting inconsistent → accounting defect |

Method: h2 client with multi-stream + window-manipulation scripts; observe server memory residency, slice granularity, stalled-stream reclamation time; control group is the normal-window baseline.

## 3. Attack-Surface Hypotheses

- **Memory-exhaustion DoS**: FW-3/FW-4 — combined with the HPACK amplification chain this is the full CVE-2026-49975 chain (cross-reference `rfc7541-hpack-decompression-accounting`)
- **CPU-exhaustion DoS**: FW-1 — 1-byte slicing multiplies the send path into N-times syscalls
- **RST-storm resource consumption**: FW-2 in bulk repetition — the server answers each frame with an RST_STREAM; the Jetty MadeYouReset empirical case (send illegal frames → server returns RST → RSTs not counted against the concurrency cap → rapid stream creation on a short clock)

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2019-9511** | Multiple implementations (Data Dribble, 2019-08 CERT batch) | Window manipulation + priority manipulation forcing the server to queue at 1-byte granularity; CVSS 7.5 / CWE-400 |
| **CVE-2025-5115** | Eclipse Jetty ≤9.4.57/≤10.0.25/≤11.0.25/≤12.0.21 (GHSA-mmxm-8w33-wc4h) | Client sends zero-increment WINDOW_UPDATE and other illegal frames → server answers RST_STREAM consuming resources; MadeYouReset variant — the RFC 9113 §6.9-compliant disposition weaponized |
| **CVE-2026-49975 / CVE-2026-47774** | Apache httpd (mod_http2 <2.0.41) / Envoy (RHSB-2026-007) | HTTP/2 Bomb: HPACK entry-accounting amplification + zero-window Slowloris holds; nginx 1.29.8 fixed via max_headers (no CVE assigned); IIS/Envoy/Pingora had no patch at the time |
| Lineage | CVE-2016-1546 (Apache worker starvation) etc. | Slowloris-type holds have recurred since 2016; this skill is flagged as a **must-check in combination with the compression-layer audit** |

## 5. Differential Verification

Control group: patched nginx (1.29.8+, max_headers + stalled-stream budget); Cloudflare edge (aggressive stalled-stream reclamation) as the benchmark.
Comparison fields: FW-1 minimum slice granularity, FW-3 maximum stalled-stream survival time, FW-2 error-code correctness, FW-5/FW-6 accounting consistency.
False-positive exclusion: an implementation with a global stalled-stream cap (e.g., connection memory quota) that triggers GOAWAY on breach → passes; zero-increment disposition correct with resource consumption comparable to the patched version → passes.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (Slowloris-type window holds), `fuzzowski-network-fuzz` (WINDOW_UPDATE increment/timing mutation)
- Tool layer (what to attack with): Python h2 window-manipulation scripts, memory-residency sampling
- Post-hit actions: FW-3+FW-4 confirmed → re-test the full HTTP/2 Bomb chain combined with HPACK amplification probes → measure maximum pinnable memory per connection → rate against the CVE-2026-49975 amplification-factor table
