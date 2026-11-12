---
name: maryam-osint-framework
description: "Maryam: Modular OSINT investigation. Signals: email collection, employee information, OSINT framework CLI, module selection, data sources."
zh-signals: "Maryam: 模块化 OSINT 调查。信号:邮箱收集,员工信息,OSINT 框架 CLI,模块选择,数据源。"
when-to-use: >-
  Use when conducting modular OSINT investigations across domain, email, and
  personnel data; select a module, set the query and data sources, then run it
  from the CLI.
---

# Maryam

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/saeeddhqan/Maryam
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/saeeddhqan/Maryam && cd Maryam && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `maryam` | OSINT framework CLI |
| `use osint/dns_search` | Module selection |
| `set SOURCE google,bing` | Data sources |
| `set QUERY corp.com` | Query |
| `run` | Execute |

## Attack Scenario Playbook

### Modular OSINT investigation

```bash
maryam && use osint/domain_search && set QUERY corp.com && run
# By OWASP, covering metadata, leaks and personnel comprehensively
```

## Notes

OWASP open source intelligence framework, an OSINT investigation tool with 200+ modules.
