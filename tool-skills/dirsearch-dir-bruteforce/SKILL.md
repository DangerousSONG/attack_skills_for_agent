---
name: dirsearch-dir-bruteforce
description: "dirsearch: backend and backup file discovery. Signals: web scanning, vulnerability scanning, extension-based directory enumeration, custom dictionary, recursive scan 3 levels."
zh-signals: "dirsearch: 后台与备份文件发现。信号:web扫描,漏洞扫描,扩展名枚举目录,自定义字典,递归扫描 3 层。"
when-to-use: >-
  Use during web reconnaissance when you need to brute-force directories and
  files, especially to discover admin panels, backups, and .git or .env leaks.
---

# dirsearch

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/maurosoria/dirsearch
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install dirsearch or git clone https://github.com/maurosoria/dirsearch
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-u URL -e php,html,bak` | Extension-based directory enumeration |
| `-w /path/wordlist.txt` | Custom wordlist |
| `-r -R 3` | Recursive scan 3 levels deep |
| `--exclude-status=403,404` | Filter out invalid status codes |
| `-t 50` | 50 threads |
| `-x 302` | Exclude redirects |
| `--proxy=http://127.0.0.1:8080` | Route through Burp for debugging |

## Attack Scenario Playbook

### Backend and backup file discovery

```bash
dirsearch -u https://target.com -e php,bak,old,zip -t 80 --exclude-status=404
dirsearch -u https://target.com/admin/ -r -R 2
```

## Notes

The default wordlist lives in the db/ directory; hitting .git/.env/.bak is a common breakthrough.
