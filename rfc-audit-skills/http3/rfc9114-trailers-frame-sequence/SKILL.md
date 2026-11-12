---
name: rfc9114-trailers-frame-sequence
description: Audit whether HTTP/3 implementations handle trailer and multi-HEADERS frame sequences per RFC 9114 §4.1/§4.2 — DATA after trailing HEADERS is a connection error, trailer vs Content-Length consistency, missing validation of duplicate response header sections is an H3-layer message-smuggling surface (blind-spot clause; nginx#1043 same ecosystem; H2 trailer/CL historical smuggling pattern replicated)
zh-signals: 审计 HTTP/3 实现对 trailer 与多 HEADERS 帧序列的处理是否按 RFC 9114 §4.1/§4.2——trailing HEADERS 后的 DATA 即连接错误、trailer 与 Content-Length 一致性、重复响应头区块缺失校验即 H3 层消息走私面（盲区条款；nginx#1043 同生态；H2 trailer/CL 历史走私模式复刻）
rfc: RFC 9114 §4.1（HTTP 消息分帧）/ §4.2（请求/响应语义）/ RFC 9110 §8.6（Content-Length 与 trailer 一致性）
license: Apache-2.0
---

# RFC 9114 §4.1 Trailer & Frame-Sequence Legality Audit

## 1. Normative Clauses (Original Sources)

RFC 9114 §4.1 (original text, key points):
> Receipt of an invalid sequence of frames MUST be treated as a connection error of type H3_FRAME_UNEXPECTED. In particular, a DATA frame before any HEADERS frame, or a HEADERS or DATA frame after the trailing HEADERS frame, is considered invalid.

That is, the three sections of an H3 message (initial HEADERS → DATA → trailing HEADERS) each appear at most once, in fixed order: any HEADERS/DATA after the trailing HEADERS is a connection error.

RFC 9114 §4.1.2 (field-section constraints): trailing HEADERS must not contain forbidden pseudo-headers and connection-level fields; RFC 9110 §8.6: the presence of a trailer requires Content-Length to match the complete payload (a trailer must not change CL semantics).

Core pattern in one sentence: **H3 expresses "the three sections of a message" as a frame sequence — section boundaries are the legal order of frame types, and any frame beyond the third section is bytes outside the message boundary; bytes outside the message boundary are the definition of smuggling.**

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| TS-1 | Send a DATA frame after the response's trailing HEADERS | Not terminated with H3_FRAME_UNEXPECTED → violation |
| TS-2 | Send a third HEADERS frame on a response (HEADERS after trailer) | Not terminated → violation |
| TS-3 | DATA before any HEADERS (test both request and response directions) | Not terminated → violation |
| TS-4 | trailing HEADERS carrying pseudo-header fields (:status, :path, etc.) / connection-level fields (connection, keep-alive) | Not treated as malformed → violation |
| TS-5 | Response with trailer + Content-Length inconsistent with the DATA sum (CL smaller / larger than actual, one group each) | Not treated as malformed, or forwarded by an intermediary → smuggling surface compounding with `rfc9114-content-length-data-mismatch` |

Method: h3i constructing multi-section frame sequences (main tool); aioquic custom response streams; compare frontend/backend parsing differences (H3 endpoint vs H1 origin).

## 3. Attack-Surface Hypotheses

- **H3→H1 message-boundary smuggling**: TS-1/TS-5 — the H3 end tolerates DATA after trailer while the H1 origin truncates by CL; boundary split is isomorphic to the batch-1 CL audit
- **Parsing-split primitive**: TS-3 — DATA without leading HEADERS interpreted by some implementations as an "implicit empty header section"; the difference from strict implementations is a divergence point
- **Trailer semantic injection**: TS-4 — pseudo-headers entering the trailer section, if reinterpreted by the origin layer, can forge :authority / :method semantics

## 4. Related Historical CVEs / Evidence

| Evidence | Implementation | Root cause |
|---|---|---|
| nginx#1043 (same ecosystem, unfixed) | nginx-quic | Incomplete malformed judgment of H3 field sections — trailer-section field constraints share the same lenient parsing surface as the batch-1 pseudo-header audit |
| H2 historical pattern (RFC 7540 §8.1.2 lesson) | Multiple implementations | Boundary-handling differences around trailers/CONTINUATION produced multiple smuggling cases in the HTTP/2 era (e.g. CL × trailer interactions); H3 inherits the same semantics with a new framing mechanism — historical-pattern replication surface |
| No standalone CVE yet | — | The three-section ordering constraint is straightforward to implement, but trailer-vs-CL consistency and trailer pseudo-header prohibition are scattered clauses with little combined test coverage — blind-spot clause |

## 5. Differential Verification

Control group: quic-go ≥ 0.60, nghttp3, nginx-quic.
Comparison fields: termination behavior for TS-1~TS-5 individually; focus on whether error handling after "trailing HEADERS" vs "after any section" uniformly goes through H3_FRAME_UNEXPECTED.
False-positive exclusion: an implementation rejecting all trailers (no explicit third-section support) is compliant; flag only "data accepted after trailer" and "trailer pseudo-headers parsed".

## 6. Downstream Attack Skills

- Skill layer (how to attack): `smuggler-desync` (boundary-split exploitation), `http2smugl-desync` (H2/H3 downgrade chains), `fuzzowski-network-fuzz` (frame-sequence fuzz)
- Tool layer (with what): h3i (main tool for section-sequence construction), aioquic
- Post-hit actions: TS-1/TS-5 split confirmed → construct end-to-end smuggling probe → assess cache-poisoning/request-hijacking chains
