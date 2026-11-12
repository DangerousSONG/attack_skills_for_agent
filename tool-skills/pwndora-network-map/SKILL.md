---
name: pwndora-network-map
description: "pwndora: Maps enterprise network asset graph. Signals: network topology, internet mapping, large-scale network mapping."
zh-signals: "pwndora: 企业网段资产图谱。信号:网络拓扑,互联网测绘,大规模网络测绘。"
when-to-use: >-
  Use when mapping a large enterprise CIDR range to build an asset graph with
  ports, banners, fingerprints and web titles, and structured JSON output is needed.
---

# pwndora

- Attack Category: C04 Network Topology and Internet Mapping
- Upstream Repository: https://github.com/alechilczenko/pwndora
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/alechilczenko/pwndora && cd pwndora
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 main.py -t 10.0.0.0/16` | Large-scale network mapping |
| `-t cidr -o out.json` | Output |
| `-p top1000` | Ports |
| `-v` | Verbose |

## Attack Scenario Playbook

### Enterprise network asset graph

```bash
python3 main.py -t 10.0.0.0/16
# Ports + banners + fingerprinting + web titles
```

## Notes

Large-scale network asset mapping with structured JSON output.
