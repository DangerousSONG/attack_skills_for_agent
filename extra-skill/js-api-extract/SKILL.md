---
name: js-api-extract
description: "JavaScript static analysis to extract hidden API endpoints. Use when the target is an SPA with a separate front-end/back-end architecture, when the page uses Vue/React/Angular, or when regular directory scanning yields little. Extracts API paths, keys, internal domains, and WebSocket endpoints by analyzing JS bundles. This is the information-gathering stage of API penetration testing. Once endpoints are found → use api-fuzz for semantic fuzzing"
zh-signals: "通过静态分析 JavaScript bundle 提取隐藏 API 端点、密钥与内部域名。信号:JS分析,API提取,SPA,bundle,信息收集"
when-to-use: "Use during reconnaissance against SPA or separate front-end/back-end targets to extract API paths, keys, internal domains, and WebSocket endpoints from JS bundles."
metadata:
  tags: "js,javascript,api,extract,spa,vue,react,angular,webpack,bundle,endpoint,front-end analysis"
  category: "recon"
---

# JavaScript API Endpoint Extraction Methodology

In a separate front-end/back-end architecture, the JS bundle is the **largest source of information** about API endpoints — 10 times more efficient than directory scanning.

## ⛔ Further Reading (Must Read)

- JS analysis regex library + extraction scripts → [references/js-extract-patterns.md](references/js-extract-patterns.md)

---

## Phase 1: JS File Collection

### 1.1 Collect from the Page HTML
```bash
# Grab every JS reference in the page
curl -s "$TARGET" | grep -oE '(src|href)="[^"]*\.js[^"]*"' | sed 's/.*="\(.*\)"/\1/'

# Recursive crawl (including iframes/dynamic loading)
curl -s "$TARGET" | grep -oP '(?:src|href|url)\s*[=:]\s*["\x27]([^"\x27]*\.js[^"\x27]*)["\x27]' | sort -u
```

### 1.2 Recover from Source Maps
```bash
# Check the sourceMappingURL at the end of the JS file
curl -s "$TARGET/static/js/app.xxx.js" | tail -1
# If there is //# sourceMappingURL=app.xxx.js.map
curl -s "$TARGET/static/js/app.xxx.js.map" -o sourcemap.json

# A source map exposes the full source code — equivalent to obtaining the front-end source
```

### 1.3 Collect from the Webpack Manifest
```bash
# Common chunk manifest files
/static/js/manifest.json
/asset-manifest.json
/webpack-manifest.json
/build/asset-manifest.json
/static/js/runtime~main.xxx.js  # the runtime chunk contains the mapping of all chunks
```

### 1.4 Historical Versions
```bash
# Use the Wayback Machine to fetch old JS (may contain APIs that were deleted but not decommissioned)
curl -s "https://web.archive.org/cdx/search/cdx?url=$DOMAIN/*.js&output=text&fl=original" | sort -u
```

## Phase 2: API Endpoint Extraction

### 2.1 Path Pattern Extraction
```bash
# Extract API paths from the JS content (the most critical step)
curl -s "$JS_URL" | grep -oP '["'"'"'](/(?:api|v[0-9]|rest|service|graphql|ws|internal|admin|auth|user|public)[^\s"'"'"']*?)["'"'"']' | sort -u

# Concatenated path extraction (common front-end pattern: baseURL + path)
curl -s "$JS_URL" | grep -oP '(?:baseURL|BASE_URL|API_URL|apiPrefix|apiBase)\s*[=:]\s*["'"'"']([^"'"'"']+)["'"'"']'

# Generic path extraction (including relative paths)
curl -s "$JS_URL" | grep -oP '["'"'"'](/[a-zA-Z][a-zA-Z0-9_/\-]{2,}(?:\?[^"'"'"']*)?)["'"'"']' | sort -u | grep -v '\.\(js\|css\|png\|jpg\|svg\|ico\|woff\|ttf\)'
```

### 2.2 Full URL Extraction
```bash
# Extract complete HTTP(S) URLs
curl -s "$JS_URL" | grep -oP 'https?://[^\s"'"'"'<>]+' | sort -u

# Extract internal domains/subdomains
curl -s "$JS_URL" | grep -oP 'https?://[a-zA-Z0-9._-]+\.DOMAIN\.com[^\s"'"'"']*' | sort -u
```

### 2.3 Key Information Extraction
```bash
# API Key / Secret / Token
curl -s "$JS_URL" | grep -oiP '(?:api[_-]?key|secret|token|auth|password|credential)\s*[=:]\s*["'"'"']([^"'"'"']{8,})["'"'"']'

# WebSocket endpoints
curl -s "$JS_URL" | grep -oP 'wss?://[^\s"'"'"']+' | sort -u

# Internal IPs/domains
curl -s "$JS_URL" | grep -oP '(?:10|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d+\.\d+' | sort -u
```

## Phase 3: Endpoint Classification and Prioritization

After extraction, classify by security value:

| Priority | Characteristics | Description |
|--------|------|------|
| 🔴 High | `/admin/`, `/internal/`, `/debug/`, `/manage/` | Administrative functions that may lack authentication |
| 🔴 High | `/upload`, `/import`, `/export`, `/download` | File operations that may allow path traversal/arbitrary read-write |
| 🔴 High | `/user/`, `/account/`, `/profile/`, `/order/` | User data operations, prime IDOR territory |
| 🟡 Medium | `/auth/`, `/login/`, `/register/`, `/reset/` | Authentication flows that may allow logic bypass |
| 🟡 Medium | `/search`, `/query`, `/filter` | Query interfaces, prime SQL injection territory |
| 🟢 Low | `/static/`, `/public/`, `/health`, `/status` | Static resources/health checks |

## Phase 4: Batch Validation

```bash
# Validate each extracted endpoint for liveness
for path in $(cat extracted_paths.txt); do
    code=$(curl -s -o /dev/null -w "%{http_code}" "$TARGET$path" --connect-timeout 5 -m 10)
    echo "$code $path"
done | grep -v "^404 " | sort
```

**Key indicators**:
- `200` → directly accessible, inspect the response content
- `401/403` → exists but requires authentication, attempt a bypass
- `405` → the endpoint exists but the method is wrong, try POST/PUT/DELETE
- `500` → backend error, there may be an injection point
- `301/302` → follow the redirect target

## Output Requirements

After extraction, output:
1. **JS file inventory** — which JS files were analyzed
2. **List of discovered API endpoints** — sorted by priority
3. **Exposed sensitive information** — API keys, internal domains, tokens
4. **Recommended next tests** — which endpoints should be fuzzed first
