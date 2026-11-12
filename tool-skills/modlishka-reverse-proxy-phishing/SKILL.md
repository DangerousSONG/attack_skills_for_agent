---
name: modlishka-reverse-proxy-phishing
description: "Modlishka: Real-time 2FA session phishing. Signals: phishing, social engineering, launch reverse proxy phishing, attach legitimate domain TLS certificate, custom credential extraction regex."
zh-signals: "Modlishka: 2FA 会话实时钓鱼。信号:钓鱼,社会工程,启动反向代理钓鱼,挂合法域名 TLS 证书,自定义凭证提取正则。"
when-to-use: >-
  Use when running an authorized phishing simulation that must capture live
  sessions to bypass TOTP/2FA via a reverse proxy; requires a controlled proxy
  domain and a matching TLS certificate/key.
---

# Modlishka

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/drk1wi/Modlishka
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/drk1wi/Modlishka@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `Modlishka -config phish.json` | Launch reverse proxy phishing |
| `cert configuration` | Attach a legitimate domain TLS certificate |
| `cred capture plugin` | Custom credential extraction regex |

## Attack Scenario Playbook

### Real-time 2FA session phishing

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
# phish.json: proxyDomain=login.target.com; target=accounts.target.com; cert/key point to the files above
Modlishka -config phish.json
```

## Notes

Reverse-proxy phishing can bypass TOTP in real time (session hijacking rather than credential reuse); always hold authorization for the target domain and a legitimate use case.
