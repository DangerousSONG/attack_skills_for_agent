---
name: rfc9113-priority-tree-abuse
description: Audit whether HTTP/2 priority-tree implementations resist resource exhaustion via cycles — continuously reshuffling priorities across many streams churns the tree structure and exhausts CPU (CVE-2019-9513 Resource Loop: nghttp2/nginx/netty/undertow full-stack impact, CVSS 7.5, fixed in nghttp2 1.39.2); RFC 9113 §5.3 permits implementations to deprioritize processing (blank-clause escape), but "if you keep it, it must resist churn" — the audit target is the boundedness of the priority state machine
zh-signals: 审计 HTTP/2 优先级树实现是否抗资源循环——多流持续打乱优先级造成树结构搅动即可 CPU 耗尽（CVE-2019-9513 Resource Loop：nghttp2/nginx/netty/undertow 全栈波及，CVSS 7.5，nghttp2 修复版 1.39.2）；RFC 9113 §5.3 允许实现放弃优先级处理（留白条款），但"保留实现就必须抗搅动"，审计对象是优先级状态机的有界性
rfc: RFC 9113 §5.3（流优先级）/ §5.3.1（依赖）/ RFC 7540 §5.3
license: Apache-2.0
---

# RFC 9113 §5.3 Priority-Tree Resource-Loop Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §5.3 (key points):
> Endpoints may **decline to process priority frames**; maintaining the priority tree is an implementation optimization, but if an implementation maintains the tree, dependency updates must be protected by cycle detection.

Core pattern in one sentence: **PRIORITY frames are low-cost "tree-reordering instructions" — an attacker shuffles dependencies across many streams to churn the tree, and if the implementation maintains a full tree with O(n) cost per reorder, low bandwidth saturates the CPU. The RFC explicitly allows not doing priorities at all (a legal escape hatch), so the audit first asks "did you implement it", and only if yes checks "is what you built bounded."**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| PT-1 | Open N streams (N=100+), cyclically send PRIORITY frames swapping dependency relationships (shuffle pattern) | CPU climbs linearly with frame rate, no throttling/coalescing → same class as CVE-2019-9513 Resource Loop |
| PT-2 | Build a dependency cycle (A→B→A) then keep adding reorders | No cycle detection, or detection fails and hangs → §5.3.1 dependency correctness missing |
| PT-3 | Send PRIORITY to an idle/closed stream (nonexistent stream or server-initiated stream) | Not ignored or mis-handled per spec → §5.3 tolerance obligation for PRIORITY targeting any stream state |
| PT-4 | PRIORITY frame flood mixed with normal requests | Normal-request latency degrades more than 2x over baseline → scheduling fairness lost (DoS already holds, no need to saturate) |
| PT-5 | A single frame declaring a dependency on itself (a stream depending on itself) | Not rejected / no disconnect → tree-consistency validation missing |

Method: h2 client with multi-stream concurrency + PRIORITY shuffle loops; observe server CPU and normal-request P99 latency; control group is the no-PRIORITY baseline.

## 3. Attack-Surface Hypotheses

- **CPU-exhaustion DoS**: PT-1 — a single low-bandwidth connection saturates the event loop (full-stack impact in the 2019 Netflix/CERT disclosure)
- **Scheduling manipulation**: PT-4 — no need to exhaust resources; merely degrading priority scheduling starves the target traffic (an L7 QoS-attack equivalent)
- **Fingerprint**: PT-3/PT-5 error-handling differences can distinguish implementation stacks and versions

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2019-9513** | nghttp2 (fixed 1.39.2), nginx, netty, undertow, Node.js | Priority-tree churn exhausts CPU; nginx fix commit 5ae726912654; Red Hat RHSA-2019:2745 batch fixes; CVSS 7.5 / CWE-400 |
| Blind-spot declaration | Same family, TBD | The RFC allows dropping priorities — some implementations choose "no tree" and are immune; every implementation that maintains a tree must prove bounded reorder cost. This skill is flagged as a **must-check on legacy stacks** |

## 5. Differential Verification

Control group: nghttp2 ≥1.39.2 (throttling/coalescing against priority churn); nginx ≥1.17.3 (2019-08 patch batch).
Comparison fields: PT-1 CPU-curve slope, PT-2 cycle detection, PT-4 normal-request P99 degradation factor.
False-positive exclusion: an implementation declaring "no priority processing" whose behavior on receiving PRIORITY frames is correct (ignored or only tallied) → passes; an implementation with a tree but lazy/merged reordering → passes.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (slow PRIORITY stream mode), `fuzzowski-network-fuzz` (PRIORITY field mutation)
- Tool layer (what to attack with): Python h2 (multi-stream + frame-level PRIORITY construction), CPU/latency sampling scripts
- Post-hit actions: PT-1 confirmed → measure the "single-connection saturation threshold frame rate" → assess multi-connection amplification and the stock of pre-2019 disclosed stack versions (nginx below 1.17.3 is fully vulnerable at scale)
