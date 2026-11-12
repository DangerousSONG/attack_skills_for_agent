---
name: testing-for-business-logic-vulnerabilities
description: "Identifies business logic flaws like price manipulation. Signals: API attacks, interface testing, GraphQL."
zh-signals: "Manually identifies flaws in application business logic - price manipulation 信号:api攻击,接口测试,graphql。"
when-to-use: Manually identifies flaws in application business logic - price manipulation,
  multi-step workflow bypass, and privilege escalation - by intercepting and modifying
  requests with Burp Suite, going beyond what automated vulnerability scanners detect.
  Use for e-commerce checkout/cart flows, voucher and rewards systems, or any assessment
  where scanners find little but business rules need scrutiny.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- business-logic
- owasp
- web-security
- burpsuite
- manual-testing
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

# Testing for Business Logic Vulnerabilities

## When to Use

- During authorized penetration tests when automated scanners have found few technical vulnerabilities
- When assessing e-commerce platforms for pricing, cart, and payment flow manipulations
- For testing multi-step workflows (registration, checkout, approval processes) for bypass opportunities
- When evaluating rate-limited features like vouchers, coupons, referrals, and rewards systems
- During security assessments of financial applications, voting systems, or any application with critical business rules

## Prerequisites

- **Authorization**: Written penetration testing agreement covering business logic testing
- **Burp Suite Professional**: For intercepting and modifying multi-step request flows
- **Application understanding**: Thorough knowledge of the application's intended business workflows
- **Multiple test accounts**: Accounts at different privilege levels and states
- **Browser DevTools**: For examining client-side validation logic
- **Documentation**: Business requirements or user stories describing expected behavior

## Workflow

### Step 1: Map Business Workflows and Rules

Document all critical business processes and their expected constraints.

```
# Critical business flows to map:
# 1. Registration/Onboarding flow
#    - Email verification requirements
#    - Account approval process
#    - Role assignment logic

# 2. E-commerce/Purchase flow
#    - Product selection → Cart → Checkout → Payment → Confirmation
#    - Price calculation logic
#    - Discount/coupon application
#    - Quantity limits
#    - Shipping cost calculation

# 3. Authentication/Authorization flow
#    - Login → MFA → Dashboard
#    - Password reset → Token → New password
#    - Role escalation/approval

# 4. Financial transactions
#    - Balance check → Transfer → Confirmation
#    - Withdrawal limits
#    - Currency conversion

# Document expected constraints:
# - Minimum order amounts
# - Maximum quantity per item
# - Coupon usage limits (one per user)
# - Referral reward caps
# - Withdrawal daily limits
# - Account verification requirements before certain actions
```

### Step 2: Test Price and Quantity Manipulation

Intercept and modify price, quantity, and total values in requests.

```bash
# Test negative quantity
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": -1, "price": 99.99}' \
  "https://target.example.com/api/cart/add"

# Test zero price
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1, "price": 0}' \
  "https://target.example.com/api/cart/add"

# Test extremely large quantity
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 999999999}' \
  "https://target.example.com/api/cart/add"

# Test decimal/float manipulation
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 0.001, "price": 0.01}' \
  "https://target.example.com/api/cart/add"

# Test integer overflow
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2147483647}' \
  "https://target.example.com/api/cart/add"

# Modify total amount directly in checkout request
# Intercept in Burp and change total from 299.99 to 0.01
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": "abc123", "total": 0.01, "payment_method": "card"}' \
  "https://target.example.com/api/checkout"
```

### Step 3: Test Workflow Step Bypass

Attempt to skip required steps in multi-step processes.

```bash
# Skip email verification
# Instead of: Register → Verify email → Access dashboard

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
