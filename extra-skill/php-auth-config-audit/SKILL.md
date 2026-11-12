---
name: php-auth-config-audit
description: |
  PHP source code audit for authentication, configuration, and logic flaws. Trigger it during
  PHP white-box audits when checking authentication bypass, access control, security configuration,
  cryptographic misuse, or business logic vulnerabilities.
  Covers 5 risk categories: authentication bypass (hardcoded credentials/weak comparison/JWT flaws),
  broken access control (IDOR/horizontal privilege escalation),
  security configuration (CORS/error exposure/debug mode), cryptographic misuse (weak hash/ECB/hardcoded keys),
  and business logic (race condition/payment tampering).
zh-signals: "PHP 源码认证、授权、配置、密码学与业务逻辑类漏洞审计。信号:认证绕过,越权,安全配置,密码学误用,业务逻辑"
when-to-use: "Use during PHP white-box audits when checking authentication bypass, IDOR and authorization, insecure configuration, cryptographic misuse, or business logic flaws."
metadata:
  tags: authentication, authorization, idor, config, cors, debug mode, cryptography, weak hash, business logic, authentication bypass, authorization, privilege bypass, config audit, cryptography, business logic
  category: code-audit
---

# PHP Authentication, Configuration, and Logic Flaw Source Code Audit
This skill focuses on authentication, authorization, configuration, cryptographic, and business logic defects at the source code level. Runtime exploitation (such as JWT forgery or race condition scripts) belongs to the corresponding black-box exploit skill.

## Further Reading

- Dangerous patterns for the 5 risk categories / safe pattern code comparison / detection methods → [references/auth-config-patterns.md](references/auth-config-patterns.md)

---

## Quick Reference Table for the 5 Risk Categories

| Type | Typical Pattern | Danger Signal | Severity |
|------|----------|----------|--------|
| Authentication bypass | Hardcoded credentials, `==` weak comparison, JWT algorithm none | Login/token validation logic | Critical-High |
| Broken access control | Direct IDOR reference, missing ownership check, middleware skip | Resource access without authorization checks | High-Critical |
| Security configuration | `display_errors=On`, CORS `*`, leftover debug mode | Information disclosure/cross-origin abuse | Medium-High |
| Cryptographic misuse | `md5($pass)`, ECB mode, hardcoded keys | Password storage/encryption logic | High-Critical |
| Business logic | Race condition, controllable payment amount, state machine step skipping | Transactions/inventory/state transitions | High-Critical |

## Authentication Audit Points

- **Hardcoded passwords/API keys**: search for places where `password`/`secret`/`api_key`/`token` is assigned a literal string
- **Weak comparison**: using `==` to compare passwords/tokens causes type confusion (`"0e123" == "0e456"` is true), so `===` or `hash_equals` is mandatory
- **JWT flaws**: algorithm confusion (RS256→HS256), unverified signature, acceptance of `alg:none`, key leakage, `kid` parameter injection
- **Remember Me**: whether the token is predictable (`md5(username.time())`) and whether it is bound to a user/device
- **Password reset**: token predictability, whether the token is bound to the target user, and whether an expiry mechanism exists

## Authorization Audit Points

- **IDOR**: `$_GET['id']` used directly in a query without a `WHERE user_id=` ownership check, allowing horizontal tampering with object references
- **Route-level vs function-level permissions**: whether the middleware mounting scope fully covers the routes and whether unprotected routes exist
- **Middleware skipping**: missing route groups, abuse of `withoutMiddleware`, OPTIONS preflight bypass
- **Horizontal vs vertical privilege escalation**: horizontal — same role accessing another user's resources; vertical — low-privileged user reaching high-privileged functionality

## Configuration Audit Points

- **Error exposure**: `display_errors=On` combined with `error_reporting=E_ALL` leaks paths/SQL/stack information
- **CORS**: `Access-Control-Allow-Origin: *` combined with `Allow-Credentials: true` allows any origin to carry credentials
- **Debug mode**: leftover Laravel `APP_DEBUG=true`, ThinkPHP `app_debug`, or custom `DEBUG` constants
- **Missing security headers**: `X-Frame-Options`, `Content-Security-Policy`, `X-Content-Type-Options` not set

## Cryptography Audit Points

- **Weak hash**: `md5($pass)` / `sha1($pass)` used for password storage; `password_hash(PASSWORD_BCRYPT)` should be used instead
- **ECB mode**: deterministic encryption where identical plaintext yields identical ciphertext, allowing content to be inferred
- **Hardcoded keys**: `KEY`/`IV`/`SECRET` hardcoded in source; trace the key sources of `openssl_encrypt`/`mcrypt_*` calls
- **Weak randomness**: `mt_rand`/`rand`/`uniqid` used to generate security tokens; `random_bytes`/`random_int` should be used instead

## Logic Audit Points

- **Race condition**: balance/inventory is checked and then decremented without a transaction/lock (SELECT→UPDATE without `FOR UPDATE`)
- **Payment amount tampering**: the amount comes from the client instead of being computed server-side, and signature verification is missing
- **State machine step skipping**: an order status jumps directly from "pending payment" to "shipped" without validation of legal state transitions
- **Unlimited bulk operations**: no rate limiting and no quantity cap, so it can be abused for bulk operations

## Detection Checklist

- [ ] The search for hardcoded credentials is complete (password/secret/key/token/api_key)
- [ ] Every location comparing a password/token with `==` is marked
- [ ] JWT signature validation logic has been reviewed (algorithm, key source, kid)
- [ ] IDOR risk points have been checked for ownership validation
- [ ] Completeness of route permission coverage has been verified
- [ ] php.ini / framework configuration has been checked against the security baseline
- [ ] The password storage method is confirmed (password_hash vs md5/sha1)
- [ ] The encryption key management method has been reviewed (hardcoded vs environment variable/key management)
- [ ] Race-condition-sensitive operations have been checked for transaction/lock mechanisms
- [ ] The amount source and signature validation of the payment/transaction flow are confirmed
