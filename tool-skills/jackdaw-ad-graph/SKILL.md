---
name: jackdaw-ad-graph
description: "jackdaw visualizes domain penetration paths. Signals: AD attack, domain pentest, SMB session and share enumeration, web UI graph, ACL path analysis."
zh-signals: "jackdaw: 可视化域渗透路径。信号:ad攻击,域渗透,SMB 会话/共享枚举,启动 Web 界面看图谱,ACL 路径分析。"
when-to-use: >-
  Use when performing Active Directory penetration testing and you need to collect
  LDAP/SMB data, build a graph, and compute shortest attack paths to Domain Admin.
---

# jackdaw

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/skelsec/jackdaw
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/skelsec/jackdaw && cd jackdaw && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `jackdaw enum ldap -d corp.local -u svc -p pass -k` | AD enumeration into SQLite |
| `jackdaw enum smb -w -d corp.local -u svc -p pass 10.0.0.0/24` | SMB session/share enumeration |
| `jackdaw nest` | Launch the web UI to view the graph |
| `jackdaw analyze -m all` | ACL path analysis |

## Attack Scenario Playbook

### Visualizing domain penetration paths

```bash
jackdaw enum ldap -d corp.local -u svc -p pass -k
jackdaw enum smb -w -d corp.local -u svc -p pass 10.0.0.0/24
jackdaw nest  # View the shortest path to DA in the browser
```

## Notes

By skelsec; after collecting AD and SMB data it computes the shortest attack path to Domain Admin with a graph algorithm (Dijkstra supported).