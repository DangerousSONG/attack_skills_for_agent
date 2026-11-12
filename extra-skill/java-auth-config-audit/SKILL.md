---
name: java-auth-config-audit
description: |
  Java source code authentication and configuration security audit. Trigger during Java white-box audits when authentication bypass, authorization flaws, or security configuration issues need to be detected.
  Covers 6 risk categories: authentication bypass (Spring Security/Shiro Filter chain URI parsing differences),
  broken access control (IDOR/horizontal privilege escalation/vertical privilege escalation), JWT security (algorithm confusion/key leakage/Claims validation),
  crypto configuration (weak algorithms/hardcoded keys/insecure randomness), information disclosure (error stack traces/Actuator/Debug mode),
  and business logic flaws (race conditions/amount tampering/process bypass).
zh-signals: "审计 Java 源码中的认证绕过、越权、JWT、加密配置、信息泄露与业务逻辑漏洞。信号:认证绕过,越权,JWT,Shiro,Java审计"
when-to-use: >-
  Use during Java white-box audit when validating authentication bypass, authorization
  flaws, JWT weaknesses, crypto config, information disclosure, or business logic bugs.
metadata:
  tags: authentication bypass, authorization, idor, jwt, shiro, spring security, crypto config, information disclosure, actuator, business logic, java source audit
  category: code-audit
---

# Java Authentication and Configuration Security Source Code Audit

Authentication, authorization, and security configuration are the highest-yield vulnerability surfaces in Java backend projects. This skill provides complete detection approaches for 6 major categories of white-box audit, applicable to Spring Boot/Spring Security, Apache Shiro, and custom frameworks.

## Related Skills

- `java-framework-audit` — Spring/Struts/MyBatis framework audits
- `java-injection-audit` — SQL/OGNL/EL injection audits
- `java-serialization-audit` — deserialization vulnerability audits
- `idor-methodology` — black-box IDOR testing methodology

## Further Reading

- Detailed patterns for the 6 vulnerability categories (dangerous code/safe code/EVID evidence) -> [references/auth-config-patterns.md](references/auth-config-patterns.md)

---

## Quick Reference Table of the 6 Risk Categories

| # | Category | Key search entry points | Severity |
|---|------|-------------|---------|
| 1 | Authentication bypass | `SecurityConfig`, `ShiroFilterFactory`, `doFilter` | Critical |
| 2 | Broken access control | DAO/Mapper query statements, `@PreAuthorize`, Controller parameters | High |
| 3 | JWT security | `Jwts.parser()`, `Algorithm.HMAC`, `SECRET_KEY` | High |
| 4 | Crypto configuration | `MessageDigest`, `Cipher.getInstance`, `new Random()` | High |
| 5 | Information disclosure | `application.yml` Actuator configuration, `@ExceptionHandler` | Medium |
| 6 | Business logic | balance/stock operations, state machine transitions, payment callbacks | High |

---

## 1. Authentication Bypass Audit Points

- **Spring Security**: check `FilterChainProxy` matching rules, the differences between `AntPathRequestMatcher` and `MvcRequestMatcher` (trailing slash/path suffix); `requestMatchers` ordering—a permissive `permitAll()` rule placed first overrides later interceptors; whether `permitAll()` is overly broad (e.g. `/api/**`)
- **Shiro**: bypass caused by URI parsing differences—`/admin/` vs `/admin` vs `/admin/..;/`; path normalization bypass series such as CVE-2020-1957 / CVE-2020-11989 / CVE-2020-13933
- **Custom Filter**: an early return in `doFilter()` causes the rest of the chain not to execute; sloppy allowlist regex (e.g. `startsWith("/public")` also matches `/publicevil`)

## 2. Broken Access Control Audit Points

- **Horizontal privilege escalation**: the endpoint only validates login state but not resource ownership—the DAO layer `WHERE id = #{orderId}` lacks the `AND user_id = #{currentUserId}` condition
- **Vertical privilege escalation**: Controller/Service methods lack role annotations `@PreAuthorize`/`@RequiresRoles`; enum values (role IDs) are guessable
- **IDOR**: auto-increment IDs can be enumerated; whether UUIDs are truly unpredictable; bulk endpoints skip per-item permission checks

## 3. JWT Security Audit Points

- **Algorithm confusion**: `alg: none` bypasses signature verification; RS256 -> HS256 attack (using the public key as the HMAC key)
- **Hardcoded keys**: `SECRET_KEY = "xxx"` in source code or plaintext configuration in `application.yml`
- **Missing Claims validation**: `exp` (expiry)/`iss` (issuer)/`aud` (audience) are unvalidated, allowing tokens to be reused across environments
- **Refresh mechanism**: `refresh_token` is long-lived and not bound to a user/device, allowing unlimited refresh after theft

## 4. Crypto Configuration Audit Points

- **Weak algorithms**: `MD5`/`SHA1` for password hashing, `DES`/`RC4` for encryption, `ECB` mode (leaks data patterns)
- **Correct practice**: use `bcrypt`/`scrypt`/`argon2` for passwords; use `AES-GCM`/`AES-CBC+HMAC` for symmetric encryption
- **Hardcoded keys/salts**: `private static final String KEY = "..."` or the salt hardcoded in code
- **Insecure randomness**: `java.util.Random` is predictable; security-sensitive scenarios must use `SecureRandom`

## 5. Information Disclosure Audit Points

- **Exposed Actuator endpoints**: `/env` (environment variables/passwords), `/heapdump` (heap memory containing keys), `/jolokia` (remote code execution)
- **Verbose error stack traces**: no global exception handler, SQL errors/class names/paths returned directly to the client
- **Debug mode**: `server.error.include-stacktrace=always`, `spring.devtools` not removed
- **Sensitive data in logs**: `log.info("user password: {}", password)` or full credit card numbers written to log files

## 6. Business Logic Audit Points

- **Concurrency race**: balance check and deduction are non-atomic (double-spending); coupon/points replay
- **Parameter tampering**: amount/quantity/discount are passed by the client and not recomputed server-side; order amounts can be negative
- **Process bypass**: multi-step flows (register-verify-set password) lack state validation between steps, allowing a direct jump to later endpoints

---

## Detection Checklist

Confirm each item during the audit and record EVID evidence for every finding:

- [ ] Spring Security configuration chain ordering issues or overly broad `permitAll`
- [ ] Shiro `filterChainDefinitionMap` URI parsing difference bypass
- [ ] Custom Filter/Interceptor early return or allowlist bypass
- [ ] Whether data queries bind the current user ID (horizontal privilege escalation)
- [ ] Whether sensitive endpoints have role/permission annotations (vertical privilege escalation)
- [ ] Whether JWT enforces a specified algorithm + secure key storage + full Claims validation
- [ ] Password storage bcrypt/scrypt/argon2; symmetric encryption AES-GCM with no hardcoded keys
- [ ] Random number generation uses SecureRandom
- [ ] Actuator endpoints restricted + protected by authentication
- [ ] Global exception handler swallows stack traces; debug/devtools disabled in production; no sensitive data in logs
- [ ] Atomicity of amount/stock operations; state machine validation for multi-step flows
