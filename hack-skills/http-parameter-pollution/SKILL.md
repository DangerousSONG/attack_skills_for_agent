---
name: http-parameter-pollution
description: "HTTP Parameter Pollution (HPP): duplicate query/body keys parsed differently by servers, proxies, WAFs, and app frameworks."
when-to-use: >-
  HTTP Parameter Pollution (HPP): duplicate query/body keys parsed differently by servers, proxies, WAFs, and app frameworks. Use when filters and application layers disagree on which value wins, enabling bypass, SSRF second URL, logic abuse, or CSRF token confusion.
---

# SKILL: HTTP Parameter Pollution (HPP)

> **AI LOAD INSTRUCTION**: Model the **full request path**: browser → CDN/WAF → reverse proxy → app framework → business code. Duplicate keys (`a=1&a=2`) are not an error at HTTP level; each hop may pick first, last, join, or array-ify. Test HPP when WAF and app disagree, or when internal HTTP clients rebuild query strings. Routing note: when the same parameter appears multiple times, or WAF/backend stacks differ, use the Section 1 matrix to test first/last/merge assumptions, then design Section 3 scenario chains.

## 0. QUICK START

**Hypothesis**: the **security check** reads one occurrence of a parameter while the **action** reads another.

### First-pass payloads

```text
id=1&id=2
id=1&id=1%20OR%201=1
url=https://legit.example&id=https://evil.example
amount=1&amount=9999
csrf=TOKEN_A&csrf=TOKEN_B
user=alice&user=admin
```

### Body variants (repeat for POST)

```text
application/x-www-form-urlencoded
id=1&id=2

multipart/form-data
------boundary
Content-Disposition: form-data; name="id"
1
------boundary
Content-Disposition: form-data; name="id"
2
```

### Quick methodology

1. Fingerprint **front** stack (CDN/WAF) vs **origin** (language/framework) using baseline `a=1&a=2`.
2. Send **both** orders: `a=1&a=2` and `a=2&a=1` (some parsers are order-sensitive).
3. If JSON: test **duplicate keys** and Content-Type confusion (see Section 2).

---

## 1. SERVER BEHAVIOR MATRIX

Typical defaults — **always confirm**; middleware and custom parsers override these.

| Technology | Behavior | Example: `a=1&a=2` |
|---|---|---|
| PHP / Apache (`$_GET`) | Last occurrence | `a=2` |
| ASP.NET / IIS | Often comma-joined (all) | `a=1,2` |
| JSP / Tomcat (servlet param) | First occurrence | `a=1` |
| Python / Django (`QueryDict`) | Last occurrence | `a=2` |
| Python / Flask (`request.args`) | First occurrence | `a=1` |
| Node.js / Express (`req.query`) | Array of values | `a=['1','2']` (shape may vary by parser version) |
| Perl / CGI | First occurrence | `a=1` |
| Ruby / Rack (Rack::Utils) | Last occurrence | `a=2` |
| Go `net/http` (`ParseQuery`) | First occurrence | `a=1` |

**Why it matters**: a WAF on **IIS** might see `1,2` while PHP backend receives `2` only — or the reverse if a proxy normalizes.

---

## 2. PAYLOAD PATTERNS

### 2.1 Basic duplicate key

```http
GET /api?q=safe&q=evil HTTP/1.1
```

### 2.2 Array-style (PHP / some frameworks)

```http
GET /api?id[]=1&id[]=2 HTTP/1.1
```

### 2.3 Mixed array + scalar

```http
GET /api?item[]=a&item=b HTTP/1.1
```

### 2.4 Encoded ampersand (parser differential)

```text
# Literal & inside a value vs new pair — depends on decoder
param=value1%26other=value2
param=value1&other=value2
```

### 2.5 Nested / bracket keys

```http
GET /api?user[name]=a&user[role]=user&user[role]=admin HTTP/1.1
```

### 2.6 JSON duplicate keys

```json
{"test":"user","test":"admin"}
```

Many parsers keep **last** key; some keep **first**. JavaScript `JSON.parse` keeps the last duplicate key.

---

## 3. ATTACK SCENARIOS

### 3.1 HPP + WAF bypass

**Pattern**: WAF inspects **first** value; application uses **last**.

```text
id=1&id=1%20UNION%20SELECT%20...
```

Also try: benign value in JSON field duplicated in query string, if gateway merges sources differently.

### 3.2 HPP + SSRF

**Pattern**: validator reads **safe** URL; fetcher reads **internal/evil** URL.

```text
url=https://allowed.cdn.example/&url=http://169.254.169.254/
```

Confirm which component (library vs app) consumes which occurrence.

### 3.3 HPP + CSRF

**Pattern**: duplicate anti-CSRF token so one copy satisfies parser A and another satisfies parser B.

```text
csrf=LEGIT&csrf=IGNORED_OR_ALT
```

Use only in **authorized** CSRF assessments with a clear state-changing target.

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
