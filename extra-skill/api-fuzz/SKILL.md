---
name: api-fuzz
description: "REST/GraphQL API security testing methodology. Use when the target has API endpoints (/api/, JSON responses), exposed Swagger/OpenAPI documentation, or an endpoint list obtained through js-api-extract or directory scanning. Covers API discovery, authentication testing, framework identification, semantic analysis-driven intelligent fuzzing (inferring parameter names/types/business meaning from endpoint semantics to build precise payloads), prototype pollution, and request smuggling. IDOR → idor-methodology | GraphQL → graphql-methodology | CSRF → csrf-methodology. Use this skill for any scenario involving API endpoint security testing, parameter discovery, or permission boundary testing"
zh-signals: "REST/GraphQL API 安全测试方法论，覆盖端点发现、认证测试与语义驱动智能 Fuzz。信号:api测试,rest,graphql,swagger,fuzz,参数发现"
when-to-use: >-
  Use when the target exposes API endpoints, JSON responses, or Swagger/OpenAPI docs, and you
  need endpoint discovery, authentication testing, semantic parameter fuzzing, or permission
  boundary testing.
metadata:
  tags: "api,fuzz,rest,json,swagger,openapi,endpoint,authentication,prototype pollution,semantic,parameter,crud,permission,parameter guessing,intelligent fuzz"
  category: "exploit"
---

# API Security Testing Methodology

## ⛔ Further Reading (Must Read)

- Authentication bypass techniques, parameter injection, Mass Assignment, request smuggling → [references/api-attack-techniques.md](references/api-attack-techniques.md)
- 403/405 bypasses (resource suffix fuzz dictionaries, empty POST JSON, Vue hash routes, prefix discovery) → [references/403-bypass-patterns.md](references/403-bypass-patterns.md)
- Endpoint semantic analysis, RESTful CRUD inference, parameter discovery, intelligent fuzzing, permission boundary testing, response analysis → [references/api-semantic-fuzz.md](references/api-semantic-fuzz.md)
- Fuzz payload templates classified by parameter semantics (ID/query/file/amount/command/Header) → [references/api-fuzz-payloads.md](references/api-fuzz-payloads.md)

---

## Phase 1: API Discovery and Documentation

### Endpoint Discovery
Key paths: `/api/`, `/v1/`, `/v2/`, `/graphql`, `/rest/`

### Documentation Leakage (Largest Source of Information)
- `/docs`, `/swagger`, `/swagger-ui`, `/swagger-ui.html`
- `/api-docs`, `/openapi.json`, `/openapi.yaml`

### Framework Identification
| Framework | Characteristics | Common Issues |
|------|------|----------|
| Spring Boot | `/actuator` endpoints | Actuator information disclosure, SpEL injection |
| Express/Koa | `X-Powered-By: Express` | Prototype pollution |
| FastAPI | auto-generated `/docs` | Swagger enabled by default |
| Django REST | `/api/?format=json` | Over-exposed serializers |
| Laravel | JSON API + PHP | Mass Assignment |

## Phase 2: Authentication Testing

```
API endpoints confirmed?
├─ Remove the auth header → unauthenticated access?
├─ IP/path/method bypass → [references/api-attack-techniques.md](references/api-attack-techniques.md)
├─ JWT → refer to jwt-attack-methodology
└─ OAuth → refer to oauth-sso-attack
```

## Phase 3: Semantic Analysis and Intelligent Fuzzing

After obtaining the endpoint list, first analyze the **business meaning** of each endpoint instead of blindly running a wordlist.

### RESTful CRUD Inference

Finding `GET /api/users/123` → infer the POST (create)/PUT (update)/DELETE (delete)/PATCH (Mass Assignment) endpoints

### Path Semantics → Testing Direction (Key Quick Reference)

| Endpoint Keyword | Testing Direction |
|-----------|----------|
| `users/{id}`, `order/{id}` | IDOR traversal |
| `search`, `query`, `q=` | SQL injection, XSS |
| `upload`, `import` | File upload bypass |
| `proxy`, `url=`, `redirect` | SSRF, open redirect |
| `template`, `render` | SSTI |
| `exec`, `run`, `cmd` | Command injection |
| `pay`, `amount`, `price` | Amount tampering (negative/zero/extreme values) |
| `admin`, `manage`, `config` | Broken access control (highest priority) |

→ Full semantic analysis methodology (parameter discovery, Content-Type variants, response analysis, batch IDOR verification, permission boundary testing) → [references/api-semantic-fuzz.md](references/api-semantic-fuzz.md)
→ Fuzz payload templates for each parameter type → [references/api-fuzz-payloads.md](references/api-fuzz-payloads.md)

## Phase 4: Targeted Test Entry Points

| Vulnerability Type | Focus |
|---------|--------|
| IDOR (accessing other users' data) | Traverse IDs/UUIDs, compare responses across users |
| GraphQL specific | Introspection/injection/permission bypass |
| CSRF (cross-site induced actions) | Token validation, SameSite, Referer checks |
| CORS (cross-origin data reads) | Origin whitelist, credential mode |

## Phase 5: Other Tests

### Prototype Pollution / Node.js Specific
- `__proto__` / `constructor.prototype` — pollution payload
- Exploit chains: eval, template injection (SSTI), server-side JS execution

### Request Smuggling
- [references/api-attack-techniques.md](references/api-attack-techniques.md)

### Path Parsing Differences
- Inconsistency between front end and back end, or proxy-layer differences, can bypass authentication
- Path variants: `/api/admin/.`, trailing dot, `/api/admin/..;/public`

## Notes
- APIs usually use JSON, so set `Content-Type: application/json`
- Error messages are more detailed than on the Web — an important source of information leakage
- API version differences (v1 may be vulnerable while v2 is fixed, with v1 still alive)
- Run the semantic analysis before fuzzing; do not blindly send requests and waste time
- Administrative endpoints (`/admin/`, `/manage/`) have the highest priority
- Immediately run `evidence_save` + `report_vuln` for each confirmed vulnerability
