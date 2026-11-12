---
name: testing-oauth2-implementation-flaws
description: "Tests OAuth 2.0 and OpenID Connect authorization code flows. Signals: API attack, interface testing, GraphQL."
zh-signals: "Tests OAuth 2.0 and OpenID Connect implementations for authorization code 信号:api攻击,接口测试,graphql。"
when-to-use: Tests OAuth 2.0 and OpenID Connect implementations for authorization code
  interception, redirect URI manipulation, CSRF in OAuth flows, token leakage, scope
  escalation, and PKCE bypass, using Burp Suite Professional and the EsPReSSO extension
  to probe the authorization server, client, and token handling. Use when assessing OAuth2/OIDC
  flows or SSO systems for misconfigurations enabling account takeover.
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- oauth2
- oidc
- authentication
- redirect-uri
- token-security
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
- T1070
---
# Testing OAuth2 Implementation Flaws

## When to Use

- Assessing OAuth 2.0 authorization code flow for redirect URI validation weaknesses
- Testing OAuth client applications for CSRF protection (state parameter usage) and PKCE enforcement
- Evaluating token storage, transmission, and lifecycle management in OAuth implementations
- Testing scope escalation where clients request more permissions than authorized
- Assessing OpenID Connect implementations for ID token validation and nonce usage

**Do not use** without written authorization. OAuth testing may result in token theft or unauthorized access.

## Prerequisites

- Written authorization specifying the OAuth provider and client applications in scope
- Test OAuth client registered with the authorization server
- Burp Suite Professional for intercepting OAuth redirects and token flows
- Python 3.10+ with `requests` and `oauthlib` libraries
- Browser developer tools for observing OAuth redirect chains
- Knowledge of the OAuth 2.0 grant types in use (authorization code, implicit, client credentials)

## Workflow

### Step 1: OAuth Flow Reconnaissance

```python
import requests
import urllib.parse
import re
import hashlib
import base64
import secrets

AUTH_SERVER = "https://auth.example.com"
CLIENT_ID = "test-client-id"
REDIRECT_URI = "https://app.example.com/callback"
SCOPE = "openid profile email"

# Discover OAuth endpoints
well_known = requests.get(f"{AUTH_SERVER}/.well-known/openid-configuration")
if well_known.status_code == 200:
    config = well_known.json()
    print("OAuth/OIDC Configuration:")
    print(f"  Authorization: {config.get('authorization_endpoint')}")
    print(f"  Token: {config.get('token_endpoint')}")
    print(f"  UserInfo: {config.get('userinfo_endpoint')}")
    print(f"  JWKS: {config.get('jwks_uri')}")
    print(f"  Supported grants: {config.get('grant_types_supported')}")
    print(f"  Supported scopes: {config.get('scopes_supported')}")
    print(f"  PKCE methods: {config.get('code_challenge_methods_supported')}")
    auth_endpoint = config['authorization_endpoint']
    token_endpoint = config['token_endpoint']
else:
    # Try common paths
    for path in ["/authorize", "/oauth/authorize", "/oauth2/authorize", "/auth"]:
        resp = requests.get(f"{AUTH_SERVER}{path}", allow_redirects=False)
        if resp.status_code in (302, 400):
            print(f"Authorization endpoint found: {AUTH_SERVER}{path}")
            auth_endpoint = f"{AUTH_SERVER}{path}"
            break
```

### Step 2: Redirect URI Validation Testing

```python
# Test redirect_uri validation strictness
REDIRECT_BYPASS_PAYLOADS = [
    # Open redirect variations
    REDIRECT_URI,                                          # Legitimate
    "https://evil.com",                                    # Different domain
    "https://app.example.com.evil.com/callback",          # Subdomain of attacker
    "https://app.example.com@evil.com/callback",          # URL authority confusion
    f"{REDIRECT_URI}/../../../evil.com",                  # Path traversal
    f"{REDIRECT_URI}?next=https://evil.com",              # Parameter injection
    f"{REDIRECT_URI}#https://evil.com",                   # Fragment injection
    f"{REDIRECT_URI}%23evil.com",                         # Encoded fragment
    "https://app.example.com/callback/../../evil",        # Relative path
    "https://APP.EXAMPLE.COM/callback",                   # Case variation
    "https://app.example.com/Callback",                   # Path case variation
    "https://app.example.com/callback/",                  # Trailing slash
    "https://app.example.com/callback?",                  # Trailing question mark
    "http://app.example.com/callback",                    # HTTP downgrade
    "https://app.example.com:443/callback",               # Explicit port
    "https://app.example.com:8443/callback",              # Different port
    f"{REDIRECT_URI}/.evil.com",                          # Dot segment
    "https://app.example.com/callbackevil",               # Path prefix match
    "javascript://app.example.com/callback%0aalert(1)",   # JavaScript protocol
]

print("=== Redirect URI Validation Testing ===\n")
for redirect in REDIRECT_BYPASS_PAYLOADS:
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": redirect,
        "scope": SCOPE,
        "state": secrets.token_urlsafe(32),
    }
    resp = requests.get(auth_endpoint, params=params, allow_redirects=False)

    if resp.status_code == 302:
        location = resp.headers.get("Location", "")
        if "code=" in location or redirect in location:
            status = "ACCEPTED"
            if redirect != REDIRECT_URI:
                print(f"  [VULNERABLE] {redirect[:70]} -> Redirect accepted")
        else:
            status = "REDIRECTED"
    elif resp.status_code == 400:
        status = "REJECTED"
    else:
        status = f"HTTP {resp.status_code}"

    if redirect == REDIRECT_URI:
        print(f"  [BASELINE] {redirect[:70]} -> {status}")
```

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
