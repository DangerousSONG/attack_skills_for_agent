---
name: lfisuite-lfi
description: "LFISuite automates LFI exploitation. Signals: web vulnerability, injection, interactive menu, target URL."
zh-signals: "LFISuite: 全自动 LFI 打点。信号:web漏洞,注入,交互菜单,目标 URL。"
when-to-use: "Use when testing a web application for local file inclusion and you need an automated workflow covering filter, log poisoning, session, and phpinfo bypasses toward an interactive shell. Requires an interactive terminal and a target URL with a suspected LFI parameter."
---

# LFISuite

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/D35m0nd142/LFISuite
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/D35m0nd142/LFISuite && cd LFISuite
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python lfisuite.py` | Interactive menu |
| `choose [1] automated LFI scan` | Target URL |
| `Log poison module` | Log poisoning to get a shell |
| `phpinfo module` | Drop a file via phpinfo |

## Attack Scenario Playbook

### Fully automated LFI exploitation

```bash
python lfisuite.py
# Enter the target → automatically walks through bypass techniques (filter/log/session/phpinfo) → interactive shell
```

## Notes

Integrates all manual LFI techniques; both the log poisoning chain and the phpinfo plus temp file chain are built in.
