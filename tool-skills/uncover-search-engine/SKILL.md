---
name: uncover-search-engine
description: "uncover: Multi-engine asset aggregation search. Signals: network topology, internet mapping, single query, batch query, specified engines."
zh-signals: "uncover: 多引擎资产聚合搜索。信号:网络拓扑,互联网测绘,单查询,批量查询,指定引擎。"
when-to-use: >-
  Use when you need aggregated asset search across multiple engines with a
  single or batch query and you want to specify which engines are used.
---

# uncover

- Attack Category: C04 Network Topology and Internet Mapping
- Upstream Repository: https://github.com/projectdiscovery/uncover
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/uncover/cmd/uncover@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-q 'search query'` | Single query |
| `-q query.txt` | Batch query |
| `-e shodan,censys,fofa,quake,zoomeye` | Specify engines |
| `-ue` | User engine ~/.config/uncover/provider-config.yaml |
| `-o out.txt` | Output |
| `-l 100` | Result limit |

## Attack Scenario Playbook

### Multi-Engine Asset Aggregation Search

```bash
uncover -q 'org:"Target Corp" http.title:"login"' -e shodan,censys -l 200
fofa syntax: uncover -q 'domain="corp.com"' -e fofa -l 500
```

## Notes

A ProjectDiscovery ecosystem aggregator: one CLI for Shodan/Censys/Fofa/Quake/ZoomEye/Hunter; configure API keys in provider-config.yaml.
