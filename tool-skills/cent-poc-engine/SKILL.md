---
name: cent-poc-engine
description: "cent: Expands nuclei templates in one click. Signals: web vulnerability, injection, keyword template filtering, specified output directory, template exclusion."
zh-signals: "cent: nuclei 模板一键扩容。信号:web漏洞,注入,按关键字筛选模板,指定输出目录,排除模板。"
when-to-use: "Use when you need to expand the nuclei template set by pulling community templates before a vulnerability scan."
---

# cent

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/xm1k3/cent
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/xm1k3/cent@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cent -p` | Pull all community nuclei templates |
| `cent -p -k 'cve-2023'` | Filter templates by keyword |
| `cent -p -o ~/nuclei-templates` | Specify output directory |
| `-e id1,id2` | Exclude templates |

## Attack Scenario Playbook

### One-Click Expansion of the nuclei Template Set

```bash
cent -p && nuclei -u https://t.com -t ~/cent-nuclei-templates
# Aggregates community templates and doubles vulnerability coverage
```

## Notes

nuclei template aggregation engine that automatically pulls templates from dozens of community repositories, a template supplementer for existing nuclei.
