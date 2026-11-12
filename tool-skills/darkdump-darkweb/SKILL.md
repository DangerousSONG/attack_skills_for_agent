---
name: darkdump-darkweb
description: "darkdump: Searches dark web intelligence. Signals: web vulnerability, injection, dark web search, page count."
zh-signals: "darkdump: 暗网情报搜索。信号:web漏洞,注入,暗网搜索,页数。"
when-to-use: "Use darkdump when searching dark web forums and markets for mentions of a target organization, brand, or leaked data as part of threat intelligence and OSINT."
---

# darkdump

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/josh0xA/darkdump
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/josh0xA/darkdump && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 darkdump.py -q 'target corp'` | Dark web search |
| `-q keywords -p 3` | Page count |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Dark Web Intelligence Search

```bash
python3 darkdump.py -q 'corp.com'
# Leaked leads mentioning the target on dark web forums and markets
```

## Notes

A wrapper around dark web (.onion) search engine interfaces for looking up leaked target data and threat intelligence.
