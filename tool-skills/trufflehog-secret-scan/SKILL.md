---
name: trufflehog-secret-scan
description: "trufflehog harvests GitHub key leaks and internal credentials from employee forks. Signals: attack surface, cloud assets, scan single repository, scan whole org"
zh-signals: "trufflehog: Github 密钥泄露收割、员工 fork 仓库找内部凭证。信号:攻击面,云资产,扫单个仓库,扫整个 org。"
when-to-use: >-
  Use when scanning GitHub repositories, organizations, GitLab or local filesystems for leaked secrets, with verification to confirm which credentials are still live.
---

# trufflehog

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/trufflesecurity/trufflehog
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/trufflesecurity/trufflehog@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `trufflehog github --repo=https://github.com/org/repo` | Scan a single repository |
| `trufflehog github --org=orgname` | Scan an entire org |
| `trufflehog gitlab --endpoint=...` | GitLab |
| `--only-verified` | Report only verified, live keys |
| `-j` | JSON output |
| `trufflehog filesystem ./leak-repo` | Scan a local directory |

## Attack Scenario Playbook

### Harvest GitHub Key Leaks

```bash
trufflehog github --org=target-org --only-verified -j | tee keys.json
# AWS keys/Slack tokens/private keys are automatically verified for validity
```

### Find Internal Credentials in Employee Fork Repositories

```bash
trufflehog github --repo=https://github.com/employee/fork --only-verified
```

## Notes

Supports 800+ key types with automatic verification; --only-verified greatly reduces false positives.
