---
name: testing-for-broken-access-control
description: Systematically tests web applications and APIs for broken access control
when-to-use: Systematically tests web applications and APIs for broken access control
  (OWASP A01:2021), including privilege escalation, missing function-level checks, insecure
  direct object references, and multi-tenant data leakage, using Burp Suite with the
  Authorize extension. Use during authorized penetration tests or RBAC/multi-tenant
  authorization audits.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- access-control
- authorization
- owasp
- privilege-escalation
- web-security
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
- T1059.007
- T1505.003
- T1083
- T1068
---

# Testing for Broken Access Control

## When to Use

- During authorized penetration tests as the primary assessment for OWASP A01:2021 - Broken Access Control
- When evaluating role-based access control (RBAC) implementations across all application endpoints
- For testing multi-tenant applications where users in one organization should not access another's data
- When assessing API endpoints for missing or inconsistent authorization checks
- During security audits where privilege escalation and unauthorized access are primary concerns

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Burp Suite Professional**: With Authorize extension for automated access control testing
- **Multiple test accounts**: Accounts at each role level (admin, manager, user, guest)
- **Application role matrix**: Documentation of what each role should and should not access
- **curl/httpie**: For manual endpoint testing with different authentication contexts
- **ffuf**: For discovering hidden endpoints that may lack access controls

## Workflow

### Step 1: Map All Endpoints and Create Access Control Matrix

Document every endpoint and the expected access level for each role.

```bash
# Extract all endpoints from Burp Site Map
# Target > Site Map > Right-click > Copy URLs in this host

# Build a matrix of endpoints vs roles:
# | Endpoint              | Admin | Manager | User | Guest |
# |-----------------------|-------|---------|------|-------|
# | GET /admin/dashboard  | Allow | Deny    | Deny | Deny  |
# | GET /api/users        | Allow | Allow   | Deny | Deny  |
# | PUT /api/users/{id}   | Allow | Deny    | Own  | Deny  |
# | DELETE /api/posts/{id} | Allow | Allow   | Own  | Deny  |

# Discover hidden endpoints
ffuf -u "https://target.example.com/FUZZ" \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt \
  -mc 200,301,302,403 -fc 404 \
  -H "Authorization: Bearer $USER_TOKEN" \
  -o endpoints.json -of json

# API endpoint discovery
ffuf -u "https://target.example.com/api/v1/FUZZ" \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,204,301,302,401,403,405 -fc 404 \
  -H "Authorization: Bearer $USER_TOKEN"
```

### Step 2: Configure Automated Access Control Testing

Set up Burp Authorize extension for parallel role-based testing.

```
# Install Authorize extension:
# Burp > Extender > BApp Store > Search "Authorize" > Install

# Configuration for three-tier testing:
# 1. Browse the application as Admin (capture all requests)
# 2. In Authorize tab:
#    a. Add Regular User's session token in "Replace cookies/headers"
#    b. Optionally add a second row for Unauthenticated (no auth header)

# Example header replacement setup:
# Row 1 (Low-privilege user):
#   Cookie: session=low_priv_user_session
#   Authorization: Bearer low_priv_token
#
# Row 2 (Unauthenticated):
#   [Empty - removes all auth headers]

# Enable interception in Authorize:
# - Check "Intercept requests from Proxy"
# - Check "Intercept requests from Repeater"

# Authorize shows results as:
# Green  = Properly restricted (different response for different user)
# Red    = POTENTIALLY VULNERABLE (same response regardless of role)
# Orange = Uncertain (needs manual verification)
```

### Step 3: Test Vertical Privilege Escalation

Attempt to access higher-privilege functionality with lower-privilege accounts.

```bash
# Collect tokens for each role
ADMIN_TOKEN="Bearer admin_jwt_here"
MANAGER_TOKEN="Bearer manager_jwt_here"
USER_TOKEN="Bearer user_jwt_here"

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
