---
name: php-logic-audit
description: "PHP web business logic vulnerability audit tool. Identifies logic flaws other than authentication/authorization issues: mass assignment, process bypass, race conditions, state machine defects, payment/permission timing flaws, and more. Outputs an evidence chain, severity rating, PoC, and remediation recommendations (omission is forbidden)."
zh-signals: "PHP 业务逻辑漏洞审计技能，识别 Mass Assignment、流程绕过、竞态条件、状态机与支付时序等缺陷。信号:业务逻辑,逻辑漏洞,越权,MassAssignment,竞态条件"
when-to-use: "Use when auditing PHP application source code for business logic flaws such as mass assignment, process bypass, race conditions, state machine defects, and payment or authorization timing issues."
---

# PHP Business Logic Vulnerability Audit (php-logic-audit)

Analyze defects related to "business process correctness" in PHP projects. Focus coverage:
- Mass Assignment (bulk assignment writes fields that should be privileged)
- Process bypass (missing prerequisite state, or validation that can be skipped)
- State machine defects (incomplete/revertible/inconsistent state updates)
- Race conditions (TOCTOU, concurrency leading to multiple payouts, duplicate charges, etc.)
- Missing business-layer authorization checks (linked to IDOR, but focused on business ownership consistency)
- Payment/refund/async task ordering flaws (async callbacks can be forged or processed repeatedly)

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-LOGIC-{sequence}`

## Mandatory Evidence
Every logic vulnerability must provide:
1. Trigger route and method (real route/HTTP method)
2. Prerequisite state (which conditions the attacker must satisfy: login state/role/resource state)
3. Defect location (business service/controller/callback handler/queue consumer logic)
4. State transition chain (input -> validation -> database write/external service call -> state update)
5. Concurrency/timing related evidence (if any: transaction boundaries/locks/unique constraints/idempotency handling)

## Mass Assignment Audit (Mandatory)
Must detect:
- Whether `$_POST/Request->all()/request()->all()` is written directly into models or the database
- Whether allowlists that restrict sensitive field updates are missing (e.g. `role/is_admin/status/price/owner_id`
- Whether ORM/framework mass assignment protection is enabled (for example Laravel `$fillable/$guarded`)

## Race Condition and Idempotency Audit (Mandatory)
Must detect:
- Whether the same operation can be executed multiple times concurrently (charge, shipment, upgrade, claim)
- Whether it relies on "read first, then write" (TOCTOU) without transactions/row locks
- Whether an idempotency key and deduplication exist (e.g. payment_id/nonce)

## Process Bypass Audit (Mandatory)
Must detect:
- Whether validation only exists on prerequisite pages while the backend lacks it
- Whether the flow is restricted only by hidden front-end fields/buttons
- Whether callback endpoints have reliable authentication and signature validation, and whether they can be called repeatedly

## Type Comparison Bypass and Weak Typing Audit (Mandatory)
Weak typing/loose comparisons in PHP frequently lead to authentication/authorization/business logic bypass and must be audited:
- Whether `==`/`!=` (non-strict comparison) is used for authorization decisions, state checks, or permission validation
- Whether `in_array($x, $arr)` is used without the strict mode flag (third parameter), allowing type coercion bypass
- Whether results of `array_search`, `strpos`, etc. are mishandled in conditional checks (for example `strpos` returning 0 treated as false, or mixed with strings/numbers)
- Whether `md5/sha1` is used for "authentication validation" with digests compared directly using `==` (must identify whether `hash_equals` is used)
- Whether token/JWT/captcha comparison logic uses methods vulnerable to timing inference or type-juggling bypass (the comparison function/condition expression must be evidenced)

Every weak typing vulnerability must provide:
- Location evidence (comparison expression/conditional statement/relevant function call site)
- Source (how user input reaches the comparison)
- Sink (branch outcome caused by the faulty comparison: allow/bypass/error state)
- PoC (request sequence or payload, at least covering "how the comparison value is crafted to trigger the bypass")

## Authentication/Account Workflow Logic (Mandatory)
Must audit business process security related to "state transitions":
- Whether password reset tokens are single-use, have an explicit expiry, and are bound to the user
- Whether OTP/captchas allow replay (whether the same token/nonce can be reused)
- Whether login failure counts/account lockout/rate limiting are implemented and enforced on the backend
- Account enumeration: whether error messages/response codes/timing differences leak whether a user exists
- Whether payment/refund callbacks are idempotent (whether the same transaction is credited or fulfilled repeatedly)

The PoC must give at least a two-step request sequence: first establish the prerequisite state, then trigger the state transition action, and annotate the observation points (database field/response code/redirect/callback execution count).

## PoC (Mandatory)
Logic vulnerability PoCs must provide a "request sequence":
- At least two steps: trigger prerequisite condition -> trigger the vulnerable action (annotate the real route)
- For race condition flaws: provide the concurrency request method and observation points (for example the steps for sending two curl requests simultaneously)

## Report Output
```
{output_path}/vuln_audit/logic_{timestamp}.md
```

## Entry Template (Mandatory)
- Location evidence
- Defect description (must be based on code semantics, not generic wording alone)
- State transition chain
- Exploitable prerequisite conditions
- Request sequence PoC
- Remediation recommendations (including: allowlist/transactions/locks/idempotency/backend re-validation)
