---
name: rfc9204-qpack-dynamic-table-capacity
description: Audit whether QPACK dynamic-table capacity negotiation and size-update ordering strictly follow RFC 9204 §3.2 — over-capacity insertion and out-of-order size updates are encoder/decoder stream errors, a compression-layer state-machine attack surface of the same family as CVE-2025-64702
zh-signals: 审计 QPACK 动态表容量协商与尺寸更新顺序是否严格按 RFC 9204 §3.2——超容量插入、乱序尺寸更新即编码器/解码器流错误，与 CVE-2025-64702 家族同源的压缩层状态机攻击面
rfc: RFC 9204 §3.2（动态表容量）/ §4（编码器指令）/ §5（解码器指令）
license: Apache-2.0
---

# RFC 9204 §3.2 QPACK Dynamic-Table Capacity & Update-Order Audit

## 1. Normative Clauses (Original Sources)

RFC 9204 §3.2 (original text, key points):
> Dynamic-table capacity is negotiated via SETTINGS_QPACK_MAX_TABLE_CAPACITY; the encoder MUST NOT let the dynamic table exceed the negotiated capacity; the encoder MUST NOT insert entries that would exceed the current capacity.
> A dynamic-table size update (Set Dynamic Table Capacity instruction) MUST appear on the encoder stream and before any encoding that references the dynamic table; a decoder detecting an out-of-order or over-capacity size update must treat it as an encoder-stream error (QPACK_ENCODER_STREAM_ERROR).

RFC 9204 §4/§5: encoder instructions and decoder instructions each have their own unidirectional stream; instruction-parsing errors on either side must be treated as the corresponding stream error and MUST NOT escalate into uncontrolled whole-connection state.

Core pattern in one sentence: **the QPACK dynamic table is a distributed state machine of "negotiated capacity + incremental updates + dual-end mirroring" — loosen any of the three invariants (negotiated capacity value, size-update ordering, entry-insertion timing) and the dual-end mirror develops ghost entries or ghost references.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| QC-1 | After negotiating SETTINGS_QPACK_MAX_TABLE_CAPACITY to 0 (or a small value), insert dynamic-table entries beyond capacity on the encoder stream | Peer not terminated with QPACK_ENCODER_STREAM_ERROR → violation |
| QC-2 | Send an encoding instruction referencing the dynamic table before the Set Dynamic Table Capacity update (out of order) | Peer not treated as an encoder-stream error → violation |
| QC-3 | Send Set Dynamic Table Capacity declaring a capacity larger than the SETTINGS-negotiated value | Peer accepts and applies → negotiation-hijack surface; not terminated → violation |
| QC-4 | Interleave entry insertion/eviction timing with absolute-index references; check whether both ends map the same absolute index to the same entry | Mapping split → ghost references, type-confusion-grade risk |
| QC-5 | Truncate the encoder stream mid-instruction (FIN lands in the middle of an instruction) and observe decoder-side state | Residual half-parsed state with connection alive → violation |

Method: aioquic with hand-written encoder/decoder dual ends; h3i QPACK scenarios; instruction-by-instruction injection against the decoder's internal table state.

## 3. Attack-Surface Hypotheses

- **Decoder memory runaway**: QC-1 — over-capacity insertion forces the decoder to allocate memory for un-negotiated table space (DoS primitive, same family as CVE-2025-64702)
- **Header-field type confusion**: QC-4 — ghost references make decoded header names/values come from attacker-controlled misplaced entries, equivalent to forging :path / :authority
- **Decoder state-machine crash**: QC-5 — half-parsed instruction + subsequent normal instructions compound into implementation-specific assertion paths

## 4. Related Historical CVEs

| CVE | Implementation | Root cause |
|---|---|---|
| **CVE-2025-64702** (HIGH) | quic-go | QPACK decoding path failed to enforce a specific state constraint and could be triggered remotely; same origin as this Skill — "an unenforced constraint in the compression-layer state machine is a vulnerability". QC-1~QC-5 of this Skill are the systematic audit expansion of that CVE family |
| **CVE-2024-22189** (corroborating pattern) | Multiple QUIC-ecosystem vendors | The symmetric pattern of "a protocol obligation (here response/accounting) not enforced"; see `rfc9000-flow-control-accounting` |

## 5. Differential Verification

Control group: quic-go ≥ fixed version, nghttp3, Cloudflare quiche (three independent QPACK implementations).
Comparison fields: error codes for QC-1~QC-5 individually (QPACK_ENCODER_STREAM_ERROR vs silent), termination level (stream error vs connection error).
False-positive exclusion: an implementation that "accepts but truncates capacity to the negotiated value" with provably rejection-equivalent behavior is compliant; flag only "over-capacity takes effect", "out-of-order accepted", "index mapping split".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `fuzzowski-network-fuzz` (QPACK instruction-stream fuzz), `grammarinator-gen-fuzz` (QPACK instruction grammar generation), `dharma-grammar-fuzz` (dual-end state-machine differential grammar)
- Tool layer (with what): aioquic (byte-level encoder/decoder instruction control), h3i
- Post-hit actions: confirm ghost references → verify whether forged headers can be injected → assess smuggling/auth-bypass chains; confirm over-capacity effect → assess memory amplification ratio
