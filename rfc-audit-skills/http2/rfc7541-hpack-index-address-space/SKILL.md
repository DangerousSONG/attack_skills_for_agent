---
name: rfc7541-hpack-index-address-space
description: Audit HPACK index address-space (static table 61 entries + dynamic table) boundary and lifecycle consistency — out-of-bounds index reads crash remotely (CVE-2018-14645 HAProxy <1.8.14 hpack_valid_idx() OOB-read DoS, CWE-125, RHSA-2018:2882); before a SETTINGS_HEADER_TABLE_SIZE=0 advertisement takes effect the encoder is entitled to use the 4096-default table, and a decoder that rejects early becomes an interoperability bomb (Zephyr #124221, 2026-11 empirical — Chrome/Firefox first-screen bursts all fail); index references to evicted entries must be decoding errors (RFC 7541 §4.3/§2.3.3); RFC 7541 §2.3.3 address-space semantics + §4.2/§6.3 capacity-negotiation timing are the audit anchors
zh-signals: 审计 HPACK 索引地址空间（静态表 61 项 + 动态表）的边界与生命周期一致性——索引越界读直接远程崩溃（CVE-2018-14645 HAProxy <1.8.14 hpack_valid_idx() 越界读 DoS，CWE-125，RHSA-2018:2882）；SETTINGS_HEADER_TABLE_SIZE=0 通告生效前编码器有权使用 4096 默认表，解码器提前拒绝即互操作炸弹（Zephyr #124221 2026-11 实证：Chrome/Firefox 首屏突发全挂）；动态表驱逐后的索引引用必须判解码错误（RFC 7541 §4.3/§2.3.3）；RFC 7541 §2.3.3 的地址空间语义 + §4.2/§6.3 的容量协商时序是判定锚点
rfc: RFC 7541 §2.3.3（索引地址空间）/ §4.2（最大表尺寸）/ §4.3（驱逐）/ §6.3（尺寸更新时序）
license: Apache-2.0
---

# RFC 7541 §2.3.3 Index Address-Space Boundary Audit

## 1. Normative Clauses (Original Sources)

RFC 7541 §2.3.3 (key points):
> Index address space = static table (61 entries) + dynamic table (current entries); **an index strictly greater than their sum must be treated as a decoding error**.

RFC 7541 §4.2 + §6.3 (key points):
> Before receiving and acknowledging the peer's SETTINGS, the encoder may assume the dynamic-table size is the protocol default of 4096; when the table size changes, eviction follows the new size, and referencing an evicted index is a decoding error.

Core pattern in one sentence: **the index is HPACK's only "pointer" — an out-of-bounds pointer in a C implementation is a direct OOB-read crash (HAProxy empirical), and "which indices are allowed when" is a timing problem: right after the server says "my table size is 0", in-flight requests encoded against the 4096 default table are perfectly legal, and a decoder that rejects them at this moment kills its own interoperability with every browser (Zephyr empirical). The audit target has two dimensions: boundary (out-of-bounds must error, not crash) and timing (indices within the default-table window must parse).**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| IA-1 | Send an indexed representation with index = 61 + current dynamic-table entry count + N (N=1/8/1024) | Crash / OOB read → same class as CVE-2018-14645; not treated as a decoding error → boundary check missing |
| IA-2 | Within the window after advertising SETTINGS_HEADER_TABLE_SIZE=0 but before the peer's ACK, send indices (≥62) referencing 4096-default-table entries | Decoder rejects (when the spec requires them to parse at this moment) → interoperability bomb (Zephyr #124221 pattern) |
| IA-3 | After a dynamic-table size update causes eviction, immediately reference the evicted old index | Not treated as a decoding error (COMPRESSION_ERROR) → §4.3 eviction consistency missing |
| IA-4 | Cross-reference boundary indices of the static table (61/62) with the dynamic table empty vs non-empty | An off-by-one in the static/dynamic concatenation → address-space concatenation implementation defect |
| IA-5 | Insert a dynamic-table size update mid-header-block (not at the block start) | Not treated as a decoding error → §6.3 size-update position constraint missing (the encoding-position dimension complementary to `rfc7541-hpack-table-capacity`) |
| IA-6 | An indexed representation with index 0 (0x80, illegal) | Not treated as a decoding error → lowest boundary check missing |

Method: hand-encode indexed representations with python-hpack + SETTINGS timing script (advertise 0, then send index ≥62 before ACK); observe crash / error codes / interoperability behavior.

## 3. Attack-Surface Hypotheses

- **Remote-crash DoS**: IA-1 — OOB read/write is a direct crash surface on embedded proxies (C-implemented HPACK)
- **Interoperability bomb**: IA-2 — not attacking the server but making the server attack itself: all browser first-screen bursts rejected, DoS-equivalent effect while being "compliant"
- **Compression-state divergence**: IA-3 — accepting index references after eviction → the two ends' table states fork → subsequent header blocks decode into garbage (information-integrity risk, can evolve into smuggling)

## 4. Related Historical CVEs

| CVE / Empirical Finding | Implementation | Root Cause |
|---|---|---|
| **CVE-2018-14645** | HAProxy <1.8.14 | HPACK decoder `hpack_valid_idx()` out-of-bounds read (CWE-125) → remote-crash DoS; CVSS 7.5; fixed in RHSA-2018:2882 |
| **Zephyr #124221** (2026-11 empirical) | Zephyr RTOS HTTP/2 server | Decoder has no dynamic table; advertises TABLE_SIZE=0 but rejects legal index ≥62 references within the ACK window → Chrome/Firefox first-screen bursts all fail; the RFC 7541 §4.2/§6.3 "default-4096 window" obligation ignored (interoperability layer rather than security layer, but must be audited) |
| Blind-spot declaration | Same family, TBD | Index boundary and SETTINGS timing are two independent dimensions; IoT/edge stacks (Zephyr class) often have incomplete dynamic-table support — a **high-recurrence zone on emerging stacks** |

## 5. Differential Verification

Control group: nghttp2 (strict COMPRESSION_ERROR on out-of-bounds indices; compliant default-window behavior); patched HAProxy ≥1.8.14.
Comparison fields: IA-1 disposition (error code vs crash), IA-2 window behavior, IA-3 post-eviction reference disposition.
False-positive exclusion: an implementation without a dynamic table that maintains a temporary parse table during the window (the Zephyr fix proposal) → passes; an out-of-bounds index errors but with a code other than COMPRESSION_ERROR → record as a compatibility blemish, not a security violation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (index-field boundary mutation), `dharma-grammar-fuzz` (SETTINGS timing × index combination generation)
- Tool layer (what to attack with): python-hpack hand index encoding, SETTINGS/ACK timing control scripts
- Post-hit actions: IA-1 confirmed → archive the minimal crashing index value → assess spread across the same embedded-stack family; IA-2 confirmed → produce a "legal request rejected" interoperability evidence chain (this finding goes through the interoperability-defect channel, not scored as security)
