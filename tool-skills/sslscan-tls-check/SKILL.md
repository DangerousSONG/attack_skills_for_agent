---
name: sslscan-tls-check
description: "sslscan audits weak TLS configurations. Signals: cryptographic attack, cryptographic cracking, TLS configuration audit, certificate details, skip cipher enumeration"
zh-signals: "sslscan: TLS 弱配置审计。信号:密码学攻击,加密破解,TLS 配置审计,证书详情,跳过套件枚举。"
when-to-use: "Use sslscan when auditing a server's TLS/SSL configuration to identify weak cipher suites, outdated protocol versions, and certificate issues."
---

# sslscan

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/rbsec/sslscan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install sslscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sslscan t.com:443` | TLS configuration audit |
| `--show-certificate` | Certificate details |
| `--no-ciphersuites` | Skip cipher suite enumeration |
| `--xml=out.xml` | XML output |

## Attack Scenario Playbook

### TLS Weak Configuration Audit

```bash
sslscan --show-certificate t.com:443
# Weak cipher suites / protocol versions / certificate issues
```

## Notes

TLS/SSL configuration audit that identifies weak cipher suites and outdated protocols.
