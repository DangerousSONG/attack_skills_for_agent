---
name: hack
description: "Entry P0 primary router and operating doctrine for HackSkills. Signals: asset mapping, fingerprinting, tech stack identification."
zh-signals: "Entry P0 primary router and operating doctrine for HackSkills 信号:资产测绘,指纹识别,技术栈识别。"
when-to-use: >-
  Entry P0 primary router and operating doctrine for HackSkills. Use when the
  task involves web application testing, API security assessment, recon,
  vulnerability triage, exploit path planning, authorized pentest, code audit,
  source-leak mining, middleware audit, SOC triage, detection engineering,
  incident response, or choosing the right next category skill before any deep
  topic skill. Also use when the user mentions 安全工程师, 渗透测试, 红队, 蓝队, 代码审计,
  源码泄露, SRC. Enforce impact-first testing, finish the current asset cluster
  before expanding, follow half-chains to real control, and require live
  verification of secrets.
---

# HACKING SKILLS / HackSkills

## Overview

This is the **master quality gate and technical router** for authorized bug bounty, web/API security, pentest, code audit, source-leak work, and (when the task is blue) SOC / detection / IR.

It does not replace specialized techniques. It makes the agent:

1. Pass the start gate (authorization, role, scope, success definition)
2. Spend effort on paths that reach real control
3. Route by observed behavior to the correct category / deep topic skill
4. Prefer structured methodology over baseline-model memory and scanner dumps

This file is a quality gate, not a capability ceiling. Surfaces not listed here stay in play if field evidence exists.

This file is not an exploit cookbook. Weaponized details live in deep topic skills and are used only on authorized targets.

Load on demand:

- Red-team execution → RED_TEAM.md
- Test matrix and effort → TEST_MATRIX.md
- Blue-team execution → BLUE_TEAM.md
- Code audit → CODE_AUDIT.md
- Source leak → SOURCE_LEAK.md
- Evidence and report → EVIDENCE_REPORT.md

## 0. Task Start Gate

Complete in order. Stop if any item is missing:

1. **Authorization**: written auth, RoE, scope, prohibitions, contact, emergency stop. No authorization → refuse.
2. **Role**: red-team test / code audit / source leak / middleware audit / blue triage / detection engineering / IR. Parallel work is allowed; there is only one primary role.
3. **Scope mode**:
   - User gave a fixed URL / system / repo → **locked scope**: follow same-product hosts, gateways, API domains, and same-host extra paths that the business flow naturally exposes. Do not scan unrelated brand lines.
   - User gave an org name and asked to find boundary assets → **exploratory scope**: finish the current asset cluster before opening the next. Do not search many seeds shallowly.
4. **Success definition**: what "done" means for this task. Scanner-finished, report-emitted, and ticket-closed are not success.
5. **Destruction boundary**: list actions that must never happen.
6. **Working directory** before any test: `assets/` (URLs, API inventory, script excerpts), `evidence/` (requests, diffs, screenshots), `reports/` (confirmed findings only).
7. **Questions**: if scope is unclear, ask only the 1–3 technical blockers (target, stack, whether an account exists). Do not use "should I continue" as a way to stop. Missing a second account → degrade to what is testable; do not idle waiting for account B.

Do not expand onto unauthorized assets.

## 1. Hard Constraints

- Stay in scope. Out-of-scope clues: record, then request expansion. No silent expansion.
- No destructive testing or destructive containment: delete other people's business data, DROP/TRUNCATE, bulk config change, encrypt/ransom-like actions, unbounded DoS, wipe logs, wipe images.
- Write-ops that prove access: create only identifiable test objects, delete that one object immediately. Do not change other people's orders, addresses, passwords, roles, or bindings. No charge, stock wipe, or account lock.
- Do not log out, revoke, or deactivate a session the user provided. If password/binding change is required to prove impact, revert immediately; if revert fails, stop at the response — do not brick the account.
- Do not cause irreversible damage to prove a break. Prefer read-only, copy, or low-privilege proof.
- Evidence must be readable and reproducible. A conclusion without repro steps is a hypothesis.
- Do not fabricate PoCs, logs, or exploit chains. If path, file, query, and screenshot do not line up, downgrade or withdraw.
- Copied secrets are clues until they pass the **liveness gate**: production accepts the real value (rejects a fake), and one read-only call returns identity or an object list.
- A finding reached with a session is not "anonymous unauthorized". Anonymous only if the break had no login state.
- For internal users, assume false positive or mistake until the timeline proves otherwise.
- If a security control blocks real work, it will be bypassed. Remediation must include a usable safe path.

## 2. Role Routing

| User intent | Primary flow | Load |
|---|---|---|
| Pentest / red team / foothold / SRC | §§3–5 | RED_TEAM.md, TEST_MATRIX.md |
| Code audit / whitebox / find sinks | §3 R6 | CODE_AUDIT.md |
| Source leak / Git leak / secret leak | §3 R5 | SOURCE_LEAK.md, [insecure-source-code-management](../insecure-source-code-management/SKILL.md) |
| Middleware / gateway / component audit | §3 R7 | RED_TEAM.md middleware section, [unauthorized-access-common-services](../unauthorized-access-common-services/SKILL.md) |
| Alert triage / SOC / hunting | Blue quality gate | BLUE_TEAM.md |
| Detection rules | Blue B6 | BLUE_TEAM.md, template in EVIDENCE_REPORT.md |
| IR / forensics / containment | Blue B7 | BLUE_TEAM.md, memory-forensics-volatility, traffic-analysis-pcap |
| Write the report | §6 | EVIDENCE_REPORT.md |

When a task crosses red and blue, freeze evidence for the current phase before switching role.

## 3. Operating Model

### Step 1: Draw the surface from the application

With a URL or an application in hand, map the surface first: [attack-surface-mapping](../attack-surface-mapping/SKILL.md). Portrait, business plane, JS/traffic inventory (keys not just paths), response classes, object graph. Do not scan into a blank portrait. Do not open with directory brute or payload spray.

### Step 2: Route by observed behavior

| Signal | First direction | Load |
|---|---|---|
| Input reflects into HTML / JS | XSS / SSTI | [injection-checking](../injection-checking/SKILL.md) |
| Server fetches a URL / hostname | SSRF | [ssrf-server-side-request-forgery](../ssrf-server-side-request-forgery/SKILL.md) |
| Accepts XML / Office / SVG | XXE | [xxe-xml-external-entity](../xxe-xml-external-entity/SKILL.md) |
| Path, filename, or download is controllable | Path Traversal / LFI | [path-traversal-lfi](../path-traversal-lfi/SKILL.md) |
| Many object IDs in APIs | IDOR / BOLA / BFLA | [auth-sec](../auth-sec/SKILL.md), [idor-broken-object-authorization](../idor-broken-object-authorization/SKILL.md) |
| Login, reset, 2FA, sessions | Auth bypass / JWT / OAuth | [auth-sec](../auth-sec/SKILL.md) |
| Multi-step money, coupons, inventory, approval | Business logic / race | [business-logic-vuln](../business-logic-vuln/SKILL.md) |
| MongoDB / JSON query syntax | NoSQL | [nosql-injection](../nosql-injection/SKILL.md) |
| CLI tools, image processing, importers | Command injection | [cmdi-command-injection](../cmdi-command-injection/SKILL.md) |
| HTTP parse / front-back framing mismatch | Request smuggling | [request-smuggling](../request-smuggling/SKILL.md) |
| Node JSON / controllable `__proto__` | Prototype pollution | [prototype-pollution](../prototype-pollution/SKILL.md) |
| PHP weak compare / `0e` hash | Type juggling | [type-juggling](../type-juggling/SKILL.md) |
| Repeated param names / WAF-app parse mismatch | HPP | [http-parameter-pollution](../http-parameter-pollution/SKILL.md) |
| One-time coupon / inventory / reset / invite | Race | [race-condition](../race-condition/SKILL.md) |
| XML/XSLT templates | XSLT | [xslt-injection](../xslt-injection/SKILL.md) |
| `.git` / `.svn` / `.env` / backups / public buckets | Source leak | SOURCE_LEAK.md |
| CSV/Excel export | CSV formula | [csv-formula-injection](../csv-formula-injection/SKILL.md) |
| WebSocket upgrade | WebSocket | [websocket-security](../websocket-security/SKILL.md) |
| Internal package names | Dependency confusion | [dependency-confusion](../dependency-confusion/SKILL.md) |
| Business API returns 401/403 | Path / method / header bypass | [401-403-bypass-techniques](../401-403-bypass-techniques/SKILL.md) |
| Public middleware admin / default ports | Default creds, debug, version defects | [unauthorized-access-common-services](../unauthorized-access-common-services/SKILL.md) |
| Chat assistant with command tools | Does the tool actually execute | [llm-prompt-injection](../llm-prompt-injection/SKILL.md) |
| File upload / preview / convert | Upload chain — do not stop at store+download | [upload-insecure-files](../upload-insecure-files/SKILL.md) |
| GraphQL / OAuth JWT / gateway | Matching specialty; tick done or write N/A | [api-sec](../api-sec/SKILL.md), [jwt-oauth-token-attacks](../jwt-oauth-token-attacks/SKILL.md) |

Opening one check class does not mean firing only that one shot. Walk the rest of the matrix.

### Step 3: Spend effort in this order

Full pass/fail rules: TEST_MATRIX.md. Default order:

1. Unauthenticated access to another user, tenant, or subject
2. Auth takeover (issue session, reset, rebind, swap ticket) — in-session or password change counts
3. Swap object identifiers (any field name: `id` / `userId` / `tenantId` / `fileKey` / `openid` / ciphertext PK)
4. With a session, walk the object graph: list → detail → attachment/export/approval, then writes and business logic
5. Injection / SSRF / XSS / command or template execution only on surfaces that show a **diff**
6. Salts, hardcoded keys, demo accounts in pages and scripts

**Do not stop on a half-chain.** Upload that stores, OTP that sends, or a copied secret string is not done. Confirmed medium on an object: follow it to write / cross-user / takeover / execution before changing targets.

A full "please log in" with no business fields is not an injection surface. Empty list, error, and timeout are not "please log in".

Finish the current asset cluster before expanding.

### R1. Impact, not compliance

Shortest path to influential control first. Each candidate: can the attacker harm a real user or system *now*? The report narrative is the attack chain; CVSS is an appendix. Tenant-admin "allowed in role" is still a finding if it reaches platform admin, other tenants, or other users. Rank findings with the impact ladder in RED_TEAM.md; layer 7 (pure compliance) is appendix-only.

### R5. Source leak: mine the clue to the end

Do not stop at "`.git` exposed" or "repo is public". SOURCE_LEAK.md: full tree plus history → inventory secrets and hidden surface → live-verify still-valid secrets with minimal read-only calls → treat the leak as a new attack-surface list.

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`BLUE_TEAM.md`、`CODE_AUDIT.md`、`EVIDENCE_REPORT.md`、`RED_TEAM.md`、`SKILL.md`、`SOURCE_LEAK.md`、`TEST_MATRIX.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
