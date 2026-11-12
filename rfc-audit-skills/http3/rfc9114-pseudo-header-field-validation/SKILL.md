---
name: rfc9114-pseudo-header-field-validation
description: Audit whether HTTP/3 targets handle malformed pseudo-headers/fields strictly per RFC 9114 §4.1.2/§4.2/§4.3 malformed judgments — lenient handling implies a parsing-split and H3→H1 smuggling attack surface (related nginx#1043 unfixed; H2 historical pattern replicated)
zh-signals: 审计 HTTP/3 目标对畸形伪头/字段的处理是否严格按 RFC 9114 §4.1.2/§4.2/§4.3 判 malformed——宽容处理即存在解析分裂与 H3→H1 走私攻击面（关联 nginx#1043 未修复；H2 历史模式复刻）
rfc: RFC 9114 §4.1.2 / §4.2 / §4.3 / §10.3
license: Apache-2.0
---

# RFC 9114 Pseudo-Header & Field Validation Strictness Audit (malformed-judgment completeness)

## 1. Normative Clauses (Original Sources)

RFC 9114 §4.1.2, non-exhaustive malformed case list:

> the presence of prohibited fields or pseudo-header fields / the absence of mandatory pseudo-header fields / invalid values for pseudo-header fields / pseudo-header fields after fields / an invalid sequence of HTTP messages / the inclusion of uppercase field names / the inclusion of invalid characters in field names or values

> Any malformed request or response detected MUST be treated as a stream error of type H3_MESSAGE_ERROR. Intermediaries MUST NOT forward.

§4.3: pseudo-header fields must appear before regular fields (otherwise malformed); request pseudo-headers must not appear in responses and vice versa; **pseudo-headers must not appear in trailer sections**; undefined/invalid pseudo-headers must be judged malformed.

§4.2: field names must be lowercase; uppercase implies malformed; **HTTP/3 messages must not contain connection-specific fields** (e.g. Connection, Transfer-Encoding semantics) — presence is malformed.

§10.3: H3 field encoding can express field names invalid in H1 syntax; messages with invalid field names must be judged malformed, so intermediaries **cannot** convert them to H1 messages — attempting conversion introduces parsing ambiguity.

The RFC emphasizes these requirements are "deliberately strict because being permissive can expose implementations to these vulnerabilities".

## 2. Violation Criteria

| ID | Probe | Verdict |
|---|---|---|
| PH-1 | Missing :method / :scheme / :path; or pseudo-headers placed after regular fields | Stream not closed with H3_MESSAGE_ERROR → violation |
| PH-2 | Field names containing uppercase (e.g. `X-Custom: v` → `X-CuStOm`), illegal characters | Same as above |
| PH-3 | Request carrying connection-specific fields (connection, keep-alive, TE other than trailers, upgrade, etc.) | Same as above |
| PH-4 | Pseudo-header fields in the trailer section | Same as above |
| PH-5 | Through an H3 proxy converting to H1: is the request received by the H1 backend "faithful" (was uppercase normalized? were illegal fields stripped?) | Conversion introduces semantic change → parsing-split surface |
| PH-6 | Unknown pseudo-headers (e.g. :foo) | Must be judged malformed |

Method: h3i field-by-field construction; compare `RESET_STREAM` error codes.

## 3. Attack-Surface Hypotheses

Every leniency is a **parsing divergence point** between the H3 frontend and the H1 backend; combined, they form the primitive library for H3→H1 request smuggling / cache poisoning. PH-3 (connection-specific fields) activates hop-by-hop semantics on the H1 side (e.g. TE: chunked), making it the most dangerous leniency surface for converting proxies. NGINX's publicly unfixed behavior (below) shows implementations are generally incomplete.

## 4. Related Historical CVEs / Public Cases

| Case | Implementation | Note |
|---|---|---|
| nginx/nginx#1043 (issue, unfixed) | NGINX | Violates §4.1.2: requests with malformed pseudo-headers are not closed with H3_MESSAGE_ERROR — shows malformed judgment in header implementations is generally incomplete |
| Same-root-cause family as CVE-2026-33555 | HAProxy | FIN path bypasses body-length check — a variant of "incomplete malformed-judgment coverage" (see rfc9114-content-length-data-mismatch) |
| Historical pattern (H2 side) | Multiple vendors | "Loose pseudo-header/field validation → smuggling" in the RFC 7540 era (e.g. the CVE-2019-* series of H2 implementation discrepancies); H3 implementations are replicating the same mistakes |

## 5. Differential Verification

Control group: quic-go (complete malformed judgment), h3i's expected behaviors.
Comparison fields: per-item checkoff matrix for PH-1~PH-6; for proxy targets additionally record the byte-level request actually received by the H1 backend.
False-positive exclusion: a server sending an HTTP error response before closing the stream is allowed by §4.1.2 (MAY), not a violation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `smuggler-desync`, `http2smugl-desync` (smuggling-primitive composition and exploitation; both in tool-skills/)
- Tool layer (with what): h3i (main tool for field-by-field construction), aioquic
- Post-hit actions: mark each violation as a smuggling primitive; combine PH-x divergences into end-to-end smuggling verification
