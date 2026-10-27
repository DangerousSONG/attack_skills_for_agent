---
name: performing-jwt-none-algorithm-attack
description: "Execute and test the JWT none algorithm attack, crafting tokens with 信号:api攻击,接口测试,graphql。"
when-to-use: Execute and test the JWT none algorithm attack, crafting tokens with
  the alg header set to none using PyJWT and an intercepting proxy (Burp Suite/mitmproxy)
  to bypass signature verification and forge arbitrary claims. Use during authorized
  penetration tests or security assessments of applications that use JWT for authentication
  or authorization, to validate that the server rejects unsigned tokens.
domain: cybersecurity
subdomain: api-security
tags:
- jwt
- none-algorithm
- authentication-bypass
- token-manipulation
- signature-bypass
- penetration-testing
- owasp
- web-security
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
- T1552.001
- T1027
- T1070
---

# Performing JWT None Algorithm Attack

## Overview

The JWT none algorithm attack exploits a vulnerability in JSON Web Token libraries that accept tokens with the `alg` header set to `none`, effectively bypassing signature verification. When a server processes a JWT with `"alg": "none"`, it treats the token as valid without checking any cryptographic signature, allowing attackers to forge tokens with arbitrary claims such as escalated privileges, impersonated users, or extended expiration times. This vulnerability was first disclosed by Tim McLean in 2015 and has affected multiple JWT libraries across languages.


## When to Use

- When conducting security assessments that involve performing jwt none algorithm attack
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Target application using JWT for authentication or authorization
- Ability to intercept and modify HTTP requests (Burp Suite, mitmproxy)
- Python 3.8+ with PyJWT library for token crafting
- Understanding of JWT structure (Header.Payload.Signature)
- Authorization to perform security testing on the target


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## JWT Structure

A JWT consists of three Base64URL-encoded parts separated by dots:

```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.    # Header
eyJzdWIiOiIxMjM0IiwibmFtZSI6IkpvaG4ifQ.    # Payload
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  # Signature
```

## Attack Methodology

### Step 1: Capture a Valid JWT

Intercept a legitimate JWT from the target application using Burp Suite or browser developer tools:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZSI6InVzZXIiLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

### Step 2: Decode and Analyze the Token

```python
import base64
import json

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZSI6InVzZXIiLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

parts = token.split('.')

# Decode header
header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
print(f"Header: {header}")
# Output: {'alg': 'HS256', 'typ': 'JWT'}

# Decode payload
payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
print(f"Payload: {payload}")
# Output: {'sub': '1234567890', 'name': 'John Doe', 'role': 'user', 'iat': 1516239022}
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
