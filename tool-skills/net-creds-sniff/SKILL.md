---
name: net-creds-sniff
description: "net-creds: Passive internal network credential harvesting. Signals: man-in-the-middle, MITM, passive credential sniffing, filter local host, PCAP analysis."
zh-signals: "net-creds: 内网凭据被动收割。信号:中间人,mitm,被动凭据嗅探,过滤本机,PCAP 分析。"
when-to-use: >-
  Use when passively sniffing a network segment for credentials across HTTP,
  FTP, POP, SNMP, and similar protocols, or analyzing an existing PCAP.
  Supports filtering local traffic.
---

# net-creds

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/DanMcInerney/net-creds
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/DanMcInerney/net-creds && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python net-creds.py -i eth0` | Passive credential sniffing |
| `-i eth0 -f` | Filter local host |
| `-p` | PCAP analysis |

## Attack Scenario Playbook

### Passive internal network credential harvesting

```bash
python net-creds.py -i eth0
# Captures credentials across HTTP/FTP/POP/SNMP
```

## Notes

Passive credential sniffing with broad protocol coverage.
