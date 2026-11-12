---
name: php-ssrf-audit
description: "PHP web source code SSRF audit tool. Identifies user-controllable URLs/addresses reaching network request sinks, traces internal network/protocol/port restrictions and response reflection, and outputs exploitability grading, PoCs, and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的 SSRF 风险，追踪用户可控 URL 进入网络请求 Sink，评估协议与内网限制并输出 PoC。信号:SSRF,PHP审计,内网访问,URL可控,漏洞利用"
when-to-use: "Use when auditing PHP source code for server-side request forgery, where user-controlled URLs reach network request sinks and you need exploitability grading, PoCs, and fixes."
---

# PHP SSRF Audit (php-ssrf-audit)

Analyze PHP project source code to identify SSRF risks: user-controllable URL/host/path reaching network request or file-read functions without protocol allowlists, DNS/IP internal-network rejection, port restrictions, or similar controls.

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-SSRF-{sequence}`

## SSRF Sinks (Mandatory)
Identify at least the following network/address access points:
- `curl_setopt(CURLOPT_URL, $url)` / `curl_exec`
- `file_get_contents($url)` / `readfile($url)` / `fopen($url, {value})`
- `stream_get_contents($stream)` / `fsockopen` / `pfsockopen`
- `get_headers($url)` / `dns_get_record` (when combined with address resolution)
Dangerous patterns:
- URL/Host/Port/Path comes from user input and is controllable
- Protocol is unrestricted (`file://`, `gopher://`, `php://`, etc. are allowed)

## Mandatory Security Checkpoints
- Protocol allowlist: allow only `http/https` (if necessary)
- Block internal network ranges after DNS/IP resolution: reject `127.0.0.1/::1/10.0.0.0/8/172.16.0.0/12/192.168.0.0/16`, etc.
- Port restrictions: reject high-risk internal ports (as defined by project policy)
- Redirect handling: restrict followed redirects (e.g. `CURLOPT_FOLLOWLOCATION`)
- Redirect and final address validation: even if the initial URL passes the allowlist, the same blocking and protocol validation MUST still be applied to the "final URL after redirects"
- DNS rebinding protection: when allowing domain access, a final resolution MUST be performed immediately before the actual request, or a safe resolution policy must be used to avoid "external first, internal later"
- URL normalization: normalize encoded hosts/paths (double encoding, case, userinfo segment `user:pass@host`) before the allowlist check

## When to Trigger the Tracer
- The URL is assembled from multiple fields (schema + host + path + query)
- There are multi-layer function calls or encode/decode/replace operations
- The security decision depends on string normalization (the real final URL MUST be traced)

## Report Output
```
{output_path}/vuln_audit/ssrf_{timestamp}.md
```

## Vulnerability Entry Template (Mandatory)
Same structure as `php-sql-audit`, but the data flow chain MUST cover:
- The source and assembly process of the URL/Host/Port variables actually used to issue the request
- Branch evidence for protocol selection and internal-network blocking decisions

## Evidence Citation (Mandatory: from php-route-tracer)
Every suspected SSRF vulnerability MUST cite the corresponding evidence points of the **SSRF row** in `## 9) Sink Evidence Type Checklist` of the trace output, item by item (writing only "possibly" is forbidden; a pending-verification status is allowed, but the evidence citations MUST exist):
1. `EVID_SSRF_URL_NORMALIZATION`: URL normalization steps (corresponding to the evidence points in the SSRF row)
2. `EVID_SSRF_FINAL_URL_HOST_PORT`: the final URL/Host/Port before the request is issued (corresponding to the evidence points in the SSRF row)
3. `EVID_SSRF_FINAL_REDIRECT_URL`: if redirects/follow-redirects exist: evidence of the address after the final redirect (corresponding to the evidence points in the SSRF row)
4. `EVID_SSRF_DNSIP_AND_INNER_BLOCK`: evidence of DNS/IP resolution and the internal-network blocking decision (corresponding to the evidence points in the SSRF row)

## Handling Missing tracer Evidence (Mandatory)
- If any of the key evidence points 1~4 above cannot be found in the trace: this finding can only be marked as `⚠️Pending Verification`, and must not be given `✅Confirmed Exploitable`.

#### PoC (Mandatory)
- Must provide an executable request (HTTP code block)
- The PoC URL must use a real route with real controllable field names

