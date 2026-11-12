---
name: w13scan-passive-audit
description: "w13scan: Passive traffic vulnerability auditing. Signals: web vulnerabilities, injection, passive scan, proxy mode traffic capture, proxy port."
zh-signals: "w13scan: 被动流量漏洞审计。信号:web漏洞,注入,被动扫描,代理模式抓流量,代理端口。"
when-to-use: >-
  Use when performing an authorized full-site web audit and you want passive vulnerability
  analysis of every request captured through the built-in proxy.
---

# w13scan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/boy-hack/w13scan
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/boy-hack/w13scan && cd w13scan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 w13scan.py -u https://t.com` | Passive scan |
| `-u url --proxy` | Proxy mode traffic capture |
| `-p 8080` | Proxy port |
| `--level 5` | Detection level |

## Attack Scenario Playbook

### Passive traffic vulnerability audit

```bash
python3 w13scan.py -u https://t.com -p 8080
# Browse the whole site through the proxy and passively analyze every request
```

## Notes

Passive web vulnerability scanner based on traffic analysis, well suited to site-wide audits in authorized testing.
