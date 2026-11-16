---
name: database-security
description: "Authorized database security assessment across PostgreSQL, MySQL, MSSQL, MongoDB, and Redis: exposure, authorization gaps, UDF/command execution paths, and misconfiguration review."
zh-signals: "对 PostgreSQL、MySQL、MSSQL、MongoDB 与 Redis 开展授权数据库安全评估，检查暴露面、授权缺陷与命令执行路径。信号:数据库安全,PostgreSQL,MySQL,Redis,权限评估"
when-to-use: >-
  Use when assessing database hardening and exposure across PostgreSQL, MySQL, MSSQL,
  MongoDB, or Redis — authorization gaps, UDF/command execution paths, and
  misconfiguration.
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

> **Mandatory confirmation gate**
> Before running any command that probes, exploits, changes, persists on, extracts data from, or attempts credential access against a target:
> 1. Ask the user to state the exact target URL, IP, account, or resource.
> 2. Ask the user to confirm written authorization and the permitted scope.
> 3. Show the exact command(s) and explain their expected effect.
> 4. Wait for explicit confirmation in the current conversation.
>
> Without that confirmation, remain read-only and provide defensive guidance only. Prefer a sandbox, disposable VM, or controlled lab.

# Database Security Assessment
## When to Use

- Assessing database hardening and exposure within an approved scope.
- Checking authz boundaries and risky server-side execution features.


## Applicable Scenarios

- Unauthenticated access / weak credentials / databases bound to 0.0.0.0
- Overly broad privileges, dangerous features (xp_cmdshell, COPY PROGRAM, UDF)
- Lateral movement: from an application account to DBA
- NoSQL injection and Redis file write, etc. (authorized environments)

## Workflow

```text
□ Network exposure and TLS
□ Account roles and grantees
□ Access control on sensitive tables
□ Dangerous configurations: file_priv, xp_cmdshell, load_file
□ Is audit logging enabled
□ Backup and snapshot permissions
```

## Toolchain

| Tool | Purpose |
|------|------|
| Official CLI | connection and enumeration |
| sqlmap | injection verification (authorized) |
| nuclei | known exposure templates |
| Cloud RDS console audit | configuration |

## References

- `references/db-misconfig-checklist.md`
- `../pentest-tools/` `../cloud-k8s/`

## Routing Context

**Upstream**: MASTER R35  
**Downstream**: obtaining OS commands → attack-chain; cloud-hosted → cloud-k8s

## Task Completion Self-Check

- [ ] Was unauthorized writing/deleting avoided?
- [ ] Were configuration issues distinguished from exploitable chains?
- [ ] Checklist?

## Limitations

- Never run against production data stores without explicit written approval.
- Active exploitation paths (UDF/command exec) are destructive-capable; simulate first.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
