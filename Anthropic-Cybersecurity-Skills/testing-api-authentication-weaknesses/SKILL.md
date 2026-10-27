---
name: testing-api-authentication-weaknesses
description: "Tests API authentication mechanisms for weaknesses including broken 信号:api攻击,接口测试,graphql。"
when-to-use: 'Tests API authentication mechanisms for weaknesses including broken
  token validation, missing authentication on endpoints, weak password policies, credential
  stuffing susceptibility, token leakage in URLs or logs, and session management flaws.
  The tester evaluates JWT implementation, API key handling, OAuth flows, and session
  token entropy to identify authentication bypasses. Maps to OWASP API2:2023 Broken
  Authentication. Activates for requests involving API authentication testing, token
  validation assessment, credential security testing, or API auth bypass.

  '
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- owasp
- authentication
- jwt
- session-management
- credential-security
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
- T1003
- T1110
---
# Testing API Authentication Weaknesses

## When to Use

- Assessing REST API authentication mechanisms for bypass vulnerabilities before production deployment
- Testing JWT token implementation for common weaknesses (none algorithm, key confusion, missing expiration)
- Evaluating whether all API endpoints enforce authentication or if some are unintentionally exposed
- Testing API key generation, storage, and rotation mechanisms for predictability or leakage
- Validating session management including token expiration, revocation, and refresh token security

**Do not use** without written authorization. Authentication testing involves attempting to bypass security controls.

## Prerequisites

- Written authorization specifying target API and authentication mechanisms in scope
- Valid test credentials for at least two user roles (regular user, admin)
- Burp Suite Professional with JWT-related extensions (JSON Web Tokens, JWT Editor)
- Python 3.10+ with `requests`, `PyJWT`, and `jwt` libraries
- Wordlists for credential testing (SecLists authentication wordlists)
- API documentation or OpenAPI specification

## Workflow

### Step 1: Authentication Mechanism Identification

```python
import requests
import json

BASE_URL = "https://target-api.example.com/api/v1"

# Probe the API to identify authentication mechanisms
auth_indicators = {
    "jwt_bearer": False,
    "api_key_header": False,
    "api_key_query": False,
    "basic_auth": False,
    "oauth2": False,
    "session_cookie": False,
    "custom_token": False,
}

# Test 1: Check unauthenticated access
resp = requests.get(f"{BASE_URL}/users/me")
print(f"Unauthenticated: {resp.status_code}")
if resp.status_code == 200:
    print("[CRITICAL] Endpoint accessible without authentication")

# Test 2: Check WWW-Authenticate header
if "WWW-Authenticate" in resp.headers:
    scheme = resp.headers["WWW-Authenticate"]
    print(f"Auth scheme advertised: {scheme}")
    if "Bearer" in scheme:
        auth_indicators["jwt_bearer"] = True
    elif "Basic" in scheme:
        auth_indicators["basic_auth"] = True

# Test 3: Login and examine tokens
login_resp = requests.post(f"{BASE_URL}/auth/login",
    json={"username": "testuser@example.com", "password": "TestPass123!"})

if login_resp.status_code == 200:
    login_data = login_resp.json()
    # Check for JWT tokens
    for key in ["token", "access_token", "jwt", "id_token"]:
        if key in login_data:
            token = login_data[key]
            if token.count('.') == 2:
                auth_indicators["jwt_bearer"] = True
                print(f"JWT found in response field: {key}")
    # Check for refresh tokens
    for key in ["refresh_token", "refresh"]:
        if key in login_data:
            print(f"Refresh token found in field: {key}")
    # Check for session cookies
    for cookie in login_resp.cookies:
        print(f"Cookie set: {cookie.name} = {cookie.value[:20]}...")
        if "session" in cookie.name.lower():
            auth_indicators["session_cookie"] = True

print(f"\nAuthentication mechanisms detected: {[k for k,v in auth_indicators.items() if v]}")
```

### Step 2: Unauthenticated Endpoint Discovery

```python

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
