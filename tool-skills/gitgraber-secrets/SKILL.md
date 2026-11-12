---
name: gitgraber-secrets
description: "gitGraber monitors GitHub for secrets in real time. Signals: attack surface, cloud assets, GitHub real-time monitoring, depth, threads."
zh-signals: "gitGraber: Github 密钥实时监控。信号:攻击面,云资产,Github 实时监控,深度,线程。"
when-to-use: "Use when monitoring GitHub for exposed secrets tied to a target domain or keyword, such as cloud keys and passwords in new commits. Requires a keyword and optionally depth and thread settings."
---

# gitGraber

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/hisxo/gitGraber
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hisxo/gitGraber && cd gitGraber && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 gitGraber.py -k 'corp.com'` | GitHub real-time monitoring |
| `-k keyword -d` | Depth |
| `-t 100` | Threads |
| `-o out/` | Output |

## Attack Scenario Playbook

### GitHub Secret Real-Time Monitoring

```bash
python3 gitGraber.py -k 'corp.com internal'
# Immediate alerting on AWS keys/passwords in new commits
```

## Notes

A GitHub secret leak monitoring tool.
