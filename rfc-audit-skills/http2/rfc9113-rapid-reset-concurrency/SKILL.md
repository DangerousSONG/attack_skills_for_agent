---
name: rfc9113-rapid-reset-concurrency
description: Audit HTTP/2 implementations' concurrency-limit accounting and forced-close obligations per RFC 9113 §5.1.2/§6.4 — only open/half-closed streams count toward concurrency (closed releases the slot immediately), RST_STREAM closes without acknowledgment so "open then cancel" consumes no concurrency slot; without a connection-level work budget this is the original CVE-2023-44487 Rapid Reset vulnerability surface (Google/AWS/Cloudflare all affected, one of the largest L7 DDoS events in history, 2023-10; variants: batched delayed cancel, over-limit stream opens relying on per-stream rejection)
zh-signals: 审计 HTTP/2 实现并发上限的记账口径与强制关闭义务是否按 RFC 9113 §5.1.2/§6.4——只有 open/half-closed 计入并发（closed 立即释放槽位）、RST_STREAM 免确认即关闭即"开了又取消"不占用并发槽；无连接级工作预算即 CVE-2023-44487 Rapid Reset 原版漏洞面（Google/AWS/Cloudflare 全量受影响，2023-10 史上最大 L7 DDoS 之一；变体：批量延迟取消、超限开流依赖逐条拒绝）
rfc: RFC 9113 §5.1.2（并发上限记账口径）/ §6.4（RST_STREAM）/ §6.8（GOAWAY）
license: Apache-2.0
---

# RFC 9113 §5.1.2 Concurrency-Limit Accounting and Rapid Reset Audit (H2 Original)

## 1. Normative Clauses (Original Sources)

RFC 9113 §5.1.2 (key points):
> SETTINGS_MAX_CONCURRENT_STREAMS limits streams in the **open and half-closed states** — idle/reserved/closed do not count.

RFC 9113 §6.4 (key points):
> RST_STREAM lets the sender **terminate a stream immediately** without waiting for peer acknowledgment; the receiver stops processing and releases that stream's resources on receipt.

RFC 9113 §6.8 (key points):
> GOAWAY initiates connection shutdown; after triggering mitigation, a server should **force-close the connection immediately** rather than drain gracefully.

Core pattern in one sentence: **the concurrency cap governs "how many live streams exist at one instant", and RST_STREAM lets the attacker compress a stream's lifetime into a single send — the instantaneous snapshot always complies while request throughput runs unbounded. The design guarded the concurrency count but not the concurrency churn rate; the audit question is: did your implementation build the limit on a snapshot or on a rate.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| RR-1 | Canonical: open stream → send HEADERS → immediately RST_STREAM, in a loop (single-connection request rate no longer RTT-bound) | Total server work grows linearly with cancel rate and no connection-level circuit breaker → same class as CVE-2023-44487 |
| RR-2 | Variant 1: batch-open streams → brief delay → batch cancel (bypasses "reset-rate" threshold mitigations) | Implementations that only count RST frequency are bypassed → mitigation-coverage defect |
| RR-3 | Variant 2: continuously open streams beyond the concurrency cap (relying on per-stream rejection without disconnect) | Server tolerates over-limit opens without forcing closure → the RFC-suggested lenient path weaponized |
| RR-4 | After triggering any suspicious pattern, observe server response | No GOAWAY forced close (graceful drain gives the attacker extra lifetime) → §6.8 mitigation obligation missing |
| RR-5 | Concurrency-accounting audit: whether closed streams release their slot immediately after RST, and whether release timing is too early | Accounting inconsistent with the state machine → implementation-level evidence that the cap is toothless |

Method: single-connection stress test (nghttp variants / custom client); the metric is the slope of server CPU/allocation versus the request-cancel rate — **do not judge single-request behavior**.

## 3. Attack-Surface Hypotheses

- **L7 DDoS (combat-verified)**: RR-1 — disclosed by Google 2023-10: peak request rate exceeded any attack in history; AWS/Cloudflare confirmed simultaneously
- **Mitigation bypass**: RR-2/RR-3 — both "cheap mitigations" (frequency thresholds and per-stream rejection) were proven bypassable
- **Backend amplification**: post-edge cost of processing canceled requests at the backend (HEADERS parsing / HPACK decoding / routing)

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2023-44487** | Entire HTTP/2 ecosystem: nghttp2 <1.57, Netty <4.1.100, Envoy, Go x/net, Jetty, Caddy <2.7.5, F5, etc. | Rapid Reset: RST_STREAM releases the concurrency slot instantly while the server pays parsing/scheduling cost per canceled request; fix = connection-level work budget + forced GOAWAY close on trigger |
| **Variant empirics (Google disclosure)** | Implementations with improper mitigations | Batched delayed cancel bypasses frequency thresholds; over-limit opens exploit lenient per-stream rejection — the two variants forced mitigation design toward "connection-behavior holistic judgment" |
| Lesson migration | H3 stacks | Official conclusion: no direct evidence for H3 but proactive mitigation recommended — maps to the H3-side `rfc9000-stream-reset-cancel` in this library; the two skills cross-reference each other |

## 5. Differential Verification

Control group: nghttp2 ≥1.57 (work budget + forced close).
Comparison fields: RR-1 single-connection injection-rate ceiling, RR-2/RR-3 close behavior under variants, RR-4 GOAWAY latency (must be immediate after trigger).
False-positive exclusion: browser navigation cancellation is legitimate open-then-reset — **judgment must be based on connection-level patterns** (joint thresholds on frequency + total + work), and single-frame behavior is not a violation; this is the lesson the CVE taught the whole industry, and the audit must not regress on it.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (request-cancel storm timing), `fuzzowski-network-fuzz` (RST/HEADERS interleave fuzzing)
- Tool layer (what to attack with): nghttp (-m concurrency variants), custom h2 client (frame-level timing), server CPU/allocation sampling
- Post-hit actions: quantify single-connection work-injection rate → re-test mitigations under variants 1/2 → output the "connection-level budget missing" evidence and merge with the H3-side skill into a cross-version Rapid Reset family
