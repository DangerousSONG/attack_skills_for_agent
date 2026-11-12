---
name: conpass-ad-mon
description: "conpass: Audits Active Directory password policies. Signals: AD attack, domain penetration, password policy and strength audit, weak password detection."
zh-signals: "conpass: AD 密码策略审计。信号:ad攻击,域渗透,密码策略+强度审计,弱口令检测。"
when-to-use: >-
  Use when you have AD credentials and need to audit the domain password
  policy and detect weak-password accounts before spraying.
---

# conpass

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/login-securite/conpass
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/login-securite/conpass && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `conpass -d corp.local -u svc -p pass --dc-ip 10.0.0.1` | Password policy + strength audit |
| `-d d -u u -p p --dc-ip ip -w` | Weak credential detection |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### AD Password Policy Audit

```bash
conpass -d corp.local -u svc -p pass
# Find accounts with weak credentials (by login-securite)
```

## Notes

By login-securite, an AD password policy analysis tool.
