---
name: tlshelpers-cert
description: "tlshelpers performs quick TLS checks. Signals: cryptographic attack, cryptographic cracking, certificate download, cipher scan, PCAP analysis"
zh-signals: "tlshelpers: TLS 快速检查。信号:密码学攻击,加密破解,证书下载,套件扫描,PCAP 分析。"
when-to-use: >-
  Use when quickly checking a host's TLS configuration, downloading its certificate
  chain, scanning cipher suites, or analyzing ciphers from a PCAP capture.
---

# tlshelpers

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/hannob/tlshelpers
- Upstream License: 0BSD (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hannob/tlshelpers
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./getcert.sh t.com` | Certificate download |
| `./cipherscan.sh t.com` | Cipher suite scan |
| `./sniffer2ciphers.py pcap` | PCAP analysis |

## Attack Scenario Playbook

### Quick TLS checks

```bash
./getcert.sh t.com > cert.pem
# Certificate chain analysis
```

## Notes

A set of TLS inspection scripts by Hanno Böck.