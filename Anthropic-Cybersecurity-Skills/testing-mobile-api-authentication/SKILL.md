---
name: testing-mobile-api-authentication
description: 'Tests authentication and authorization mechanisms in mobile application
when-to-use: 'Tests authentication and authorization mechanisms in mobile application
  APIs to identify broken authentication, insecure token management, session fixation,
  privilege escalation, and IDOR vulnerabilities. Use when performing API security
  assessments against mobile app backends, testing JWT implementations, evaluating
  OAuth flows, or assessing session management. Activates for requests involving mobile
  API auth testing, token security assessment, OAuth mobile flow testing, or API authorization
  bypass.

  '
domain: cybersecurity
subdomain: mobile-security
author: mahipal
tags:
- mobile-security
- android
- ios
- api-security
- authentication
- penetration-testing
version: 1.0.0
license: Apache-2.0
nist_csf:
- PR.PS-01
- PR.AA-05
- ID.RA-01
- DE.CM-09
mitre_attack:
- T1059
- T1056
- T1036
- T1078
- T1068
---
# Testing Mobile API Authentication

## When to Use

Use this skill when:
- Assessing mobile app backend API authentication during penetration tests
- Testing JWT token implementation for common vulnerabilities (none algorithm, weak signing)
- Evaluating OAuth 2.0 / OIDC flows in mobile applications for redirect, PKCE, and scope issues
- Testing for broken object-level authorization (BOLA/IDOR) in API endpoints

**Do not use** this skill against production APIs without explicit authorization and rate-limiting awareness.

## Prerequisites

- Burp Suite or mitmproxy configured as mobile device proxy
- SSL pinning bypassed on target application (if implemented)
- Valid test account credentials for the target application
- Postman or curl for API request crafting
- jwt.io or PyJWT for JWT analysis and manipulation

## Workflow

### Step 1: Map Authentication Endpoints

Intercept mobile app traffic to identify authentication-related endpoints:

```
POST /api/v1/auth/login          - Initial authentication
POST /api/v1/auth/register       - Account registration
POST /api/v1/auth/refresh        - Token refresh
POST /api/v1/auth/logout         - Session termination
POST /api/v1/auth/forgot-password - Password reset
POST /api/v1/auth/verify-otp     - OTP verification
GET  /api/v1/auth/me             - Authenticated user profile
```

### Step 2: Analyze Token Format and Security

**JWT Analysis:**
```bash
# Decode JWT without verification
echo "eyJhbGciOiJIUzI1NiIs..." | cut -d. -f2 | base64 -d 2>/dev/null

# Check for common JWT vulnerabilities:
# 1. None algorithm attack
# Change header to: {"alg":"none","typ":"JWT"}
# Remove signature: header.payload.

# 2. Algorithm confusion (RS256 to HS256)
# If server uses RS256, try HS256 with public key as secret

# 3. Weak signing key
# Use hashcat or jwt-cracker to brute-force HMAC secret
hashcat -m 16500 jwt.txt wordlist.txt

# 4. Expiration bypass
# Modify "exp" claim to future timestamp
```

**Opaque Token Analysis:**
```
- Test token length and entropy
- Check if tokens are sequential/predictable
- Test token reuse after logout
- Verify token invalidation on password change
```

### Step 3: Test Authentication Bypass

```bash
# Test missing authentication
curl -X GET https://api.target.com/api/v1/users/profile

# Test with empty/null token
curl -X GET https://api.target.com/api/v1/users/profile \
  -H "Authorization: Bearer "

curl -X GET https://api.target.com/api/v1/users/profile \
  -H "Authorization: Bearer null"

# Test with expired token (should fail)
curl -X GET https://api.target.com/api/v1/users/profile \
  -H "Authorization: Bearer <expired_token>"

# Test token from different user
curl -X GET https://api.target.com/api/v1/users/123/profile \
  -H "Authorization: Bearer <user_456_token>"
```

### Step 4: Test IDOR / Broken Object-Level Authorization

```bash
# Change user ID in request path
curl -X GET https://api.target.com/api/v1/users/123/orders \
  -H "Authorization: Bearer <user_456_token>"

# Change object ID in request body
curl -X PUT https://api.target.com/api/v1/orders/789 \
  -H "Authorization: Bearer <user_456_token>" \
  -d '{"status": "cancelled"}'

# Test horizontal privilege escalation
# Access admin endpoints with regular user token
curl -X GET https://api.target.com/api/v1/admin/users \
  -H "Authorization: Bearer <regular_user_token>"
```

### Step 5: Test Session Management

```bash
# Test concurrent sessions
# Login from multiple devices simultaneously - should both remain valid?

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
