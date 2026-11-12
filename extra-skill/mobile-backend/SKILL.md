---
name: mobile-backend
description: "Mobile app backend API security testing. Use when the target is a mobile app's backend interface, when mobile API paths such as /api/v1/ are discovered, or when communication security between the app and its server needs testing. Covers API endpoint discovery, authentication mechanism testing, business logic flaws, and mobile-specific security issues"
zh-signals: "移动 App 后端 API 安全测试，覆盖端点发现、认证机制、业务逻辑漏洞与移动端特有风险。信号:移动后端,API测试,认证绕过,IDOR,业务逻辑"
when-to-use: >-
  Use when the target is a mobile app's backend API, you discover /api/v1/ style mobile
  API paths, or you need to test communication security between an app and its server.
metadata:
  tags: "mobile,api,backend,auth,app,ios,android,mobile-security,business-logic,payment"
  category: "exploit"
---

# Mobile App Backend API Security Testing Methodology

Differences between mobile backend APIs and traditional web: mobile clients usually call REST APIs directly (without a browser), and authentication mechanisms, parameter formats and business logic all have mobile-specific characteristics.

## ⛔ Further Reading (Must Read)

- Payment tampering, CAPTCHA bypass, race conditions, data security, mobile-specific issues → [references/mobile-logic-bugs.md](references/mobile-logic-bugs.md)

## Phase 1: API Endpoint Discovery

```bash
# spray directory brute-forcing (recommended)
spray -u http://target -d $ABOUTSECURITY_ROOT/Dic/Web/Directory/Fuzz_common.txt
# or ffuf
ffuf -u http://target/FUZZ -w $ABOUTSECURITY_ROOT/Dic/Web/Directory/Fuzz_common.txt -mc 200,301,302,403
# /api/v1/, /api/v2/, /mobile/api/, /graphql
```
Check documentation: `/docs`, `/swagger`, `/openapi.json`, `/redoc`

App reverse engineering: capture traffic (Burp/Charles) | decompile the APK and search for URL strings

## Phase 2: Authentication Mechanism Testing

| Auth Method | Fingerprint | Attack Direction |
|----------|------|----------|
| JWT | `Bearer eyJ...` | `jwt-attack-methodology` |
| API Key | `X-API-Key` | leak detection |
| OAuth | `/oauth/token` | `oauth-sso-attack` |
| Custom signature | `sign=md5(...)` | signature algorithm reverse engineering |

Bypass testing: access without a token | expired token | modify user_id/role | low-privilege access to high-privilege APIs

## Phase 3: Business Logic Flaws

### Broken Access Control (IDOR)
```
GET /api/v1/users/1001/profile → yourself
GET /api/v1/users/1002/profile → someone else? → IDOR!
```

### Payment / CAPTCHA / Race Conditions
→ detailed methods and payloads → [references/mobile-logic-bugs.md](references/mobile-logic-bugs.md)

## Notes
- Mobile APIs usually trust the client more than web does — the backend performs fewer validations
- Watch for API version differences (v1 may be vulnerable, v2 may have fixed it while v1 is still online)
