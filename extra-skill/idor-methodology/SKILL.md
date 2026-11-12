---
name: idor-methodology
description: "IDOR insecure direct object reference and unauthorized access detection and exploitation. Use when APIs or URLs expose predictable identifiers such as user_id, account, order number, or filename, or when you need to test horizontal privilege escalation (accessing other people's data), vertical privilege escalation (a normal user gaining admin privileges), or interface-level privilege bypass. Covers ID enumeration, bypass techniques (parameter pollution/encoding/method switching), multi-step IDOR chains, file resource IDOR, bulk operation privilege bypass, indirect reference enumeration, framework-specific exploitation, UUID guessing, response comparison analysis, write-operation privilege bypass, JWT Claims tampering, token/session permission check bypass, and missing role/permission checks. Always load this skill after discovering API endpoints to check for privilege bypass and unauthorized access issues"
zh-signals: "检测与利用 IDOR 越权及未授权访问，覆盖水平/垂直越权与绕过技巧。信号:IDOR,越权访问,对象引用,ID遍历,权限绕过。"
when-to-use: >-
  Use when APIs or URLs expose predictable object identifiers such as user_id, account, order number, or filename, and you need to test horizontal or vertical authorization flaws.
metadata:
  tags: "idor,insecure direct object reference,privilege_escalation,authorization,access-control,bola,privilege-bypass,horizontal-privilege-escalation,vertical-privilege-escalation,permission-bypass,object-reference,bypass,hpp,file-idor,bulk-operation,api,permission,role,admin,user_id,account,privilege,token,session,jwt,api-idor,unauthorized-access"
  category: "exploit"
---

# IDOR Insecure Direct Object Reference Methodology

IDOR is one of the most common API vulnerabilities — developers check "are you logged in" but never check "are you allowed to access this record". Change one number and you get someone else's data; change one role and you become an administrator.

## ⛔ Further Reading

- Bypass techniques (parameter wrapping, encoding, HPP, method switching) → [references/idor-bypass-techniques.md](references/idor-bypass-techniques.md)
- Advanced patterns (multi-step chains, file IDOR, bulk operations, indirect references, framework fingerprints, evidence standards) → [references/idor-advanced-patterns.md](references/idor-advanced-patterns.md)
- Bulk detection scripts, write-operation privilege bypass, identifier predictability table → [references/idor-techniques.md](references/idor-techniques.md)

---

## Phase 1: Discovering IDOR Entry Points

Any location carrying an object identifier is an IDOR candidate:

| Location | Example | Priority |
|------|------|--------|
| URL path | `/api/users/1001` | 🔴 High |
| Query parameter | `?user_id=1001&order_id=5003` | 🔴 High |
| POST/PUT body | `{"user_id": 1001}` | 🔴 High |
| Cookie/Header | `uid=1001` / `X-User-Id: 1001` | 🟡 Medium |
| File path | `/uploads/user_1001/avatar.jpg` | 🟡 Medium |
| GraphQL variable | `query { user(id: 1001) {...} }` | 🔴 High |
| WebSocket message | `{"action":"getProfile","uid":1001}` | 🟡 Medium |

**Key identification signals**: auto-increment integers, short sequence numbers (ORD-001), Base64-encoded IDs, file names/paths in URLs.

## Phase 2: Horizontal Privilege Escalation Testing (Read Operations)

At least two accounts are required (register two, or know your own ID).

```
Token of account A (uid=1001):
GET /api/users/1001/profile → 200 (own data, record as baseline)
GET /api/users/1002/profile → 200 + different data? → IDOR!
GET /api/users/1/profile    → admin data? → vertical privilege escalation!
GET /api/users/0/profile    → 500 error leaking internal information?
```

**Response comparison analysis** (status code alone is not enough):
| Response | Verdict | Next Step |
|------|------|--------|
| 200 + different user data | ✅ IDOR confirmed | Save evidence, test write operations |
| 200 + identical data | Backend ignored the ID parameter | Try another endpoint |
| 200 + empty data | User does not exist or data is empty | Try another ID range |
| 403/401 | Permission checks exist | Attempt bypass → Phase 5 |
| 404 | ID does not exist | Try another ID range or enumerate |
| 500 | Backend error | Analyze the error message |

→ Bulk detection script → [references/idor-techniques.md](references/idor-techniques.md)

## Phase 3: Write-Operation Privilege Bypass

Once read privilege bypass is confirmed, write operations are 10 times more dangerous — changing a password means taking over an account:

```
PUT    /api/users/1002         {"email":"evil@x.com"}    → account takeover
PATCH  /api/users/1002         {"password":"hacked"}     → password change
DELETE /api/orders/5003                                   → delete someone else's order
POST   /api/users/1/reset-pwd                             → reset the admin password
PUT    /api/users/1002/role    {"role":"admin"}           → privilege escalation
```

**Important**: many applications enforce permission checks on GET but forget them on POST/PUT/DELETE — test every HTTP method.

## Phase 4: Vertical Privilege Escalation

Access administrative functionality with a normal user identity:

```
GET  /api/admin/users          → admin user list?
POST /api/admin/create-user    → can create users?
GET  /api/admin/config         → system configuration leak?
GET  /api/internal/dashboard   → internal dashboard?
```

### Approval/Workflow System Privilege Bypass

In OA, contract approval, and ticketing systems, "approve" operations are the most typical vertical privilege escalation targets — call the administrator's approval interface with an employee identity:

```
# For example
POST   /contracts/1/approve
PATCH  /contracts/1  {"status":"approved"}
POST   /api/admin/approval  {"id":1,"action":"approve"}
```

**Key**: approval endpoints are often not standalone files but embedded in the dashboard's `$_POST['action']` handling. If there is LFI/source access, search the source code for `approve`/`action` to locate the exact endpoint instead of guessing paths blindly.

**JWT Claims tampering**: decode the JWT → change `"role":"user"` to `"role":"admin"` → forgeable if `alg:none` or a weak key is used

**Mass Assignment**: inject `{"role":"admin","is_admin":true}` during registration/update

## Phase 5: IDOR Bypass Techniques

When basic testing returns 403, do not give up — many permission checks can be bypassed:

| Bypass Technique | Example |
|----------|------|
| ID parameter wrapping | `id=1002` → `id[]=1002`, `id={"$eq":1002}` |
| HTTP method switching | GET 403 → PUT/PATCH/DELETE 200? |
| Path variation | `/api/v1/` → `/api/v2/`, `/api/internal/` |
| Encoding bypass | Base64, Hex, double URL encoding |
| Parameter pollution (HPP) | `?id=mine&id=victim` (the backend may take the last one) |
| Content-Type switching | JSON→XML→form-urlencoded (different parsers, different filters) |
| Request smuggling/chunking | Bypass the permission checks of the front-end proxy |

→ Complete bypass payloads and scripts → [references/idor-bypass-techniques.md](references/idor-bypass-techniques.md)

## Phase 6: Multi-Step IDOR Chains

Many IDORs are not single-step — you need to obtain information from endpoint A and then exploit it at endpoint B:

```
1. GET /api/comments → a comment leaks user_id: 1002
2. GET /api/users/1002/profile → read the profile with the leaked ID
3. GET /api/users/1002/orders → read further order data

1. GET /api/invites?code=ABC → the response contains group_id: 77
2. GET /api/groups/77/members → obtain the member list with the leaked group_id
```

**ID leak hunting checklist**: comments, messages, logs, invite links, share links, exported files, API error responses, GraphQL introspection, JS front-end code.

→ Detailed hunting process → [references/idor-advanced-patterns.md](references/idor-advanced-patterns.md)

## Phase 7: File/Media Resource IDOR

Uploaded files often have far weaker permission checks than API data:

```
/uploads/user_1001/avatar.jpg   → change 1001 to 1002
/attachments/report-001.pdf     → enumerate the numbers
/export/data-20260101.csv       → change the date and enumerate
/media/a1b2c3d4.jpg             → predictable hash?
```

**S3/OSS direct links**: if the file URL is `https://bucket.s3.amazonaws.com/users/1001/doc.pdf`, changing the path directly may bypass the application-layer permission check.

## Phase 8: Bulk Operations and Indirect References

### Bulk Operation IDOR
```json
// Bulk endpoints may skip per-item permission checks entirely
POST /api/users/bulk {"ids": [1001, 1002, 1003, 1004]}
POST /api/orders/export {"order_ids": [5001, 5002, 5003]}

// GraphQL batch
[
  {"query": "{ user(id:1) { email } }"},
  {"query": "{ user(id:2) { email } }"}
]
```

### Indirect Reference IDOR
Use email/phone/username instead of numeric IDs:
```
GET /api/users?email=victim@test.com     → look up others by email
POST /api/password-reset {"phone":"13800138001"}  → reset by phone number
GET /api/profile/john_doe                → the username is the identifier
```

→ Detailed patterns → [references/idor-advanced-patterns.md](references/idor-advanced-patterns.md)

## Phase 9: Framework-Specific IDOR

Different back-end frameworks have different high-incidence IDOR patterns:

| Framework | High-incidence point | Reason |
|------|--------|------|
| Spring Data REST | `/{entity}/{id}` fully exposed | Auto-generated CRUD endpoints with no permissions by default |
| Django REST Framework | `/api/{model}/{pk}/` | ViewSets are open by default, permission_classes often forgotten |
| Express + Mongoose | `/api/users/:id` | Incorrect middleware ordering causes authorization to be skipped |
| Laravel | `/api/{model}/{id}` | Route Model Binding auto-queries, Policy often forgotten |
| GraphQL (any) | `query { node(id:"...") }` | Relay Global ID may expose arbitrary objects |

## Evidence Collection Standards

A valid IDOR PoC must prove that you **saw someone else's data**, not your own:

1. **Request/response pair**: the complete HTTP request (including the authentication header) + the complete response
2. **Two-account comparison**: account A accesses account B's data, account B accesses the same endpoint to confirm the data belongs to B
3. **Key field annotation**: highlight the sensitive fields in the returned data (name, email, phone number)
4. **ID difference proof**: explicitly mark that the ID in the request differs from the currently logged-in user's ID

```
✅ Good evidence:
"Using account A's token (uid=1001) to request /api/users/1002/profile returned
account B's name (Zhang San), email (zhangsan@test.com), and phone number"

❌ Poor evidence:
"Requesting /api/users/1002 returned 200"
(no proof that the returned data belongs to someone else)
```

**As soon as an IDOR is confirmed, run `evidence_save` + `report_vuln` immediately**, including: request URL, request headers, response status code, and a summary of the sensitive data in the response.

## CTF Specifics: Flag Retrieval
Access `/api/flag`, `/admin/flag` | Check the admin profile/notes | Check the user with ID=1 or a high-privilege user | `/api/users/0` or `/api/users/-1`
