---
name: rfc9114-content-length-data-mismatch
description: Audit whether HTTP/3 targets violate RFC 9114 §4.1.2 — the Content-Length value must equal the sum of received DATA frame lengths; a violation that gets forwarded implies an H3→H1 request-smuggling surface (related CVE-2026-33555 HAProxy)
zh-signals: 审计 HTTP/3 目标是否违反 RFC 9114 §4.1.2 —— Content-Length 值必须等于收到的 DATA 帧长度之和；违规且被转发即存在 H3→H1 请求走私攻击面（关联 CVE-2026-33555 HAProxy）
rfc: RFC 9114 §4.1.2
license: Apache-2.0
---

# RFC 9114 §4.1.2 Content-Length vs DATA Frame-Length Consistency Audit

## 1. Normative Clauses (Original Sources)

RFC 9114 §4.1.2 (Malformed Requests and Responses):

> A request or response that is defined as having content when it contains a Content-Length header field (Section 8.6 of [HTTP]) is malformed if the value of the Content-Length header field does not equal the sum of the DATA frame lengths received.

> Intermediaries that process HTTP requests or responses (i.e., any intermediary not acting as a tunnel) MUST NOT forward a malformed request or response. Malformed requests or responses that are detected MUST be treated as a stream error of type H3_MESSAGE_ERROR.

## 2. Violation Criteria

Send the following three probe groups to the target (server / H3 proxy) and record each behavior:

| ID | Probe | Verdict |
|---|---|---|
| CL-1 | Content-Length = N, actual DATA frame lengths ≠ N (more or fewer) | Correct: stream reset with H3_MESSAGE_ERROR; violation: accepted and processed as-is |
| CL-2 | Content-Length = N, QUIC stream ends early with FIN and body is shorter than N | Correct: judged malformed; **key test: does the "bare-FIN fast path" skip the check** (root cause of CVE-2026-33555) |
| CL-3 | Through a proxy to an H1 backend, a request with CL/body mismatch is converted verbatim | Proxy violates MUST NOT forward → smuggling surface confirmed |

Method: h3i (Cloudflare's open-source H3 test tool, supports frame-level construction), aioquic custom client; observe whether `RESET_STREAM` carries error code `H3_MESSAGE_ERROR (0x0100)`.

## 3. Attack-Surface Hypotheses

Any leniency in body-length validation by H3→H1 converting proxies splits "frontend H3 parsing" and "backend H1 parsing" into two independent decision points → **cross-protocol request smuggling**: reaching backend resources blocked by H1 frontend rules, cache poisoning, session fixation. The FIN-path bypass (CL-2) means no complex frame sequence is needed — a single connection suffices.

## 4. Related Historical CVEs

| CVE | Implementation | Root cause |
|---|---|---|
| **CVE-2026-33555** | HAProxy (HTTP/3 → HTTP/1) | A standalone QUIC FIN took a standalone-FIN fast path, skipping the `h3_check_body_size()` RFC 9114 §4.1.2 check; CL-mismatched requests were forwarded to the H1 side, achieving cross-protocol smuggling. Fix commit `05a29544` (2026-03-18) adds the check to the fast path |
| Reference: nginx/nginx#1043 | NGINX | Violates §4.1.2: requests with malformed pseudo-headers are not closed with H3_MESSAGE_ERROR (issue status: open, unfixed) |

## 5. Differential Verification

Control group: quic-go ≥0.59.1, HAProxy ≥ fixed version (check present on the FIN path).
Comparison fields: whether the target returns `H3_MESSAGE_ERROR` under CL-1/CL-2/CL-3, whether it forwards, and whether the H1 backend receives a body consistent with the declared length.
False-positive exclusion: some implementations allow a non-zero CL on "never-has-content" responses (§4.1.2 second paragraph) — that is compliant; do not misjudge the response case as a violation.

## 6. Downstream Attack Skills

- Skill layer (how to attack): `smuggler-desync` (smuggling probing and exploitation), `http2smugl-desync` (H2/H3 desync variants; both in tool-skills/)
- Tool layer (with what): h3i, aioquic (differential frame construction), curl --http3 (control group), Burp-class replay tools (registry: Web application category, 272 tools)
- Post-hit actions: smuggling confirmation probe (access a path only reachable by the backend) → escalate into cache-poisoning/session-hijacking exploit chains
