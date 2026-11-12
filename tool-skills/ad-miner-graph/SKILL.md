---
name: ad-miner-graph
description: "AD Miner: visualizes BloodHound data and rates risk. Signals: ad attack, domain pentest, control path graph generation, control path depth, direct DC collection"
zh-signals: "AD Miner: BH 数据可视化风险评级。信号:ad攻击,域渗透,生成控制路径图,控制路径层数,直接连域控采集。"
when-to-use: >-
  Use after collecting BloodHound data in an Active Directory assessment to
  visualize attack paths, rate risk, and compute control paths to Domain Admin.
---

# AD Miner

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/Mazars-Tech/AD_Miner
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install ad-miner
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `AD-miner -b mycontext -u neo4j -p pass` | Generate a risk graph from BloodHound data |
| `-c -cf mycontext` | Generate the control path graph |
| `-l 3` | Control path depth |
| `-d 10.0.0.1` | Collect directly from the domain controller |

## Attack Scenario Playbook

### BH Data Visualization and Risk Rating

```bash
bloodhound-python -u svc -p pass -d corp.local -c All
AD-miner -b context -u neo4j -p pass
# Obtain a risk score graph that shows the tier0 asset exposure surface
```

## Notes

By Mazars, consumes a BloodHound database to produce a graphical risk rating report for Active Directory.
