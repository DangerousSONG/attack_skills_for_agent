---
name: testing-api-security-with-owasp-top-10
description: "Assesses REST, GraphQL, and gRPC APIs against OWASP. Signals: API attacks, interface testing."
zh-signals: "Systematically assesses REST, GraphQL, and gRPC API endpoints against the OWASP 信号:api攻击,接口测试。"
when-to-use: Systematically assesses REST, GraphQL, and gRPC API endpoints against the OWASP
  API Security Top 10 (2023) using Burp Suite and Postman for automated and manual testing.
  Use during authorized API penetration tests, before deploying new endpoints to production,
  or when validating API gateway controls and rate limiting.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- api-security
- owasp
- rest-api
- graphql
- burpsuite
- postman
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
---

# Testing API Security with OWASP Top 10

## When to Use

- During authorized API penetration testing engagements
- When assessing REST, GraphQL, or gRPC APIs for security vulnerabilities
- Before deploying new API endpoints to production environments
- When reviewing API security posture against the OWASP API Security Top 10 (2023)
- For validating API gateway security controls and rate limiting effectiveness

## Prerequisites

- **Authorization**: Written scope document covering all API endpoints to be tested
- **Burp Suite Professional**: For intercepting and modifying API requests
- **Postman**: For organizing and executing API test collections
- **ffuf**: For API endpoint and parameter fuzzing
- **curl/httpie**: Command-line HTTP clients for manual testing
- **API documentation**: Swagger/OpenAPI spec, GraphQL schema, or API docs
- **jq**: JSON processor for parsing API responses (`apt install jq`)

## Workflow

### Step 1: Discover and Map API Endpoints

Enumerate all available API endpoints and understand the API surface.

```bash
# If OpenAPI/Swagger spec is available, download it
curl -s "https://api.target.example.com/swagger.json" | jq '.paths | keys[]'
curl -s "https://api.target.example.com/v2/api-docs" | jq '.paths | keys[]'
curl -s "https://api.target.example.com/openapi.yaml"

# Fuzz for API endpoints
ffuf -u "https://api.target.example.com/api/v1/FUZZ" \
  -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt \
  -mc 200,201,204,301,401,403,405 \
  -fc 404 \
  -H "Content-Type: application/json" \
  -o api-enum.json -of json

# Fuzz for API versions
for v in v1 v2 v3 v4 beta internal admin; do
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://api.target.example.com/api/$v/users")
  echo "$v: $status"
done

# Check for GraphQL endpoint
for path in graphql graphiql playground query gql; do
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST -H "Content-Type: application/json" \
    -d '{"query":"{__typename}"}' \
    "https://api.target.example.com/$path")
  echo "$path: $status"
done
```

### Step 2: Test API1 - Broken Object Level Authorization (BOLA)

Test whether users can access objects belonging to other users by manipulating IDs.

```bash
# Authenticate as User A and get their resources
TOKEN_A="Bearer eyJhbGciOiJIUzI1NiIs..."
curl -s -H "Authorization: $TOKEN_A" \
  "https://api.target.example.com/api/v1/users/101/orders" | jq .

# Try accessing User B's resources with User A's token
curl -s -H "Authorization: $TOKEN_A" \
  "https://api.target.example.com/api/v1/users/102/orders" | jq .

# Fuzz object IDs with Burp Intruder or ffuf
ffuf -u "https://api.target.example.com/api/v1/orders/FUZZ" \
  -w <(seq 1 1000) \
  -H "Authorization: $TOKEN_A" \
  -mc 200 -t 10 -rate 50

# Test IDOR with different ID formats
# Numeric: /users/102
# UUID: /users/550e8400-e29b-41d4-a716-446655440000
# Encoded: /users/MTAy (base64)
```

### Step 3: Test API2 - Broken Authentication

Assess authentication mechanisms for weaknesses.

```bash
# Test for missing authentication
curl -s "https://api.target.example.com/api/v1/users" | jq .

# Test JWT token vulnerabilities
# Decode JWT without verification
echo "eyJhbGciOiJIUzI1NiIs..." | cut -d. -f2 | base64 -d 2>/dev/null | jq .

# Test "alg: none" attack
# Header: {"alg":"none","typ":"JWT"}
# Create unsigned token with modified claims

# Test brute-force protection on login
ffuf -u "https://api.target.example.com/api/v1/auth/login" \
  -X POST -H "Content-Type: application/json" \
  -d '{"email":"admin@target.com","password":"FUZZ"}' \
  -w /usr/share/seclists/Passwords/Common-Credentials/top-1000.txt \
  -mc 200 -t 5 -rate 10

# Test password reset flow
curl -s -X POST "https://api.target.example.com/api/v1/auth/reset" \
  -H "Content-Type: application/json" \
  -d '{"email":"victim@target.com"}'

# Check if token is in response body instead of email only
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
