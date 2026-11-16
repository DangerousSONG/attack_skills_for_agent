---
name: rfc7541-hpack-decode-limit
description: Audit whether the HPACK decoder bounds integer/string representations — overlong integer encodings and oversized string literals must be treated as decoding errors, otherwise a single header block can exhaust memory or bypass length limits (CVE-2026-59248 cowlib HPACK/QPACK integer-decoder memory-exhaustion DoS; Jetty OSTIF audit TOB:JETTY-1 HpackDecoder integer overflow past maxHeaderSize; h2o issue #3602 accepts overlong varint while nghttp2/ls-hpack reject it — a compliance divergence that bypasses length limits); RFC 7541 §5.1/§5.2/§7.4 explicitly place the burden of limits on the implementation (blind-spot clause)
zh-signals: 审计 HPACK 解码器整数/字符串表示是否有界——超长整数编码、超长字符串字面量必须按解码错误处理，否则单头块即可撑爆内存或绕过长度限制（CVE-2026-59248 cowlib HPACK/QPACK 整数解码内存耗尽 DoS；Jetty OSTIF 审计 TOB:JETTY-1 HpackDecoder 整数溢出超 maxHeaderSize；h2o issue #3602 接受超长 varint 而 nghttp2/ls-hpack 拒绝，属可绕过长限制的合规分歧点）；RFC 7541 §5.1/§5.2/§7.4 明确"实现必须自设上限"（盲区条款）
rfc: RFC 7541 §5.1（整数表示）/ §5.2（字符串字面量）/ §7.4（实现上限义务）
license: Apache-2.0
---

# RFC 7541 §5.1/§5.2 HPACK Decode-Boundedness Audit

## 1. Normative Clauses (Original Sources)

RFC 7541 §5.1 (key points):
> Integer representations allow arbitrarily large values; an encoder can send long runs of zero-value bytes to waste bandwidth and to enable integer overflow. **Integer encodings whose value or encoding length exceeds the implementation's limit MUST be treated as a decoding error.**

RFC 7541 §7.4 (key points):
> Implementations MUST set limits on the **integer values, integer encoding lengths, and string literal lengths** they accept.

Core pattern in one sentence: **HPACK integers are variable-length varints (7 bits per group, theoretically unbounded), and string length fields are likewise unbounded — the RFC delegates all limits entirely to the implementation. That makes the decoder a memory amplifier. The audit target is not "which MUST is violated" but "have you set the three limits (value / encoding length / string length), where, and can an overlong encoding bypass them."**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| HD-1 | Send an HPACK integer (e.g., an indexed `:path` field) with an encoding length of 11+ bytes (prefix value deliberately low-padded) | Not treated as a decoding error (accepted or silently truncated) → §5.1 limit obligation missing; overlong encoding can bypass the outer header-length limit |
| HD-2 | Send a string literal (name or value) with a declared length of 16MB+ | Not rejected as a stream/decoding error, or fully allocated before validation → memory amplification (4-byte length field on the wire drives a 16MB allocation off it) |
| HD-3 | Integer-decoding accumulator overflows (craft prefix + consecutive 0xFF bytes to wrap the accumulator) | Small value passes after overflow, or enters a negative-length path → same class as Jetty TOB:JETTY-1 |
| HD-4 | Alternate overlong encodings with legitimate fields within a single header block | Per-field processing with no aggregate accounting → a single header block bypasses per-field limits (a header-block-level cumulative limit is required) |
| HD-5 | Send a legitimate request after an overlong encoding | Connection not closed, or decoder state not reset → error-recovery path defect |

Method: hand-craft HPACK byte streams with the Python h2/hpack library (bypassing the high-level API's length checks); observe server memory allocation peaks and connection survival.

## 3. Attack-Surface Hypotheses

- **Memory-exhaustion DoS**: HD-2 — low bandwidth (a few bytes of length field) triggers a large allocation; the cowlib finding shows the HPACK/QPACK decode paths are shared
- **Length-limit bypass**: HD-1 — an overlong varint encoding a small value bypasses naive WAF/gateway length caps based on encoded length, and the decoded value processed downstream creates a smuggling divergence
- **Integer overflow → out-of-bounds read/write**: HD-3 — accumulator overflow can lead to negative-length memcpy (TOB:JETTY-1 rated Medium/DoS; heap overflow can escalate)

## 4. Related Historical CVEs

| CVE / Audit Finding | Implementation | Root Cause |
|---|---|---|
| **CVE-2026-59248** | cowlib (Erlang, Cowboy server) | HPACK/QPACK integer decoder has no memory bound → decoding memory-exhaustion DoS; reproducible Docker lab + exploit client available |
| **TOB:JETTY-1** (Trail of Bits OSTIF Jetty audit 2023) | Eclipse Jetty HpackDecoder | Integer-overflow risk lets decoding exceed the maxHeaderSize limit (Medium, fixed and re-verified) |
| h2o/h2o#3602 (2026-06 empirical) | h2o | HPACK decoder accepts overlong integer encodings while nghttp2 and ls-hpack reject them → inter-implementation compliance divergence; can bypass length limits / confuse header content |

## 5. Differential Verification

Control group: nghttp2 ≥1.44 (rejects overlong integer encodings outright); patched h2o.
Comparison fields: whether HD-1 is rejected and with which error code (COMPRESSION_ERROR); HD-2 allocate-before-check vs check-before-allocate; HD-3 overflow handling; HD-5 connection disposition.
False-positive exclusion: an implementation that accepts overlong encodings but enforces a header-block-level total-byte limit checked before allocation → passes (limit placed differently but equivalent).

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (HPACK byte mutation), `dharma-grammar-fuzz` (combinations of integer/string length fields)
- Tool layer (what to attack with): python-hpack hand-encoded byte streams, memory sampling scripts (tracemalloc / jmap)
- Post-hit actions: HD-2 confirmed → measure per-connection memory amplification factor and time-to-OOM → assess blast radius on shared gateways (cowlib/Cowboy family)
