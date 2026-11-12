---
name: pcredz-smb-creds
description: "SMB/HTTP credential sniffing. Signals: MITM, mitm, traffic credential extraction, PCAP analysis, detailed."
zh-signals: "PCredz: SMB/HTTP 凭据嗅探。信号:中间人,mitm,流量凭据提取,PCAP 分析,详细。"
when-to-use: >-
  Use when extracting credentials from live traffic or PCAP files, including
  NTLM hashes, HTTP Basic credentials, and Kerberos data; capture on an
  interface or analyze an existing capture.
---

# PCredz

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/lgandx/PCredz
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/lgandx/PCredz && cd PCredz
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3Pcredz -i eth0` | Traffic credential extraction |
| `-f capture.pcap` | PCAP analysis |
| `-v` | Verbose |

## Attack Scenario Playbook

### SMB/HTTP Credential Sniffing

```bash
python3 Pcredz -i eth0
# Catches NTLM hashes / HTTP Basic / Kerberos alike
```

## Notes

By lgandx (the author of Responder), traffic credential extraction.
