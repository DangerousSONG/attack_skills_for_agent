# testing-for-host-header-injection — 详细参考（由 SKILL.md 拆分）

# Enumerate virtual hosts
for vhost in admin staging dev test api internal backend; do
  status=$(curl -H "Host: $vhost.target.com" http://target.com/ -o /dev/null -w "%{http_code}" -s)
  size=$(curl -H "Host: $vhost.target.com" http://target.com/ -o /dev/null -w "%{size_download}" -s)
  echo "$vhost.target.com - Status: $status, Size: $size"
done

# Check default virtual host behavior
curl -H "Host: nonexistent.target.com" http://target.com/ -v
# Compare with legitimate host response

# Access internal admin panels via virtual host
curl -H "Host: admin" http://target.com/
curl -H "Host: management.internal" http://target.com/
```

### Step 6 — Test Connection-State Attacks
```bash
# HTTP/1.1 connection reuse attack
# Send legitimate first request, then inject Host header on subsequent request
# Use Burp Repeater with "Update Content-Length" and manual Connection: keep-alive

# In Burp Repeater, send grouped request:
# Request 1 (legitimate):
# GET / HTTP/1.1
# Host: target.com
# Connection: keep-alive
#
# Request 2 (injected):
# GET /admin HTTP/1.1
# Host: internal.target.com

# Test with HTTP Request Smuggling combined
# If front-end validates Host but back-end doesn't:
# Smuggle request with modified Host header
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| Host Header | HTTP header specifying the target virtual host for the request |
| Password Reset Poisoning | Injecting Host to make reset emails contain attacker-controlled URLs |
| Cache Poisoning via Host | Poisoning CDN cache with responses containing attacker-controlled host |
| Virtual Host Routing | Web server using Host header to route requests to different applications |
| X-Forwarded-Host | Alternative header used by proxies that may override Host header |
| Connection State Attack | Exploiting persistent connections to send requests with different Host values |
| Server-Side Host Resolution | Backend code using Host header for URL generation and redirects |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy for Host header manipulation and analysis |
| Burp Collaborator | Out-of-band detection for Host header SSRF |
| ffuf | Virtual host brute-forcing with custom Host headers |
| gobuster vhost | Virtual host enumeration mode |
| Nuclei | Template-based scanning for Host header injection |
| param-miner | Burp extension for discovering unkeyed Host-related headers |

## Common Scenarios

1. **Password Reset Token Theft** — Poison Host header during password reset to make victim click a link pointing to attacker server, leaking reset token
2. **Web Cache Poisoning** — Inject Host header to cache responses with attacker-controlled JavaScript URLs, achieving stored XSS for all users
3. **Internal Panel Access** — Enumerate and access internal admin panels through virtual host manipulation
4. **SSRF to Cloud Metadata** — Use Host header to redirect server-side requests to cloud metadata endpoints
5. **Routing Bypass** — Bypass access controls by manipulating Host to route requests to unprotected backend instances

## Output Format

```
## Host Header Injection Report
- **Target**: http://target.com
- **Reverse Proxy**: Nginx
- **Backend**: Apache/PHP

### Findings
| # | Technique | Header | Impact | Severity |
|---|-----------|--------|--------|----------|
| 1 | Password Reset Poisoning | Host: evil.com | Token theft | Critical |
| 2 | Cache Poisoning | X-Forwarded-Host: evil.com | Stored XSS | High |
| 3 | Virtual Host Access | Host: admin.target.com | Admin panel exposure | High |
| 4 | SSRF | Host: 169.254.169.254 | Metadata access | Critical |

### Remediation
- Validate Host header against a whitelist of expected values
- Do not use Host header for generating URLs in password reset emails
- Configure web server to reject requests with unrecognized Host values
- Set absolute URLs in application configuration instead of deriving from Host
```
