---
name: yasuo-vuln-scan
description: "yasuo: Admin panel and vulnerability dual detection. Signals: web vulnerability, injection, web app vulnerability scan, all ports, brute-force admin panel."
zh-signals: "yasuo: 后台+漏洞双探测。信号:web漏洞,注入,Web 应用漏洞扫描,全端口,爆破后台。"
when-to-use: >-
  Use when scanning one or many authorized web hosts to detect application fingerprints,
  default admin panels and known web vulnerabilities. Suitable for batch IP ranges with
  specified ports or full-port scanning.
---

# yasuo

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/0xsauby/yasuo
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0xsauby/yasuo && cd yasuo
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ruby yasuo.rb -r hosts.txt -p 80,8080` | Web application vulnerability scanning |
| `-r file -f` | All ports |
| `-b` | Brute-force admin panels |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Dual Admin Panel and Vulnerability Detection

```bash
ruby yasuo.rb -r ips.txt -p 80,443,8080
# Identify application types + default admin panels + known vulnerabilities
```

## Notes

Web application fingerprinting plus vulnerability scanning, well suited to large IP ranges in bulk.
