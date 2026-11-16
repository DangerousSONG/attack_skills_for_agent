---
name: rfc9113-continuation-header-limit
description: Audit HTTP/2 implementations' enforcement of CONTINUATION frames and header-block size limits — buffering unbounded oversized header blocks just to return a 413, or END_HEADERS never set, leads to memory-exhaustion DoS (related CVE-2024-27316 Apache httpd 2.4.17-2.4.58 nghttp2 buffering memory exhaustion; CERT VU#421644 frame-class disclosure; CVE-2024-24549 Tomcat and CVE-2024-30255 Envoy sibling variants)
zh-signals: 审计 HTTP/2 实现 CONTINUATION 帧与头块大小限制执行是否安全——超限头块为生成 413 而无界缓冲、END_HEADERS 永不置位即内存耗尽 DoS（关联 CVE-2024-27316 Apache httpd 2.4.17-2.4.58 nghttp2 缓冲内存耗尽；CERT VU#421644 帧类；CVE-2024-24549 Tomcat、CVE-2024-30255 Envoy 同族变体）
rfc: RFC 9113 §6.10（HEADERS/CONTINUATION 序列）/ §6.5.2（SETTINGS_MAX_HEADER_LIST_SIZE）/ RFC 7540 §10.5.1（头块上限）
license: Apache-2.0
---

# RFC 9113 §6.10 CONTINUATION Frames and Header-Block Limit Enforcement Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §6.5.2 (key points):
> SETTINGS_MAX_HEADER_LIST_SIZE (0x06) advertises the **uncompressed** header-list size the endpoint is willing to accept (each field name+value octet count + 32 octets overhead per field); an exceeding message is **malformed** and should be rejected.

RFC 9113 §6.10 (key points):
> A header block consists of HEADERS + any number of CONTINUATION frames; no other frame may appear until END_HEADERS is set on the sequence; CONTINUATION may only follow a mid-header-block frame.

RFC 7540 §10.5.1 (key points):
> Intermediaries and endpoints MUST be able to impose a limit on header-block size — implementations may enforce a value lower than the peer's advertised one, but the post-limit error-handling path must be **bounded**.

Core pattern in one sentence: **the root cause of this CVE class is not "no limit" but "the over-limit error-handling path is unbounded" — to give the client a polite 413, the server first buffers the attacker's infinite stream. Good intentions became the amplifier.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| CT-1 | After establishing a connection, send HEADERS (END_HEADERS unset), then keep sending CONTINUATION frames forever (END_HEADERS never set); observe server RSS | Memory grows without a hard cap → same class as CVE-2024-27316 (unbounded 413 buffering path) |
| CT-2 | Keep sending CONTINUATION after the header block exceeds SETTINGS_MAX_HEADER_LIST_SIZE | Server does not disconnect/reset at the limit point but keeps receiving and buffering → bounded-execution-path violation |
| CT-3 | Insert a non-CONTINUATION frame (PING/DATA) mid-CONTINUATION-sequence | Not disconnected as a protocol error → frame-sequence validation missing |
| CT-4 | Interleave across streams: send stream B's HEADERS while stream A's header block is unfinished | Not rejected → implementation allows header-block interleaving, enlarged state surface |
| CT-5 | Trailing extra CONTINUATION after the header block completes | Not rejected → sequence-termination validation missing |

Method: custom H2 client (frame-level control under the h2 library); RSS sampling + measurement of the delay until the 413 response arrives.

## 3. Attack-Surface Hypotheses

- **Single-connection memory-exhaustion DoS**: CT-1 — the discoverer's assessment: more resource-efficient than Rapid Reset; a single TCP connection can crash some implementations
- **Header-parse state-surface enlargement**: CT-3/CT-4 — decoder state-machine confusion under interleaved sequences → crash/UAF family
- **Header-block boundary confusion**: CT-5 — miscounted boundaries leave seams for parse splits

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2024-27316** | Apache httpd 2.4.17–2.4.58 (nghttp2, CVSS 7.5) | Oversized headers temporarily buffered to produce a 413; if the client never stops, buffering is unbounded → memory exhaustion. Fix: terminate once the parse-error threshold is crossed (httpd commit 0d73970ec161) |
| **CVE-2024-24549** | Apache Tomcat | Request exceeding the header limit not reset before all headers are processed — sibling variant |
| **CVE-2024-30255** | Envoy (nghttp2 integration surface) | Unbounded resource consumption in CONTINUATION handling, same family |
| CERT VU#421644 | Frame-class disclosure (Bartek Nowotarski, 2024-04) | CONTINUATION Flood disclosed as a **frame class**: not limited to Apache, a generic H2 implementation weakness |

## 5. Differential Verification

Control group: httpd ≥2.4.59 (fixed version: error-count threshold termination), nghttp2 ≥1.61 (if it includes frame-count cap logic).
Comparison fields: CT-1 RSS ceiling, CT-2 disconnect timing (must be at the limit, not after buffering), CT-3/CT-4/CT-5 rejection rates.
False-positive exclusion: a server that disconnects normally after N frames with bounded RSS is a compliance policy difference; only "unbounded buffering" and "sequence-validation missing" are judged violations.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `slowhttptest-dos` (single-connection slow header-block stream mode), `fuzzowski-network-fuzz` (CONTINUATION sequence grammar fuzzing)
- Tool layer (what to attack with): Python h2 library (frame-level control), RSS sampling scripts, CVE-2024-27316 PoC reference implementation
- Post-hit actions: measure per-connection memory injection rate → minimize the CT-1 reproducing frame sequence → assess multi-connection concurrent amplification (memory-exhaustion slope × connection count)
