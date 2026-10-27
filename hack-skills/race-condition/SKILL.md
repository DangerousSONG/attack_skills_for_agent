---
name: race-condition
description: "Race condition and TOCTOU testing for web apps 信号:漏洞情报,cve,cnvd。"
when-to-use: >-
  Race condition and TOCTOU testing for web apps. Use when testing one-time operations, concurrent HTTP abuse, rate-limit bypass, Turbo Intruder gates, HTTP/2 single-packet attacks, and CWE-362-style synchronization gaps.
---

# SKILL: Race Conditions — Testing & Exploitation Playbook

> **AI LOAD INSTRUCTION**: Treat race conditions as **authorization/state integrity** issues: non-atomic read-then-write lets multiple requests observe stale state. Prioritize **one-time** or **balance-like** operations. Combine **parallel transport** (HTTP/1.1 last-byte sync, HTTP/2 single-packet, Turbo Intruder gates) with **application evidence** (duplicate success responses, inconsistent balances, duplicate ledger rows). **Authorized testing only.** Routing note: for business workflows, coupons, inventory, or one-time rewards, start with this skill and cross-load `business-logic-vulnerabilities`.

---

## 0. QUICK START — What to Test First

Target endpoints where **check** and **update** are unlikely to be a single atomic database operation:

| Priority | Operation class | Example paths / parameters |
|----------|------------------|----------------------------|
| 1 | One-time redeem / coupon / bonus | `redeem`, `apply_coupon`, `claim_reward`, `voucher` |
| 2 | Balance / quota / stock deduction | `transfer`, `purchase`, `reserve`, `inventory` |
| 3 | Invite / referral / signup bonus | `invite_accept`, `referral_claim` |
| 4 | Password / email / MFA verification | `verify_token`, `confirm_email`, `reset_password` |
| 5 | Idempotent-looking APIs without strong keys | `POST` that should succeed only once per user |

**First moves (conceptual)**:

1. Capture the **state-changing** request in a proxy.
2. Send **20–100** copies **as simultaneously as your tooling allows**.
3. Classify outcome: **0/1 expected successes** vs **N successes** or **inconsistent final state**.

---

## 1. CORE CONCEPT

### 1.1 TOCTOU (Time-of-check to time-of-use)

```
Thread A                    Thread B
   |                            |
   +-- CHECK (resource OK)      |
   |                            +-- CHECK (resource OK)  ← both see "OK"
   +-- USE / UPDATE             |
   |                            +-- USE / UPDATE           ← duplicate effect
```

**TOCTOU** means the **decision** (check) and the **mutation** (use) are not one indivisible step.

### 1.2 Non-atomic read-then-write

Typical vulnerable pseudo-flow:

```text
balance = SELECT balance FROM accounts WHERE id = ?
if balance >= amount:
    UPDATE accounts SET balance = balance - ? WHERE id = ?
```

Two concurrent requests can both pass the `if` before either `UPDATE` commits.

### 1.3 Database-level vs application-level locking gaps

| Layer | What goes wrong |
|-------|------------------|
| **Application** | In-memory flag, cache, or session says "not used yet" while DB already updated — or the reverse. |
| **ORM / service** | Two instances, no distributed lock; each thinks it owns the decision. |
| **DB** | Missing `SELECT … FOR UPDATE`, wrong isolation level, or logic split across multiple statements without transaction. |
| **API gateway** | Per-IP rate limit is **check-then-increment** — parallel burst passes duplicate checks. |

**Hint**: `UNIQUE` constraints and **idempotency keys** often eliminate entire bug classes — test whether the app **enforces** them on the hot path.

---

## 2. ATTACK PATTERNS

### 2.1 Limit-overrun (double redeem / double claim)

Send the **same** authenticated request many times in parallel:

```http
POST /api/v1/rewards/claim HTTP/1.1
Host: target.example
Authorization: Bearer <token>
Content-Type: application/json

{"reward_id":"welcome_bonus"}
```

**Success signal**: HTTP `200`/`201` more than once, duplicate ledger entries, or balance higher than policy allows.

### 2.2 Rate-limit bypass via simultaneity

If limits are implemented as **counters checked per request** without atomic increment:

```http
POST /api/v1/login HTTP/1.1
Host: target.example
Content-Type: application/json

{"email":"victim@example.com","password":"wrong"}
```

Fire **N** parallel attempts in one wave; compare with **N** sequential attempts.

**Success signal**: more failures accepted than documented cap, or lockout never triggers when burst completes inside one window.

### 2.3 Multi-step exploitation (beat the pipeline)

Workflow: `create → pay → confirm`. If **confirm** does not cryptographically bind to **pay** completion:

1. Start two parallel pipelines from the same session/item.
2. Complete **confirm** on channel B while **pay** on channel A is still in-flight or abandoned.

**Success signal**: item marked paid/shipped without matching payment, or state skips backward.

---

## 3. HTTP/1.1 LAST-BYTE SYNCHRONIZATION

**Idea**: Hold all requests **blocked** until every socket has sent the full request **except the last byte** of the body; then release the final byte together so the server receives them in a tight cluster.

```text
Client 1: [headers + body - 1 byte] ----hold----+
Client 2: [headers + body - 1 byte] ----hold----+--> flush last byte together
Client N: [headers + body - 1 byte] ----hold----+
```

**Why**: Reduces **network jitter** between copies compared to naive sequential paste in Repeater.

**Tooling**: Custom scripts, some Burp extensions, or **Turbo Intruder** `gate` pattern (see §5) as the practical stand-in for synchronized release.

---

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
