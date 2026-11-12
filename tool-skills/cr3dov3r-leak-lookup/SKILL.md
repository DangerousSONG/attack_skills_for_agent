---
name: cr3dov3r-leak-lookup
description: "Cr3dOv3r: Collects leaked passwords and verifies credential reuse. Signals: email harvesting, employee information, silent mode, plaintext password databases only, no credential reuse testing."
zh-signals: "Cr3dOv3r: 收集泄露口令并验证凭据复用。信号:邮箱收集,员工信息,静默,只查明文密码库,不测试凭据复用。"
when-to-use: "Use when looking up leaked passwords for target emails and verifying credential reuse during OSINT or credential assessment. Requires target email addresses and optionally silent mode."
---

# Cr3dOv3r

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/D4Vinci/Cr3dOv3r
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/D4Vinci/Cr3dOv3r && cd Cr3dOv3r && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python Cr3dOv3r.py victim@email.com` | Breach database plus credential reuse check |
| `-q` | Quiet |
| `-p` | Plaintext password databases only |
| `-np` | Do not test credential reuse |

## Attack Scenario Playbook

### Collecting leaked passwords and verifying credential reuse

```bash
python Cr3dOv3r.py admin@corp.com
# Outputs HaveIBeenPwned breach records plus plaintext passwords, and attempts to reuse the login on various platforms
```

## Notes

Chains "lookup leaks" and "test reuse" into a single flow; project updates have slowed, so review the results manually.
