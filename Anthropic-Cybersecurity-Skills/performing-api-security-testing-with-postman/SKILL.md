---
name: performing-api-security-testing-with-postman
description: "Use Postman to build structured API security test collections. Signals: api attack, interface testing, graphql."
zh-signals: "Uses Postman to build structured API security test collections covering 信号:api攻击,接口测试,graphql。"
when-to-use: 'Uses Postman to build structured API security test collections covering
  the OWASP API Security Top 10—authentication bypass, authorization flaws, injection,
  and data exposure—with multi-role environments, automated test scripts, and OWASP
  ZAP/Newman integration for CI/CD. Use when building repeatable Postman-based API
  security regression tests or automating OWASP API Top 10 coverage in a pipeline.

  '
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- postman
- owasp
- automated-testing
- security-validation
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
- T1055
- T1059
---
# Performing API Security Testing with Postman

## When to Use

- Building repeatable API security test suites for OWASP API Security Top 10 coverage
- Creating automated security regression tests that run in CI/CD pipelines via Newman
- Testing API authentication and authorization across multiple user roles systematically
- Integrating Postman with OWASP ZAP proxy for combined manual and automated security testing
- Establishing a baseline security test collection for new API endpoints before deployment

**Do not use** against production APIs without authorization. Postman security testing involves sending potentially malicious payloads.

## Prerequisites

- Postman Desktop or web application with an active workspace
- Target API with OpenAPI/Swagger specification for collection import
- Test accounts for at least three roles: unauthenticated, regular user, admin
- Newman CLI installed for CI/CD integration: `npm install -g newman`
- OWASP ZAP configured as local proxy (localhost:8080) for Postman proxy integration
- API environment variables for base URL, tokens, and test data

## Workflow

### Step 1: Environment and Collection Setup

Create Postman environments for multi-role testing:

```json
// Environment: API Security Test - Regular User
{
    "values": [
        {"key": "base_url", "value": "https://target-api.example.com/api/v1"},
        {"key": "auth_token", "value": ""},
        {"key": "user_email", "value": "regular@test.com"},
        {"key": "user_password", "value": "TestPass123!"},
        {"key": "user_id", "value": ""},
        {"key": "other_user_id", "value": "1002"},
        {"key": "admin_endpoint", "value": "/admin/users"},
        {"key": "test_order_id", "value": ""},
        {"key": "other_user_order_id", "value": "5003"}
    ]
}
```

**Pre-request script for automatic authentication:**
```javascript
// Collection-level pre-request script for auto-login
if (!pm.environment.get("auth_token") || pm.environment.get("token_expired")) {
    const loginRequest = {
        url: pm.environment.get("base_url") + "/auth/login",
        method: "POST",
        header: {"Content-Type": "application/json"},
        body: {
            mode: "raw",
            raw: JSON.stringify({
                email: pm.environment.get("user_email"),
                password: pm.environment.get("user_password")
            })
        }
    };

    pm.sendRequest(loginRequest, (err, res) => {
        if (!err && res.code === 200) {
            const token = res.json().access_token;
            pm.environment.set("auth_token", token);
            pm.environment.set("user_id", res.json().user.id);
        }
    });
}
```

### Step 2: BOLA (API1) Test Collection

```javascript
// Test: Access other user's profile (BOLA)
// Request: GET {{base_url}}/users/{{other_user_id}}
// Auth: Bearer {{auth_token}}

// Test script:
pm.test("BOLA: Cannot access other user profile", function() {
    pm.expect(pm.response.code).to.be.oneOf([401, 403]);
});

pm.test("BOLA: No user data leaked on denial", function() {
    if (pm.response.code === 200) {
        const body = pm.response.json();
        pm.expect(body).to.not.have.property("email");
        pm.expect(body).to.not.have.property("phone");
        pm.expect(body).to.not.have.property("address");
        // Flag as BOLA if full profile returned
        console.error("BOLA VULNERABILITY: Full profile returned for other user");
    }
});

// Test: Access other user's order
// Request: GET {{base_url}}/orders/{{other_user_order_id}}
pm.test("BOLA: Cannot access other user order", function() {
    pm.expect(pm.response.code).to.be.oneOf([401, 403, 404]);
});

// Test: Modify other user's resource
// Request: PATCH {{base_url}}/users/{{other_user_id}}
// Body: {"name": "Hacked"}
pm.test("BOLA: Cannot modify other user profile", function() {
    pm.expect(pm.response.code).to.be.oneOf([401, 403]);
});
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
