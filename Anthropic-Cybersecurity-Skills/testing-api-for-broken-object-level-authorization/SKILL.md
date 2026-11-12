---
name: testing-api-for-broken-object-level-authorization
description: "Tests REST and GraphQL APIs for BOLA/IDOR. Signals: API attacks, interface testing, GraphQL."
zh-signals: "Tests REST and GraphQL APIs for Broken Object Level Authorization (BOLA/IDOR) 信号:api攻击,接口测试,graphql。"
when-to-use: 'Tests REST and GraphQL APIs for Broken Object Level Authorization (BOLA/IDOR,
  OWASP API1:2023) by intercepting API calls, identifying object ID parameters (numeric
  IDs, UUIDs, slugs), and systematically substituting IDs belonging to other users
  to check whether the server enforces per-object authorization. Use when asked to
  test BOLA or IDOR in an API, verify object-level authorization, or assess an API
  for access control bypass.

  '
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- owasp
- bola
- idor
- authorization
- rest-security
version: 1.0.0
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
- T1552.001
- T1027
- T1070
---
# Testing API for Broken Object Level Authorization

## When to Use

- Assessing REST or GraphQL APIs that use object identifiers in URL paths, query parameters, or request bodies
- Performing OWASP API Security Top 10 assessments where API1:2023 (BOLA) must be tested
- Testing multi-tenant SaaS applications where users from different tenants should not access each other's data
- Validating that API endpoints enforce per-object authorization checks beyond just authentication
- Evaluating APIs after new endpoints are added to ensure authorization middleware is applied consistently

**Do not use** without written authorization from the API owner. BOLA testing involves accessing or attempting to access other users' data, which requires explicit permission.

## Prerequisites

- Written authorization specifying the target API endpoints and scope of testing
- At least two test accounts with different privilege levels and distinct data sets
- Burp Suite Professional or OWASP ZAP configured as an intercepting proxy
- Authentication tokens (JWT, session cookies, API keys) for each test account
- API documentation (OpenAPI/Swagger spec) or access to enumerate endpoints
- Python 3.10+ with `requests` library for scripted testing
- Autorize Burp extension installed for automated BOLA detection

## Workflow

### Step 1: API Endpoint Discovery and Object ID Mapping

Enumerate all API endpoints and identify parameters that reference objects:

**From OpenAPI/Swagger Specification:**
```bash
# Download and parse the OpenAPI spec
curl -s https://target-api.example.com/api/docs/swagger.json | python3 -m json.tool

# Extract all endpoints with path parameters
curl -s https://target-api.example.com/api/docs/swagger.json | \
  python3 -c "
import json, sys
spec = json.load(sys.stdin)
for path, methods in spec.get('paths', {}).items():
    for method, details in methods.items():
        if method in ('get','post','put','patch','delete'):
            params = [p['name'] for p in details.get('parameters',[]) if p.get('in') in ('path','query')]
            if params:
                print(f'{method.upper()} {path} -> params: {params}')
"
```

**From Burp Suite Traffic:**
1. Browse the application as User A, exercising all features that involve data creation and retrieval
2. In Burp, go to Target > Site Map and filter for API paths (e.g., `/api/v1/`, `/graphql`)
3. Look for patterns: `/api/v1/users/{id}`, `/api/v1/orders/{order_id}`, `/api/v1/documents/{doc_uuid}`
4. Note the object ID format: sequential integers (predictable), UUIDs (less predictable), or encoded values

**Classify Object ID Types:**

| ID Type | Example | Predictability | BOLA Risk |
|---------|---------|---------------|-----------|
| Sequential Integer | `/orders/1042` | High - increment/decrement | Critical |
| UUID v4 | `/orders/550e8400-e29b-41d4-a716-446655440000` | Low - random | Medium (if leaked) |
| Encoded/Hashed | `/orders/base64encodedvalue` | Medium - decode and predict | High |
| Composite | `/users/42/orders/1042` | High - multiple IDs to swap | Critical |
| Slug | `/profiles/john-doe` | Medium - guess usernames | High |

### Step 2: Baseline Request Capture with Authenticated User

Capture legitimate requests for User A and User B:

```python
import requests

BASE_URL = "https://target-api.example.com/api/v1"

# User A credentials
user_a_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
user_a_headers = {"Authorization": user_a_token, "Content-Type": "application/json"}

# User B credentials
user_b_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
user_b_headers = {"Authorization": user_b_token, "Content-Type": "application/json"}

# Step 1: Identify User A's objects
user_a_profile = requests.get(f"{BASE_URL}/users/me", headers=user_a_headers)
user_a_id = user_a_profile.json()["id"]  # e.g., 1001

user_a_orders = requests.get(f"{BASE_URL}/users/{user_a_id}/orders", headers=user_a_headers)
user_a_order_ids = [o["id"] for o in user_a_orders.json()["orders"]]  # e.g., [5001, 5002]

# Step 2: Identify User B's objects
user_b_profile = requests.get(f"{BASE_URL}/users/me", headers=user_b_headers)
user_b_id = user_b_profile.json()["id"]  # e.g., 1002

user_b_orders = requests.get(f"{BASE_URL}/users/{user_b_id}/orders", headers=user_b_headers)
user_b_order_ids = [o["id"] for o in user_b_orders.json()["orders"]]  # e.g., [5003, 5004]

print(f"User A (ID: {user_a_id}): Orders {user_a_order_ids}")
print(f"User B (ID: {user_b_id}): Orders {user_b_order_ids}")
```

### Step 3: BOLA Testing - Horizontal Privilege Escalation

Attempt to access User B's objects using User A's authentication:

```python
import json

results = []

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
