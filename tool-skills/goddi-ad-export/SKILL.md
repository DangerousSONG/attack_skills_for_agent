---
name: goddi-ad-export
description: "goddi exports full Active Directory structure for offline analysis. Signals: AD attack, domain penetration, JSON."
zh-signals: "goddi: AD 结构全量导出(离线分析)。信号:ad攻击,域渗透,json`。"
when-to-use: >-
  Use to dump the full Active Directory structure (users, groups, computers,
  GPOs) to CSV or JSON for offline attack-path analysis.
---

# goddi

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/NetSPI/goddi
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/NetSPI/goddi@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `goddi -username svc@corp.local -password pass -domain corp.local -dc 10.0.0.1 -unsafe` | Export the full AD structure (users/groups/computers/GPOs) |
| `-format csv|json` | Output format |

## Attack Scenario Playbook

### Full AD Structure Export (Offline Analysis)

```bash
goddi -u svc@corp.local -p pass -domain corp.local -dc 10.0.0.1 -unsafe
# Take the CSV and map privilege relationships offline to pick an escalation path
```

## Notes

By NetSPI, a one-click full export of AD information (users/groups/computers/trusts/GPOs/OU) to CSV, ideal for building an attack path graph offline.
