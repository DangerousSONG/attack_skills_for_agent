---
name: code-audit
description: "Authorized source-code security review and SAST workflows: Semgrep and CodeQL pattern hunting, dangerous API identification, and fix verification."
zh-signals: "授权源码安全审查与 SAST 工作流，使用 Semgrep、CodeQL 等检索危险 API、注入点并验证修复。信号:代码审计,SAST,Semgrep,CodeQL,漏洞验证"
when-to-use: >-
  Use when reviewing a codebase for security defects with static analysis, or
  verifying that a vulnerability fix removes the flawed pattern within an authorized
  repository.
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# Source Code Security Audit
## When to Use

- Reviewing a codebase for security defects with static analysis.
- Verifying that a vulnerability fix actually removes the flawed pattern.


## Applicable Scenarios

- White-box audits, PR / diff security review
- SAST with Semgrep / CodeQL / Bandit / gosec
- Dangerous APIs, injection points, missing authorization, cryptographic misuse
- Division of labor with `supply-chain-security/`: this skill focuses on **first-party code logic**, while supply chain focuses on dependencies and pipelines

## Workflow

### 1. Scope and Threat Model

```text
□ Trust boundaries: user input, files, deserialization, SSRF, authentication middleware
□ High-value assets: authentication, payments, admin panels, key handling
```

### 2. Automated Scanning

```bash
semgrep --config auto .
# or the project rule pack
semgrep --config p/owasp-top-ten .
```

### 3. Manual Verification (MUST)

```text
□ Every SAST hit: reachable? exploitable? false positive?
□ Authorization: IDOR / broken access control, missing checks, faulty multi-tenant isolation
□ Injection: SQL / command / template / LDAP
□ Cryptography: hardcoded keys, ECB, custom crypto
```

### 4. Deliverables

```text
Finding: location + data flow + PoC + remediation recommendation
Optional ATT&CK / CWE identifiers
```

## Toolchain

| Tool | Language / Scenario |
|------|-----------|
| Semgrep | Fast multi-language rules |
| CodeQL | Deep data flow (GitHub) |
| Bandit | Python |
| gosec / staticcheck | Go |
| SpotBugs / FindSecBugs | Java |

## References

- `references/sast-review-checklist.md`
- `../supply-chain-security/` `../api-security/` `../llm-security/` (Agent code)

## Routing Context

**Upstream**: MASTER R26  
**Role**: `ops/role-map.md` cae  
**Downstream**: dependency vulnerabilities → supply-chain; runtime verification → pentest-tools

## Task Completion Self-Check

- [ ] Did I verify manually instead of only pasting scanner output?
- [ ] Does the report contain remediation recommendations?
- [ ] Is the work limited to the authorized repository scope?
- [ ] Checklist?

## Limitations

- Static analysis produces false positives; manual triage is required.
- Coverage depends on language support of the chosen SAST engine.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
