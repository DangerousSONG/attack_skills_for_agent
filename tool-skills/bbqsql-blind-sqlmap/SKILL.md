---
name: bbqsql-blind-sqlmap
description: "BBQSQL: manually configures semi-blind injection. Signals: web vulnerability, injection, run blind injection after configuration, export results"
zh-signals: "BBQSQL: 半盲注手工配置。信号:web漏洞,注入,配置完成后执行盲注,导出结果。"
when-to-use: >-
  Use when sqlmap cannot handle a custom blind injection, such as comparison or
  similarity logic, and you need to manually configure the injection point and technique.
---

# BBQSQL

- Attack Category: C09 Web Exploitation (SQL Injection)
- Upstream Repository: https://github.com/neohapsis/bbqsql
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install bbqsql
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `bbqsql` | Enter interactive configuration: URL/method/injection point/comparison request |
| `run` | Run the blind injection once configuration is complete |
| `export results.csv` | Export results |

## Attack Scenario Playbook

### Manual Configuration for Semi-Blind Injection

```bash
bbqsql
# set url=https://t.com/report?id=1; injection point select id; technique=comparison; run
```

## Notes

A SQL blind injection framework suited to custom comparison logic that sqlmap cannot crack (such as comparing the similarity of two responses), driven by an interactive configuration menu.
