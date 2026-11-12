---
name: rfc7541-hpack-table-capacity
description: Audit HPACK dynamic-table capacity negotiation and size-update timing per RFC 7541 §4.2/§6.3 — encoder-chosen values above the SETTINGS limit must be decoding errors, size updates must appear at the start of the first header block after a change, and multiple changes must signal the smallest value (at most two updates); divergent interpretations become COMPRESSION_ERROR interoperability bombs and table-eviction holes (related nghttp2/nghttp2#1660 interpretation-divergence empirical finding; Google Cloud ALB temporarily degraded dynamic tables to mitigate a client bug; apache.hc.core5 5.3.1 fix)
zh-signals: 审计 HPACK 动态表容量协商与尺寸更新时序是否按 RFC 7541 §4.2/§6.3——编码器选择值超 SETTINGS 上限必须判解码错误、尺寸更新必须出现在变更后第一个头块开头、多次变更必须信号化最小值（至多两次更新）；解释分歧即 COMPRESSION_ERROR 互操作炸弹与表驱逐漏洞（关联 nghttp2/nghttp2#1660 解释分歧实证；Google Cloud ALB 临时降级动态表缓解客户端 bug；apache.hc.core5 5.3.1 修复）
rfc: RFC 7541 §4.2（Maximum Table Size）/ §4.3 / §6.3（Dynamic Table Size Update）/ §7.3（内存消耗）+ RFC 9113 §6.5.2（SETTINGS_HEADER_TABLE_SIZE）
license: Apache-2.0
---

# RFC 7541 §4.2/§6.3 HPACK Dynamic-Table Capacity and Size-Update Timing Audit

## 1. Normative Clauses (Original Sources)

RFC 7541 §4.2 (verbatim):
> An encoder can choose to use less capacity than this maximum size (see Section 6.3), but the chosen size MUST stay lower than or equal to the maximum set by the protocol.

> This dynamic table size update MUST occur at the beginning of the first header block following the change to the dynamic table size. In HTTP/2, this follows a settings acknowledgment.

> In the case that this size is changed more than once in that interval, the smallest maximum table size that occurs in that interval MUST be signaled in a dynamic table size update. The final maximum size is always signaled, resulting in at most two dynamic table size updates.

RFC 7541 §6.3 (verbatim):
> The new maximum size MUST be lower than or equal to the limit determined by the protocol using HPACK. A value that exceeds this limit MUST be treated as a decoding error.

Core pattern in one sentence: **the dynamic table is a piece of stateful memory shared between encoder and decoder — any interpretation divergence in size negotiation explodes into COMPRESSION_ERROR, and the "update must appear at the start of the header block" timing constraint is the only gate preventing the decoder from decoding new-table content with the old table.**

## 2. Violation Criteria

| ID | Probe | Criterion |
|---|---|---|
| HP-1 | Send a dynamic-table size update with a value greater than the peer's SETTINGS_HEADER_TABLE_SIZE | Not disconnected as a decoding error → §6.3 violation (table limit breached, memory surface out of control) |
| HP-2 | After SETTINGS changes the table size from 4096 to 0, omit the size update at the **start** of the first header block (or place the update mid-block) | No COMPRESSION_ERROR → §4.2 timing violation (core scenario of nghttp2#1660 interpretation divergence) |
| HP-3 | Change the table size multiple times within the interval (4096→0→4096); check whether the smallest value (0) is signaled with at most two updates | Signaling the final value directly causes wrong decoder eviction timing → §4.2 violation (eviction desync = ghost entries / stale references) |
| HP-4 | After a size update, reference an index in an evicted slot | Decoder crash / wrong entry → eviction-consistency defect (§4.3/§4.4 implementation warning zone) |
| HP-5 | Oscillate the size 0↔4096 frequently (once per header block) | Significant server CPU increase and eviction table flushed each time → resource-consumption surface (attack path explicitly noted in RFC 7541 §7.3) |

Method: reproduce #1660 with nghttp -v --header-table-size=0; decode the same byte stream with two implementations and compare results.

## 3. Attack-Surface Hypotheses

- **Interoperability bomb**: HP-2/HP-3 — send lenient byte streams to strict peers (or vice versa) to kill connections with COMPRESSION_ERROR; in LB/proxy settings this can selectively fuse specific backends
- **Memory surface out of control**: HP-1 — breaching the table limit directly breaks the memory promise made to the decoder
- **CPU/eviction oscillation**: HP-5 — a variant of the memory-consumption attack path explicitly noted in RFC 7541 §7.3

## 4. Related Historical CVEs

| CVE / Empirical Finding | Implementation | Root Cause |
|---|---|---|
| **nghttp2/nghttp2#1660** (2021-12, reproduced via HAProxy) | nghttp2 ↔ HAProxy interoperability | Interpretation divergence over whether an initial size update is required when SETTINGS_HEADER_TABLE_SIZE=0 → COMPRESSION_ERROR disconnects; empirical proof of the RFC text's multi-interpretability |
| **Google Cloud ALB mitigation event** (disclosed around 2024-10) | Google front end + apache.hc.core5.http2 <5.3.1 | A client dynamic-table bug forced Google to temporarily reduce the dynamic-table size across all classic/global external ALBs — a demonstration of the blast radius of one HPACK size-negotiation bug |
| **apache.hc.core5 5.3.1 fix** (merged 2024-10-12) | Apache HttpComponents Core | Dynamic-table size-change signaling timing fix, same family as #1660 |

## 5. Differential Verification

Control group: latest nghttp2, strict implementations (initial update per RFC 7541 letter).
Comparison fields: HP-1 error determination, HP-2 zero-table scenario behavior, HP-3 three-change sequence handling, HP-5 oscillation cost curve.
False-positive exclusion: both ends being lenient so interoperability "succeeds" is not compliance evidence — every clause must be judged against the RFC text; the SETTINGS_HEADER_TABLE_SIZE=0 scenario is already flagged as disputed (#1660 unsettled), so this probe is marked an "interpretation-divergence signal" rather than a hard violation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (HPACK instruction-sequence fuzzing), `dharma-grammar-fuzz` (size-update / header-block combination grammar generation)
- Tool layer (what to attack with): nghttp (--header-table-size variants), Python h2/hpack library (byte-level HPACK construction)
- Post-hit actions: HP-2/HP-3 hit → targeted interoperability-bomb verification (strict peer + lenient self combination) → HP-5 measure eviction-oscillation CPU cost → evidence merged into the compression-layer weakness family
