---
name: rfc9113-stream-state-machine
description: Audit HTTP/2 stream-state-machine handling of illegal frame transitions — DATA on a half-closed(remote) stream and similar violations must be answered with STREAM_CLOSED, and manufacturing them in bulk becomes the MadeYouReset resource drain (CVE-2025-5115 Jetty GHSA-mmxm-8w33-wc4h); the HEADERS+RST_STREAM race with double callbacks and double cleanup can cause double-free (Apache h2_mplx.c, disclosed 2026); the RST_STREAM refused-stream path forcing an in-scope write can cause heap UAF (CVE-2026-56848 Node.js, fixed in commit ba6cb5c); sustained RST floods leaking memory on connection close (CVE-2023-45802 Apache); RFC 9113 §5.1 transition table is the audit anchor, but correct convergence of "legitimate RST interleaved with race frames" rests entirely on the implementation
zh-signals: 审计 HTTP/2 流状态机对非法帧迁移的处置——half-closed(remote) 收 DATA 等违规帧必须回 STREAM_CLOSED，攻击者批量制造即 MadeYouReset 资源消耗（CVE-2025-5115 Jetty GHSA-mmxm-8w33-wc4h）；HEADERS+RST_STREAM 竞态双回调双清可致 double-free（Apache h2_mplx.c，2026 披露）；RST_STREAM 的 refused-stream 路径在作用域内强制写可致堆 UAF（CVE-2026-56848 Node.js，修复 commit ba6cb5c）；持续 RST 洪流致连接关闭内存泄漏（CVE-2023-45802 Apache）；RFC 9113 §5.1 状态迁移表是判定锚点，但"合法 RST 与竞态帧交错"的正确收敛全靠实现
rfc: RFC 9113 §5.1（流状态）/ §5.4（错误处理）/ §6.4（RST_STREAM）
license: Apache-2.0
---

# RFC 9113 §5.1 Stream State-Machine Illegal-Transition Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §5.1 (key points):
> An idle stream receiving anything other than HEADERS/PRIORITY → connection error PROTOCOL_ERROR; a half-closed(remote) stream receiving anything other than WINDOW_UPDATE/PRIORITY/RST_STREAM → **stream error STREAM_CLOSED**; reserved streams sending/receiving out-of-bounds frames → connection error.

RFC 9113 §5.1.1 (key points):
> Stream IDs must not be reused; WINDOW_UPDATE on closed streams may be ignored (grace period), all other frames get STREAM_CLOSED.

Core pattern in one sentence: **the H2 stream state machine is a clear transition table, but every illegal transition that "must be answered with an error" is a resource expense for the server — an attacker mass-manufacturing illegal frames makes the server run error-handling paths (allocating RSTs, running callbacks, doing cleanup) on its behalf: that is MadeYouReset. More dangerous is the legitimate-frame race: HEADERS immediately followed by RST_STREAM, two callbacks each cleaning up the same object — the state machine is correct but lifecycle management double-frees. The audit checks both "is illegal-frame disposition compliant" and "is the cost of compliant disposition clamped", plus "does race convergence have a dedup guard."**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| SS-1 | Bulk-send DATA on half-closed(remote)/closed streams | Not handled as STREAM_CLOSED, or disposition cost grows linearly without bound → same class as CVE-2025-5115 (also test whether the cost is exempted from the concurrency cap) |
| SS-2 | Send DATA/SETTINGS-class stream frames on an idle stream (no stream opened) | Not disconnected with PROTOCOL_ERROR connection error → §5.1 idle disposition missing |
| SS-3 | HEADERS + immediate RST_STREAM on the same stream (non-zero error code) in a high-speed loop | Memory error on the race path (double-free/UAF) or duplicate cleanup → same class as Apache 2026 / Node.js |
| SS-4 | Stream-ID wraparound reuse (reuse old IDs past 2^31) | Implementation fails to prevent reuse → §5.1.1 ID-uniqueness lost (long-connection attack surface) |
| SS-5 | DATA received on a reserved(local) stream (illegal) | Not handled as a connection error → push state-machine violation |
| SS-6 | Frames sent to a stream after trailers (END_STREAM HEADERS) | State-convergence error → trailing-frame sequence defect (parallel to the H3-side trailers skill) |

Method: frame-level scripts walking the illegal-transition matrix by state; high-speed loops to measure resource slopes; heap checkers (ASan/jemalloc sampling) to catch race memory errors.

## 3. Attack-Surface Hypotheses

- **Memory corruption**: SS-3 — double-free/UAF can escalate into an RCE prerequisite (Apache h2_mplx double cleanup and the Node.js in-scope RST submission are both empirical)
- **Resource-consumption DoS**: SS-1 — the error-handling path itself weaponized (MadeYouReset family, fixed across all Jetty branches)
- **Long-lived connection state pollution**: SS-4/SS-6 — stream-ID reuse or trailing-frame convergence errors cause cross-request state cross-talk (evolving toward request smuggling)

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2025-5115** | Eclipse Jetty ≤9.4.57/≤10.0.25/≤11.0.25/≤12.0.21 (GHSA-mmxm-8w33-wc4h, MadeYouReset) | Client sends illegal frames (zero-increment WINDOW_UPDATE, DATA on closed streams) → server compliantly returns RST_STREAM → the cost is not counted against the concurrency cap → rapid stream creation exhausts resources |
| **CVE-2026-56848** | Node.js (fixed in commit ba6cb5c "http2: defer rst stream while in scope") | The refused-stream path forces SendPendingData inside the nghttp2 scope → heap use-after-free; CVSS 7.5 |
| Apache double-free (disclosed 2026, h2_mplx.c) | Apache httpd mod_http2 | HEADERS+RST_STREAM race: nghttp2's double callbacks each call m_stream_cleanup, putting the same h2_stream pointer into the purge list twice → apr_pool double free |
| **CVE-2023-45802** | Apache httpd | Rapid-Reset family: memory leak on the connection-close path, cumulative exhaustion under sustained attack |

## 5. Differential Verification

Control group: patched Jetty (versions specified in GHSA-mmxm-8w33-wc4h); Node.js versions containing ba6cb5c.
Comparison fields: SS-1 error-code correctness and cost slope, SS-3 race window (heap-error detection rate over 1e5 repetitions), SS-4 ID-reuse protection.
False-positive exclusion: an implementation returning STREAM_CLOSED but with a connection-level circuit breaker on such frames → passes; correct error disposition with cost comparable to the patched version → passes.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (state × frame-type matrix fuzzing), `slowhttptest-dos` (illegal-frame slow streams)
- Tool layer (what to attack with): Python h2 frame-level construction + ASan/Valgrind detection on the target side
- Post-hit actions: SS-3 confirmed → immediately escalate to memory-corruption exploitation assessment (paired with the C46 binary-exploitation skill class) → archive the minimal triggering sequence; SS-1 confirmed → measure incapacitation parameters of "illegal-frame rate × resource consumption"
