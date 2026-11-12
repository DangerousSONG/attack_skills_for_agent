---
name: deathstar-automation
description: "DeathStar: one-click automated Active Directory domain penetration. Signals: AD attack, domain penetration, automated domain admin path, domain controller."
zh-signals: "DeathStar: 一键自动化域渗透。信号:ad攻击,域渗透,自动化域管路径,域控。"
when-to-use: >-
  Use when you hold low-privilege domain credentials and want to automate
  Active Directory privilege escalation toward Domain Admin. Requires a
  domain, username/password, and optionally a domain controller address.
---

# DeathStar

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/ByronLeeeee/DeathStar
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ByronLeeeee/DeathStar && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 deathstar.py -u svc -p pass -d corp.local` | Automated path to Domain Admin |
| `-u u -p p -d d -dc 10.0.0.1` | Domain controller |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### One-Click Automated Domain Penetration

```bash
python3 deathstar.py -u lowpriv -p pass -d corp.local
# Empire ecosystem, automatic BloodHound + automatic privilege escalation
```

## Notes

An automated AD attack framework that integrates with Empire.
