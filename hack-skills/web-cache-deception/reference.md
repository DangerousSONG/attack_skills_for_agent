# web-cache-deception — 详细参考（由 SKILL.md 拆分）

# Application treats these as equivalent:
/account/profile
/account/profile/anything
/account/profile/x.css
/account/profile;.css

# CDN treats .css as cacheable static asset
→ Mismatch = vulnerability
```

---

## 5. CACHE POISONING REAL-WORLD PATTERN

### X-Forwarded-Host → Open Graph / Meta Tag Injection

```text
# Target page uses X-Forwarded-Host to generate meta tags:
GET / HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com

# Response:
<meta property="og:image" content="https://evil.com/assets/logo.png">
# or:
<link rel="canonical" href="https://evil.com/">

# If response is cached → all users see evil.com references
# Impact: XSS via injected JS path, phishing via canonical redirect, SEO hijack
```

### Cache Deception with Path Separator Tricks

```text
# Semicolon (treated as path parameter by some frameworks):
/account/profile;.css

# Encoded separators:
/account/profile%2F.css

# Trailing dot/space:
/account/profile/.css
/account/profile .css
```

---

## 6. DEFENSE

### For Cache Deception

- Cache only explicitly static paths (e.g., `/static/*`, `/assets/*`)
- Never cache based on file extension alone
- Set `Cache-Control: no-store, private` on authenticated endpoints
- Use `Vary: Cookie` to prevent cross-user cache hits

### For Cache Poisoning

- Include all reflected headers in cache key
- Validate and sanitize `X-Forwarded-*` headers
- Use `Cache-Control: no-cache` for dynamic content
- Strip unknown headers at CDN edge

---

## 6. TESTING CHECKLIST

```
□ Identify CDN/cache layer (X-Cache, Age, Via headers)
□ Append .css/.js/.png to authenticated API endpoints
□ Check if response is cached (X-Cache: HIT on second request)
□ Test path separators: /x.css, ;.css, %2F.css
□ Test unkeyed headers: X-Forwarded-Host, X-Original-URL
□ Verify Cache-Control headers on sensitive endpoints
□ Check Vary header presence
□ Test with and without authentication
```
