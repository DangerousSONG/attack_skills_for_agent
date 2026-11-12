---
name: pymeta-metadata
description: "pymeta: Harvests document metadata. Signals: email collection, employee information, document metadata extraction, file type."
zh-signals: "pymeta: 文档元数据收割。信号:邮箱收集,员工信息,文档元数据提取,类型。"
when-to-use: "Use pymeta when harvesting document metadata from a target domain to extract authors, software, and internal paths for email and people OSINT."
---

# pymeta

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/m8sec/pymeta
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install pymeta3
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `pymeta -d corp.com` | Document metadata extraction |
| `-d domain -f pdf,docx` | File types |
| `-o out.txt` | Output |
| `-e 50` | Limit |

## Attack Scenario Playbook

### Document metadata harvesting

```bash
pymeta -d corp.com
# Authors, software and paths leak internal network information
```

## Notes

Search engine plus metadata extraction, a file-based OSINT tool.
