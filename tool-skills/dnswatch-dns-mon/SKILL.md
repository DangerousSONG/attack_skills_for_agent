---
name: dnswatch-dns-mon
description: "DNSWatch: DNS request monitoring and hijacking. Signals: man-in-the-middle, MITM, DNS monitoring plus spoofing, spoofing modes, targeted."
zh-signals: "DNSWatch: DNS 请求监控+劫持。信号:中间人,mitm,DNS 监控+伪造,伪造模式,定向。"
when-to-use: "Use on a LAN to monitor DNS requests and spoof responses for phishing redirection or traffic analysis."
---

# DNSWatch

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/HalilDeniz/DNSWatch
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/HalilDeniz/DNSWatch && cd DNSWatch && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 dnswatch.py -i eth0` | DNS monitoring and spoofing |
| `-i eth0 -f` | Spoofing mode |
| `-i eth0 -d example.com/10.0.0.5` | Targeted |

## Attack Scenario Playbook

### DNS request monitoring and hijacking

```bash
python3 dnswatch.py -i eth0
# Internal DNS analysis and phishing redirection
```

## Notes

All-in-one DNS monitoring and spoofing.
