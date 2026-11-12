---
name: rbndr-dns-rebinding
description: "rbndr: Bypasses browser same-origin policy. Signals: man-in-the-middle, MITM, DNS rebinding, A records, TTL control."
zh-signals: "rbndr: 浏览器同源策略绕过。信号:中间人,mitm,DNS 重绑定,A 记录,TTL 控制。"
when-to-use: "Use to bypass the browser same-origin policy by performing DNS rebinding attacks against internal services."
---

# rbndr

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/taviso/rbndr
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/taviso/rbndr && cd rbndr && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./rbndr 10.0.0.5 target.com` | DNS rebinding |
| `-a` | A record |
| `-t TTL` | TTL control |

## Attack Scenario Playbook

### Browser same-origin policy bypass

```bash
./rbndr 127.0.0.1 internal.corp.local
# Attack the internal network to bypass the same-origin policy
```

## Notes

DNS rebinding tool from taviso.
