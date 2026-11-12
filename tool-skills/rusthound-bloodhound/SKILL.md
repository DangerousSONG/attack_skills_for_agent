---
name: rusthound-bloodhound
description: "RustHound: Rust implementation of SharpHound. Signals: AD attack, domain penetration, domain controller IP, Kerberos, packaged output."
zh-signals: "RustHound: Rust 版 SharpHound。信号:ad攻击,域渗透,域控 IP,Kerberos,打包输出。"
when-to-use: "Use to collect Active Directory data for BloodHound in a Rust binary, including Kerberos, ADCS, and zipped output."
---

# RustHound

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/OPFOR-Crown-Cottage/rusthound
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install rusthound or take the release binary
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `rusthound -d corp.local -u user -p pass` | BloodHound data collection |
| `-i 10.0.0.5` | Domain controller IP |
| `-k` | Kerberos |
| `--zip` | Packaged output |
| `-c All` | Collect everything |
| `--adcs` | Include ADCS data |
| `--old-bloodhound` | Compatible with legacy JSON |

## Attack Scenario Playbook

### SharpHound in Rust

```bash
rusthound -d corp.local -u svc -p pass -i 10.0.0.5 --zip --adcs
# Drop the output zip straight into BloodHound GUI/CE to analyze attack paths
```

## Notes

A single Rust binary, cross-platform and free of .NET dependencies; supports the latest BloodHound CE schema.
