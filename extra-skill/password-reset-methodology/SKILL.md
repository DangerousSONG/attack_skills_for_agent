---
name: password-reset-methodology
description: "Methodology for password reset and user registration / unauthorized profile modification. Use when the target has a forgot-password/password-reset flow, verification code reflection, check bypasses, arbitrary user password modification, unauthorized registration (endpoints such as registersysuser, goedituser), thinkphp mall login SMS verification codes, and similar scenarios. Covers password reset chain analysis, verification code reflection/brute force, SMS verification code bypass, arbitrary user password modification and unauthorized registration, authorization bypass on spring-style .do endpoints (e.g. login_tologin.do), and authorization boundaries"
zh-signals: "分析密码重置链路，排查验证码回显与爆破、短信验证码绕过、任意用户密码修改与越权注册等问题。信号:密码重置,验证码回显,任意用户密码修改,越权注册,鉴权绕过"
when-to-use: >-
  Use when a target has forgot-password/reset flows, verification-code
  reflection, check bypasses, arbitrary password change, or
  privilege-escalation registration endpoints.
metadata:
  tags: "password reset,password modification,verification code reflection,verification code,SMS verification code,check bypass,arbitrary user password modification,arbitrary user,privilege bypass,registration,registersysuser,goedituser,login_tologin.do,thinkphp,mall,login,reset,password,reset,assessment,authorization"
  category: "exploit"
---

# Password Reset / Unauthorized Registration and Modification Methodology

## Applicable Scenarios

Use when password recovery, verification codes, or user registration/profile modification endpoints are involved.

## Phase 1: Password Reset Chain Analysis

```
Forgot-password flow
├── Steps: phone number/email → verification code → password reset
├── Capture and analyze the request/response of every step
└── Key focus: how the verification code is validated, how it is returned, and whether it can be replayed
```

## Phase 2: Verification Code Troubleshooting

1. **Verification code reflection**: the response packet / API response contains the verification code directly (SMS/image/email code reflection)
2. **Verification code can be brute-forced**: the code is too short (4 digits) and there is no rate limit
3. **Verification code check bypass**: delete or blank out the code parameter, modify the response, replay concurrently, use a universal code
4. **SMS bombing / send endpoint not rate limited**: the endpoint that sends verification codes has no request count limit

## Phase 3: Arbitrary User Password Modification and Unauthorized Registration

- Replace the target phone number / user ID in the reset endpoint: `mobile=<target>&code=<your own code>`
- Unauthorized registration/profile modification endpoints: `registersysuser`, `goedituser` and similar endpoints have no authorization check or do not verify data ownership
- Validation method: use A's verification code to reset B's account; call administrative registration endpoints with low privileges or while unauthenticated
- Example: when a login/registration entry point like `login_tologin.do` has an authorization bypass, an administrator account can be registered without authorization

## Phase 4: thinkphp Mall SMS Verification Codes

- Common problems with SMS verification codes in mall-style systems (thinkphp framework): the code is stored in the Session so it can be used concurrently, the endpoint can be replayed, and the response packet leaks the code
- Test the verification code logic in login, registration, and password recovery separately

## Authorization Boundary

- Authorized penetration testing only
- Do not bulk-reset other people's accounts; stop as soon as unauthorized modification is confirmed

## Related Skills

- Authorization bypass supplement → 401-403-bypass
- Image captcha recognition and bypass → captcha-bypass-methodology
