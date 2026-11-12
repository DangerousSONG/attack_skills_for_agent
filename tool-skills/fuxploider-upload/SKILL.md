---
name: fuxploider-upload
description: "Fuxploider tests upload functionality bypass matrices. Signals: web vulnerabilities, injection, upload vulnerability detection, target scripting language, extension probing."
zh-signals: "Fuxploider: 上传功能绕过矩阵。信号:web漏洞,注入,上传漏洞检测,目标脚本语言,扩展名探测。"
when-to-use: >-
  Use when a web application exposes a file-upload feature and you want to automatically test
  extension, MIME, and content bypass matrices.
---

# Fuxploider

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/almandin/fuxploider
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/almandin/fuxploider && cd fuxploider && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python fuxploider.py --url https://t.com/upload --not-regex 'wrong'` | Upload vulnerability detection |
| `--scripts extension` | Target scripting language |
| `--detect-extensions` | Extension probing |
| `--true-regex 'success'` | Success fingerprint |
| `-t 10` | Threads |

## Attack Scenario Playbook

### Upload functionality bypass matrix

```bash
python fuxploider.py --url http://target/upload --not-regex 'error' --detect-extensions
# Automatically tests extension bypasses (phtml/.htaccess/case/double extension) plus MIME confusion
```

## Notes

Fully automated upload testing: dozens of techniques are rotated across the extension, MIME and content check layers.
