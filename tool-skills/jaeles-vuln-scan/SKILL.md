---
name: jaeles-vuln-scan
description: "jaeles verifies vulnerabilities with signatures. Signals: web vulnerability, injection, built-in signature scan, signature family selection, custom signatures."
zh-signals: "jaeles: 签名驱动漏洞验证。信号:web漏洞,注入,内置签名扫描,指定签名族,自定义签名。"
when-to-use: >-
  Use when verifying suspected web vulnerabilities with signature-based checks,
  optionally scoping to specific signature families, custom signatures, or
  routing through Burp.
---

# jaeles

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/jaeles-project/jaeles
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/jaeles-project/jaeles@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `jaeles scan -u https://t.com` | Built-in signature scan |
| `-x 'sqli,xxe'` | Specify signature families |
| `jaeles config add -R ~/custom-signatures` | Custom signatures |
| `-o out/` | Output |
| `--proxy http://127.0.0.1:8080` | Route through Burp |

## Attack Scenario Playbook

### Signature-Driven Vulnerability Validation

```bash
jaeles scan -u https://t.com -x rce
# YAML signatures with OOB correlation, offering more flexible result determination than nuclei
```

## Notes

Signature-based vulnerability scanning framework; YAML signatures support multi-request chains and OOB correlation validation, in the same ecosystem as gospider.
