---
name: sprayhound-ad-spray
description: "sprayhound sends spray results directly to attack paths. Signals: brute force, password spraying, spray+BH integration, threads"
zh-signals: "sprayhound: 喷洒结果直通攻击路径。信号:暴力破解,口令喷射,喷洒+BH 联动,线程。"
when-to-use: "Use sprayhound when spraying passwords against Active Directory and you want successful credentials automatically correlated with BloodHound attack paths."
---

# sprayhound

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/Hackndo/sprayhound
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Hackndo/sprayhound && cd sprayhound && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sprayhound -d corp.local -u users.txt -p passwords.txt` | Spraying + BloodHound integration |
| `-d d -u u.txt -p p.txt -b` | BloodHound integration |
| `-t 5` | Threads |

## Attack Scenario Playbook

### Spray Results Feed Directly into Attack Paths

```bash
sprayhound -d corp.local -u users.txt -p pass.txt -b
# Automatically query the shortest BH path on a hit
```

## Notes

By Hackndo, password spraying plus BloodHound integration that yields attack paths on every hit.
