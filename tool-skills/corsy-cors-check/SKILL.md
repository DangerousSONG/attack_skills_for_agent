---
name: corsy-cors-check
description: "Corsy: Quickly checks CORS configurations. Signals: web vulnerability, injection, CORS scanning, batch, delay."
zh-signals: "Corsy: CORS 配置快速体检。信号:web漏洞,注入,CORS 扫描,批量,延迟。"
when-to-use: >-
  Use when quickly assessing CORS misconfigurations across one or many authorized web hosts
  and prioritizing findings by risk level.
---

# Corsy

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/s0md3v/Corsy
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/s0md3v/Corsy && cd Corsy && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 corsy.py -u https://t.com` | CORS scanning |
| `-i urls.txt` | Batch |
| `-d 2` | Delay |
| `-v` | Verbose |

## Attack Scenario Playbook

### Quick CORS Configuration Health Check

```bash
python3 corsy.py -i alive_hosts.txt
# detects 12 CORS attack surface issues and outputs a risk rating
```

## Notes

A lightweight CORS scanner by s0md3v; detects 12 CORS configuration problems and is faster than its peers.
