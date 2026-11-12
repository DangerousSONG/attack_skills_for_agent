---
name: typo3scan
description: "Typo3Scan scans TYPO3 vulnerabilities. Signals: web vulnerability, injection, SSL, batch"
zh-signals: "Typo3Scan: Typo3 漏洞扫描。信号:web漏洞,注入,SSL,批量。"
when-to-use: >-
  Use when the target appears to be TYPO3 and you need version, extension, and
  CVE detection. Supports SSL, batch domain files, and output.
---

# Typo3Scan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/whoot/Typo3Scan
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/whoot/Typo3Scan && cd Typo3Scan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 typo3scan.py -d t.com` | Typo3 enumeration + vulnerability scan |
| `-d domain -s` | SSL |
| `-o out.txt` | Output |
| `-f domains.txt` | Batch |

## Attack Scenario Playbook

### Typo3 Vulnerability Scanning

```bash
python3 typo3scan.py -d t.com
# Full extension/version/CVE detection
```

## Notes

A dedicated TYPO3 CMS scanner with an extension-level vulnerability database.
