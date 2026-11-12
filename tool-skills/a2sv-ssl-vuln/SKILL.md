---
name: a2sv-ssl-vuln
description: "a2sv: detects SSL/TLS CVEs. Signals: cryptographic attack, encryption cracking, SSL vulnerability scan"
zh-signals: "a2sv: SSL/TLS CVE 检测。信号:密码学攻击,加密破解,SSL 漏洞扫描。"
when-to-use: "Use when you need to scan a host for SSL/TLS vulnerabilities such as Heartbleed, CCS, and POODLE; specify a target and optional port."
---

# a2sv

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/hahwul/a2sv
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hahwul/a2sv && cd a2sv && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python a2sv.py -t t.com` | SSL vulnerability scan |
| `-t ip -p 443` | Port |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### SSL/TLS CVE Detection

```bash
python a2sv.py -t t.com
# 17 CVEs including Heartbleed/CCS/POODLE
```

## Notes

An SSL vulnerability scanner covering classic CVEs such as Heartbleed.
