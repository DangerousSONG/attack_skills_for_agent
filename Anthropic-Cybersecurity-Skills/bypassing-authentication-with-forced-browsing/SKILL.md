---
name: bypassing-authentication-with-forced-browsing
description: "Discovering and accessing unprotected pages, APIs, and administrative 信号:web漏洞,注入,sql注入。"
when-to-use: Discovering and accessing unprotected pages, APIs, and administrative
  interfaces by enumerating URLs and bypassing authentication controls during authorized
  security assessments.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- authentication-bypass
- forced-browsing
- ffuf
- directory-enumeration
- owasp
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1083
- T1087
---

# Bypassing Authentication with Forced Browsing

## When to Use

- During authorized penetration tests to discover hidden or unprotected administrative pages
- When testing whether authentication is consistently enforced across all application endpoints
- For identifying backup files, configuration files, and debug interfaces left exposed in production
- When assessing access control on API endpoints that should require authentication
- During security audits to validate that all sensitive resources enforce session validation

## Prerequisites

- **Authorization**: Written penetration testing agreement covering directory enumeration
- **ffuf**: Fast web fuzzer (`go install github.com/ffuf/ffuf/v2@latest`)
- **Gobuster**: Directory brute-force tool (`apt install gobuster`)
- **Burp Suite**: For intercepting and analyzing requests and responses
- **Wordlists**: SecLists collection (`git clone https://github.com/danielmiessler/SecLists.git`)
- **Target access**: Network connectivity and valid test credentials for authenticated comparison

## Workflow

### Step 1: Enumerate Hidden Directories and Files

Use ffuf or Gobuster to discover paths not linked in the application's navigation.

```bash
# Directory enumeration with ffuf
ffuf -u https://target.example.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt \
  -mc 200,301,302,403 \
  -fc 404 \
  -o results-dirs.json -of json \
  -t 50 -rate 100

# File enumeration with common extensions
ffuf -u https://target.example.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-files.txt \
  -e .php,.asp,.aspx,.jsp,.html,.js,.json,.xml,.bak,.old,.txt,.cfg,.conf,.env \
  -mc 200,301,302,403 \
  -fc 404 \
  -o results-files.json -of json \
  -t 50 -rate 100

# Gobuster for directory enumeration
gobuster dir -u https://target.example.com \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -s "200,204,301,302,307,403" \
  -x php,asp,aspx,jsp,html \
  -o gobuster-results.txt \
  -t 50
```

### Step 2: Discover Administrative and Debug Interfaces

Target common administrative paths and debug endpoints.

```bash
# Admin panel enumeration
ffuf -u https://target.example.com/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/common.txt \
  -mc 200,301,302 \
  -t 50 -rate 100

# Common admin paths to check manually:
# /admin, /administrator, /admin-panel, /wp-admin
# /cpanel, /phpmyadmin, /adminer, /manager
# /console, /debug, /actuator, /swagger-ui
# /graphql, /graphiql, /.env, /server-status

# API endpoint discovery
ffuf -u https://target.example.com/api/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,204,301,302,401,403 \
  -fc 404 \
  -o api-results.json -of json

# Check for Spring Boot Actuator endpoints
for endpoint in env health info beans configprops mappings trace; do
  curl -s -o /dev/null -w "%{http_code} /actuator/$endpoint\n" \
    "https://target.example.com/actuator/$endpoint"
done
```

### Step 3: Test Authentication Enforcement on Discovered Endpoints

Compare responses between unauthenticated and authenticated requests.

```bash
# Test without authentication
curl -s -o /dev/null -w "%{http_code}" \
  "https://target.example.com/admin/dashboard"

# Test with valid session cookie
curl -s -o /dev/null -w "%{http_code}" \
  -b "session=valid_session_token_here" \
  "https://target.example.com/admin/dashboard"

# Automated check: compare response sizes
# Unauthenticated request
curl -s "https://target.example.com/admin/users" | wc -c

# Authenticated request
curl -s -b "session=valid_token" \
  "https://target.example.com/admin/users" | wc -c

# If both return similar content, authentication is not enforced

# Test with Burp Intruder: send a list of discovered URLs
# without cookies and flag any 200 responses
```

### Step 4: Test HTTP Method-Based Authentication Bypass

Some applications only enforce authentication for specific HTTP methods.

```bash

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
