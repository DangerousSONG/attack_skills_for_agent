---
name: lorsrf-ssrf-hunt
description: "lorsrf: Batch SSRF probing. Signals: web vulnerability, injection, SSRF parameter testing, OOB receiver, batch URLs."
zh-signals: "lorsrf: SSRF 批量探测。信号:web漏洞,注入,SSRF 参数测试,OOB 接收,批量 URL。"
when-to-use: >-
  Use when testing parameters for server-side request forgery in batch; supply
  URLs or a wordlist and an out-of-band receiver to confirm callbacks.
---

# lorsrf

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/knassar702/lorsrf
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/knassar702/lorsrf && cd lorsrf
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./lorsrf -u 'https://t.com/?u=x' -p u` | SSRF parameter testing |
| `-u url -b http://burp.collab` | OOB receiver |
| `-w wordlist.txt` | Batch URLs |

## Attack Scenario Playbook

### Batch SSRF probing

```bash
./lorsrf -u urls.txt -b http://vps.interactsh.com
# Inject callback payloads into every parameter
```

## Notes

SSRF probing tool with OOB callback verification.
