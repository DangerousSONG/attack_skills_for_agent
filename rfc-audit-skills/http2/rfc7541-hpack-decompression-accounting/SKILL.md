---
name: rfc7541-hpack-decompression-accounting
description: Audit the resource-accounting model on the HPACK decode side — the 4KiB dynamic-table cap does not cover per-entry materialization during decoding; index-reference amplification (1-byte reference → full header copy) combined with per-entry bookkeeping overhead becomes an HTTP/2 Bomb (CVE-2026-49975 Apache httpd / CVE-2026-47774 Envoy, full stack nginx/IIS/Pingora, 32GB in 20 seconds per connection); classic HPACK Bomb lineage CVE-2016-6581 (python-hpack) / CVE-2016-1544 (nghttpd) / CVE-2025-53020 (Apache ~4000x) / CVE-2026-10725 (Perl Protocol::HTTP2 advertises header-list limit but never enforces it); RFC 7541 §7.3 empirically proven to be a specification defect — decompressed size and header-field count are two independent limits, and an implementation needs both
zh-signals: 审计 HPACK 解码侧的资源记账模型——动态表 4KiB 上限管不住解码过程中的逐条目物化分配，索引引用放大（1 字节引用 → 全量头副本）与逐条目簿记开销叠加即成 HTTP/2 Bomb（CVE-2026-49975 Apache httpd / CVE-2026-47774 Envoy，nginx/IIS/Pingora 全栈，单连接 20 秒 32GB）；经典 HPACK Bomb 谱系 CVE-2016-6581（python-hpack）/CVE-2016-1544（nghttpd）/CVE-2025-53020（Apache 4000x）/CVE-2026-10725（Perl Protocol::HTTP2 头列表上限通告不执行）；RFC 7541 §7.3 被实证为规范缺陷——解码后大小与头字段数是两个独立上限，实现缺一不可
rfc: RFC 7541 §7.3（内存消耗，已实证缺陷条款）/ §4.1（条目尺寸记账）+ RFC 9113 §6.5.2（SETTINGS_MAX_HEADER_LIST_SIZE）
license: Apache-2.0
---

# RFC 7541 §7.3 / RFC 9113 §6.5.2 HPACK Decode Resource-Accounting Audit

## 1. Normative Clauses (Original Sources)

RFC 9113 §6.5.2 (key points):
> After advertising `SETTINGS_MAX_HEADER_LIST_SIZE`, an endpoint **MUST treat a received header list that exceeds the advertised limit as a stream error or connection error**.

RFC 7541 §7.3 (key points, empirically proven defective):
> An attacker can cause an endpoint to exhaust memory. HPACK limits dynamic-table memory via SETTINGS_HEADER_TABLE_SIZE… (this one sentence, assuming the problem is solved).

Core pattern in one sentence: **§7.3 frames memory risk in terms of "compression ratio", but the 2026 HTTP/2 Bomb proved this model wrong — a single nearly-empty header (tiny decompressed size, decompression never triggers any limit) can still make the server pay per-entry bookkeeping overhead (pool blocks, structs, NUL-terminated copies) for every entry, with amplification factors from 68:1 (IIS) to 5700:1 (Envoy). Five independent implementation teams read the same spec paragraph and made the same mistake, so the audit point is not "is there a limit" but "which layer of memory does the limit govern." Decompressed total size and header-field count are two independent limits; missing either one is a hole.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| HA-1 | Thousands of "index references to the same large cookie entry" (1 byte per reference) within a single header block | Server materializes a full copy per reference and the header-list total limit does not stop it → HTTP/2 Bomb phase 1 holds |
| HA-2 | Thousands of independent small header fields in a single header block (total below the decompressed-size limit) | No field-count limit → bookkeeping amplification bypasses the size limit (the Calif variant core) |
| HA-3 | Header list exceeds the advertised SETTINGS_MAX_HEADER_LIST_SIZE | Not rejected as a stream error → §6.5.2 advertise/enforce inconsistency (same class as CVE-2026-10725: advertises 65536 but the decoder never checks) |
| HA-4 | Huffman-encoded tiny on-wire payload expands into a large string (compression ratio >100:1) | No string-level limit after expansion → the field-level dimension complementary to `rfc7541-hpack-decode-limit` |
| HA-5 | HA-1/HA-2 combined with flow-control holds (INITIAL_WINDOW_SIZE=0) | Buffer cannot be released → full chain holds; compare against the CVE-2026-49975 reproduction table |

Method: hand-craft header blocks with python-hpack; observe per-request server memory increments; test the "size limit" and "field-count limit" dimensions separately.

## 3. Attack-Surface Hypotheses

- **Memory-exhaustion DoS**: HA-1/HA-2/HA-5 — the currently highest-risk H2 attack class, hitting five major implementations simultaneously in 2026-06
- **Advertise/enforce divergence fingerprint**: HA-3 — a SETTINGS-advertised value that is not actually enforced exposes the stack and version
- **Field-count smuggling**: HA-2 — when a WAF/gateway quotas by byte count, massive numbers of small header fields can bypass audit rules

## 4. Related Historical CVEs

| CVE | Implementation | Root Cause |
|---|---|---|
| **CVE-2026-49975 / CVE-2026-47774** | Apache httpd (mod_http2 <2.0.41) / Envoy / nginx (1.29.8 max_headers fix) / IIS / Cloudflare Pingora (RHSB-2026-007, disclosed 2026-06-02 by Calif, discovered with OpenAI Codex assistance) | Per-entry bookkeeping overhead not covered by the dynamic-table budget + zero-window holds pinning memory; amplification 68:1–5700:1; ~880K public websites exposed |
| **CVE-2026-10725** | Perl Protocol::HTTP2 <1.13 | Inbound HPACK has no header-list limit: SETTINGS advertises MAX_HEADER_LIST_SIZE default 65536 but the decode path never consults it; CONTINUATION buffering accumulates without bound |
| **CVE-2025-53020** | Apache httpd (Gal Bar Nahum, ~4000x amplification) | Prelude to the HTTP/2 Bomb: amplification via compressed-header expansion and residency |
| **CVE-2016-6581 / CVE-2016-1544** | python-hpack <2.3.0 / nghttpd, nghttp, libnghttp2_asio | Classic HPACK Bomb: fill the dynamic table with large entries then reference them thousands of times, 16KB on the wire → 64MB decoded; boundary case where the nghttp2 library itself is unaffected (application-layer obligation) |

## 5. Differential Verification

Control group: nginx ≥1.29.8 (max_headers field-count limit) and mod_http2 ≥2.0.41 (patched) as the dual-limit benchmark.
Comparison fields: HA-1 per-reference materialization cost, HA-2 field-count limit value, HA-3 advertise/enforce consistency, HA-5 combined amplification factor with flow-control holds.
False-positive exclusion: an implementation with an extremely high field-count limit (e.g., 2^20) still counts as a violation (a DoS floor set too low is what matters); an implementation limiting by decompressed size with field count indirectly constrained by size (large fields squeeze the count) → passes HA-1 but HA-2 still requires empirical testing.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (HPACK header-block mutation), `dharma-grammar-fuzz` (entry-count / reference-pattern combination generation)
- Tool layer (what to attack with): python-hpack hand-encoding, the public CVE-2026-49975 reproduction project (razureink/cve-2026-49975-http2bomb_reproduction) as the control baseline
- Post-hit actions: HA-2 confirmed → test the "field count × entry size" amplification matrix → rate against the five-implementation fix table → combine with `rfc9113-flow-control-window-stall` for the full chain
