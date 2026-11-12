---
name: corscanner-cors-misconfig
description: "CORScanner: Scans for CORS cross-origin hijacking. Signals: web vulnerability, injection, CORS configuration scanning, batch, threads."
zh-signals: "CORScanner: CORS 跨域劫持。信号:web漏洞,注入,CORS 配置扫描,批量,线程。"
when-to-use: >-
  Use during web vulnerability scanning when you need to detect CORS
  misconfigurations such as arbitrary origin reflection that enable cross-origin
  data theft.
---

# CORScanner

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/chenjj/CORScanner
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/chenjj/CORScanner && cd CORScanner && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python cors_scan.py -u https://t.com` | CORS configuration scanning |
| `-i urls.txt` | Batch |
| `-t 100` | Threads |
| `-o out.json` | JSON output |
| `-d example.com` | Custom Origin test |

## Attack Scenario Playbook

### CORS Cross-Origin Hijacking

```bash
python cors_scan.py -i subs.txt -t 100
# hit when ACAO reflects an arbitrary origin and ACAC=true → steal token
```

## Notes

Detects CORS misconfigurations (arbitrary origin reflection / null origin / prefix matching) and outputs a list of exploitable origins.
