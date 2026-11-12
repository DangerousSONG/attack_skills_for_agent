---
name: striptls-downgrade
description: "striptls performs STARTTLS downgrade attacks. Signals: MITM, mitm, IMAP downgrade, transparent mode"
zh-signals: "striptls: STARTTLS 降级攻击。信号:中间人,mitm,IMAP 降级,透明模式。"
when-to-use: "Use when attacking mail protocols to downgrade STARTTLS and capture credentials in plaintext."
---

# striptls

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/tintinweb/striptls
- Upstream License: CC0-1.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install striptls
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `striptls --server 0.0.0.0:25` | SMTP STARTTLS downgrade |
| `--server 0.0.0.0:143` | IMAP downgrade |
| `-f` | Transparent mode |

## Attack Scenario Playbook

### STARTTLS downgrade attack

```bash
striptls --server 0.0.0.0:25
# Mail protocol downgrade sniffing
```

## Notes

A STARTTLS downgrade framework by tintinweb.
