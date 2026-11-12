---
name: injectus-crlf-openredirect
description: "Injectus probes combined open redirect and CRLF issues. Signals: web vulnerability, injection, batch, CRLF only, open redirect only."
zh-signals: "Injectus: 开放重定向+CRLF 组合探测。信号:web漏洞,注入,批量,仅 CRLF,仅开放重定向。"
when-to-use: "Use when probing URL parameters for open redirect and CRLF injection during bug bounty or web assessment, including batch runs. Requires target URLs and optionally selecting CRLF-only or redirect-only mode."
---

# Injectus

- Attack Category: C09 Web Exploitation (CRLF / Redirect)
- Upstream Repository: https://github.com/BountyStrike/Injectus
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/BountyStrike/Injectus && cd Injectus && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 injectus.py -u 'https://t.com/?redir=x'` | Scan for CRLF plus open redirect |
| `-f urls.txt` | Batch |
| `--crlf-only` | CRLF only |
| `--redirect-only` | Open redirect only |

## Attack Scenario Playbook

### Combined open redirect and CRLF probing

```bash
python3 injectus.py -u 'https://t.com/go?to=https://evil.com'
# Hit the redir parameter → phishing/token theft chain
```

## Notes

Batch scanning for CRLF injection and open redirect, well suited to a bug bounty hunter's workflow.
