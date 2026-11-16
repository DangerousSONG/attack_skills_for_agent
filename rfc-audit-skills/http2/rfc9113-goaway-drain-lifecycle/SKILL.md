---
name: rfc9113-goaway-drain-lifecycle
description: Audit the HTTP/2 connection-termination lifecycle (GOAWAY draining and RST_STREAM races) — concurrent RST_STREAM and GOAWAY triggering a write-pipeline race can permanently block worker threads until the thread pool is exhausted (CVE-2026-12611 Jetty GHSA-gpg9-4257-cfm3: HTTP2Flusher.terminated reset to null by the race, queued items never processed); nginx graceful shutdown leaking GOAWAY on H2 connections causes worker hangs (2024-05 kaseiwang patch + http2-grace-shutdown-test PoC); RFC 9113 §6.8 defines the double-GOAWAY graceful-shutdown sequence, but the race window and termination one-way-sink are implementation obligations
zh-signals: 审计 HTTP/2 连接终止生命周期（GOAWAY draining 与 RST_STREAM 竞态）——RST_STREAM 与 GOAWAY 并发触发写管线竞态可致工作线程永久阻塞直至线程池耗尽（CVE-2026-12611 Jetty GHSA-gpg9-4257-cfm3：HTTP2Flusher.terminated 被竞态重置为 null，入队项永不处理）；nginx 优雅关闭时 H2 连接漏发 GOAWAY 致 worker 卡死（2024-05 kaseiwang 补丁 + http2-grace-shutdown-test PoC）；RFC 9113 §6.8 规定双 GOAWAY 优雅关闭序列但竞态窗口与终止单向性是实现义务
rfc: RFC 9113 §6.8（GOAWAY）/ §6.4（RST_STREAM）/ §5.1（流状态机）
license: Apache-2.0
---

# RFC 9113 §6.8 GOAWAY Draining and Termination-Race Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §6.8 (key points):
> GOAWAY carries a last-stream-ID; in-flight streams with larger IDs **may** be retried by the sender; endpoints **should** first send a GOAWAY with last-stream-ID at maximum value, wait at least 1 RTT, then send a second GOAWAY carrying the real last-stream-ID (the graceful-shutdown sequence).

Core pattern in one sentence: **connection termination is the easiest path in the H2 state machine to write races into — GOAWAY says "no new streams", old streams still run during draining, and RST_STREAM can barge in anytime to chop half the state. The RFC gives the double-GOAWAY sequence, but the invariant "termination is a one-way transition" is guarded entirely by the implementation; once some concurrent path can reset the terminated flag back, the write pipeline deadlocks forever.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| GD-1 | Concurrently interleave RST_STREAM and GOAWAY (multi-stream interleave, multi-connection amplification) | Worker threads grow monotonically with repetitions and never recover → same class as CVE-2026-12611 (thread dump shows flusher blocked stack) |
| GD-2 | After GOAWAY, continue opening new streams above last-stream-ID | Server does not ignore / does not sequence them → §6.8 last-stream-ID semantics missing |
| GD-3 | Open a slow connection at the instant of server graceful shutdown (reload/restart signal) | Connection leaks GOAWAY or never enters closing → same class as nginx 2024, worker stuck at shutting down |
| GD-4 | After receiving GOAWAY, send a second GOAWAY with a different last-stream-ID (double-GOAWAY sequence) | Implementation does not support double GOAWAY or treats the second as an error → graceful-shutdown sequence incompatible (interoperability defect) |
| GD-5 | Send RST_STREAM to half-closed streams during draining | Stream state machine does not converge correctly → §5.1 state-transition defect (stuck streams hold resources) |

Method: h2 client concurrent frame scripts + signal injection like `nginx -s reload`; observe thread count / connection close time; thread dumps to locate blocked stacks.

## 3. Attack-Surface Hypotheses

- **Thread-pool-exhaustion DoS**: GD-1 — no high bandwidth needed; precisely timed RST/GOAWAY interleaving can wipe out Jetty-class thread-pool models
- **Graceful-shutdown hijacking**: GD-3 — slow connections pin the publish/restart window, an operations-level DoS (amplified in rolling-release scenarios)
- **Draining resource residency**: GD-2/GD-5 — new streams after GOAWAY are ignored but the connection stays up; connection table / stream table occupied by draining connections for a long time

## 4. Related Historical CVEs

| CVE / Empirical Finding | Implementation | Root Cause |
|---|---|---|
| **CVE-2026-12611** (GHSA-gpg9-4257-cfm3) | Eclipse Jetty jetty-http2-server | The RST_STREAM × GOAWAY race resets HTTP2Flusher.terminated back to null → queued items never processed; blocked writes accumulate until the thread pool exhausts and the service stops entirely; CWE-400; fixed across all version branches (9.x/10.x/11.x/12.x) |
| nginx graceful-shutdown defect (2024-05, kaseiwang) | nginx (freenginx patch discussion, commit 7f18358cc) | Time race between `ngx_close_idle_connections` and `ngx_http_v2_init` → some H2 connections get c->idle set after the close scan, GOAWAY never sent, worker stuck at shutting down; PoC repo http2-grace-shutdown-test (15-second slow connection + reload to reproduce) |
| SwiftNIO design discussion (2024-02) | SwiftNIO | GOAWAY and client-initiated new streams race by nature → the community adopted the "GOAWAY(max) + PING + 1RTT + GOAWAY(real)" double-GOAWAY scheme (implementation reference for the RFC-recommended sequence) |

## 5. Differential Verification

Control group: patched Jetty (versions specified in GHSA-gpg9-4257-cfm3); nginx with the 7f18358cc patch applied.
Comparison fields: GD-1 recoverable thread count, GD-3 shutdown-completion time, GD-4 double-GOAWAY compatibility.
False-positive exclusion: an implementation that brutally disconnects on receiving GOAWAY (no double GOAWAY) → ungraceful but not a violation; record as interoperability defect, not security; GD-1 with 1000 repetitions and no thread growth → passes.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (slow connections + signal-window stacking), `fuzzowski-network-fuzz` (RST/GOAWAY interleave timing mutation)
- Tool layer (what to attack with): Python h2 concurrent frame construction, JVM thread dumps / nginx worker-state observation
- Post-hit actions: GD-1 confirmed → measure thread-consumption rate and trigger-window probability → output minimal "connections × repetitions" incapacitation parameters; GD-3 confirmed → correlate with the release process for an attack-window assessment
