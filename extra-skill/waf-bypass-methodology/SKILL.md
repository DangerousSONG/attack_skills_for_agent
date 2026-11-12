---
name: waf-bypass-methodology
description: "Unified WAF bypass methodology. Use when an exploit payload is blocked by a WAF returning 403/406. Covers fingerprinting and bypass for F5, ChinaNetCenter, UEWAF, Cloudflare, ModSecurity, SafeDog, and BT Panel products, including encoding bypass, chunked transfer, HTTP method switching, parameter pollution, payload mutation, SQL injection bypass, captcha bypass, and proxy pool / free proxy IP rotation to evade IP bans"
zh-signals: "统一 WAF 绕过方法论，识别 WAF 指纹并通过编码、分块传输、参数污染、验证码与代理池等手段绕过拦截。信号:WAF绕过,403拦截,编码绕过,参数污染,验证码"
when-to-use: "Use when an exploit payload is blocked by a WAF returning 403/406 or an interception page. Applies to F5, ChinaNetCenter, UEWAF, Cloudflare, ModSecurity and similar products across encoding, HTTP-layer, and parameter-layer bypass."
metadata:
  tags: "waf,bypass,bypass,firewall,cloudflare,modsecurity,safedog,btpanel,WAFbypass,encoding,chunkedtransfer,parameterpollution,403,forbidden,blocked,rejected,406,interception,intercepted,requestrejected,payloadblocked,f5,chinanetcenter,uewaf,captcha,verificationcode,unlock,sql,injection,injectionbypass,proxypool,freeproxy,proxy,iprotation"
  category: "exploit"
---

# Unified WAF Bypass Methodology

The core principle of WAF bypass: the WAF and the backend application parse the same HTTP request differently — exploit that difference so the WAF "sees" a legitimate request while the backend "sees" a malicious payload.

## Further Reading

- Encoding bypass payloads (double URL / Unicode / HTML / mixed encoding) → [references/encoding-bypass-payloads.md](references/encoding-bypass-payloads.md)
- HTTP protocol layer bypass (chunked transfer / Content-Type / method switching / HTTP2 / smuggling) → [references/http-protocol-bypass.md](references/http-protocol-bypass.md)
- Parameter layer bypass (HPP / array syntax / Multipart) → [references/parameter-bypass.md](references/parameter-bypass.md)
- Payload mutation (generic encoding / splitting / format switching) → [references/payload-mutation.md](references/payload-mutation.md)

---

## Phase 0: WAF Identification

### 0.1 Detect Whether a WAF Is Present

```bash
# Send an obviously malicious request and observe the response
curl -s "http://TARGET/?id=1' OR '1'='1" -D-
curl -s "http://TARGET/?id=<script>alert(1)</script>" -D-
curl -s "http://TARGET/?cmd=;id" -D-

# Compare the response differences between normal and malicious requests
# WAF interception features: 403/406 status code, a specific interception page, a different Server header
```

### 0.2 WAF Fingerprinting

| Feature | WAF Product |
|------|----------|
| `Server: cloudflare` / `cf-ray` header | Cloudflare |
| `X-Sucuri-ID` header | Sucuri |
| Response contains `ModSecurity` | ModSecurity |
| Response contains `SafeDog` / `safedog` | SafeDog |
| Response contains `BT Panel` / `bt.cn` | BT Panel WAF |
| `X-Powered-By-Anquanbao` | Anquanbao WAF |
| Response contains `yunsuo` | Yunsuo |
| Alibaba Cloud 403 page | Alibaba Cloud Security Center |
| Tencent Cloud specific 403 | Tencent Cloud WAF |

---

## Generic Bypass Checklist

```
Payload blocked → 403 / interception page
├── 1. Encoding bypass
│   ├── Double URL encoding
│   ├── Unicode encoding
│   └── Mixed case + NULL byte
├── 2. HTTP layer
│   ├── Chunked transfer
│   ├── Content-Type switching
│   ├── HTTP method switching
│   └── HTTP/2
├── 3. Parameter layer
│   ├── Parameter pollution (HPP)
│   ├── Array / JSON nesting
│   └── Multipart wrapping
├── 4. Payload mutation
│   ├── Space substitution (comment / Tab / newline)
│   ├── Function name substitution
│   ├── Concatenation / encoding functions
│   └── Wildcards / variables
└── 5. Logic layer
    ├── Send over multiple requests (probe first, then exploit)
    └── Abuse allowlisted paths (/api/health + path traversal)
```

> See the corresponding references file for the detailed payloads of each branch

## Phase 5: Domestic / Commercial WAF Fingerprints and Bypass

| WAF | Fingerprint Feature | Bypass Approach |
|-----|---------|---------|
| F5 BIG-IP ASM | `X-Content-Type-Options`, ASM interception page | Encoding obfuscation, chunked transfer, method switching |
| ChinaNetCenter | `X-Cache: NS`, ChinaNetCenter interception page | Parameter pollution, case variation, Unicode encoding |
| UEWAF | Specific interception page / JS challenge | Request the backend IP/domain directly, bypass the JS check |
| Cloudflare | `cf-ray`, `server: cloudflare` | Direct connection to the origin IP, encoding bypass |
| SafeDog / BT Panel | Page features | Comment characters, equivalent functions, encoding |

## Phase 6: Captcha Unlocking (captcha bypass)

When a WAF/risk control uses a captcha to block high-frequency attacks:

1. **Logic bypass**: reuse the captcha, blank the code field, drop the parameter, universal captcha
2. **Recognition**: OCR / captcha-solving platform for image captchas, coordinate-simulated clicks for click-type captchas
3. **Trigger point switching**: change the endpoint / change the parameter to bypass the captcha trigger logic
4. See captcha-bypass-methodology for detailed methods

## Phase 7: Proxy Pool / Free Proxy IP Rotation

When the WAF rate-limits or bans by IP:

1. Use free proxies / a proxy pool to rotate the egress IP and evade IP bans
2. Mind proxy availability and speed, and prefer high-anonymity proxies
3. Combine with low-rate (slow) requests to lower the chance of triggering risk controls
4. Free proxy sources change dynamically, so verify proxy availability before testing

## Phase 8: SQL Injection Bypass (F5 / ChinaNetCenter scenarios)

- Comment character substitution: `-- ` → `#` → `/*!*/` → `;%00`
- Keyword obfuscation: case variation, inline comments `/*!union*/`, equivalent functions
- Encoding: double URL encoding, Unicode, hex
- Combine chunked transfer with parameter pollution

