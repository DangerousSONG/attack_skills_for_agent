---
name: stews-websocket-scan
description: "STEWS discovers WebSocket endpoints. Signals: web vulnerability, injection, vulnerability detection"
zh-signals: "STEWS: WebSocket 端点发现。信号:web漏洞,注入,漏洞检测。"
when-to-use: "Use STEWS when you need to discover hidden WebSocket endpoints or test a WebSocket service for weak authentication and vulnerabilities."
---

# STEWS

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/PalindromeLabs/STEWS
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/PalindromeLabs/STEWS && cd STEWS
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 stews.py -u wss://t.com/ws` | WebSocket security scan |
| `-u url -m discovery` | Endpoint discovery |
| `-u url -m vuln` | Vulnerability detection |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### WebSocket endpoint discovery

```bash
python3 stews.py -u wss://api.t.com -m discovery
# Discover hidden ws endpoints and weak authentication
```

## Notes

Dedicated WebSocket scanning framework by Palindrome Labs.
