---
name: postenum-linux-audit
description: "Quick Linux foothold assessment. Signals: red team, methodology, basic system info, container/virtualization detection, network info."
zh-signals: "postenum: Linux 立足点快速摸底。信号:红队,方法论,基础系统信息,容器/虚拟化检测,网络信息。"
when-to-use: >-
  Use on a freshly gained Linux foothold to quickly enumerate system, container,
  and network details and locate privilege-escalation paths.
---

# postenum

- Attack Category: C50 Trace Cleanup and Anti-Forensics
- Upstream Repository: https://github.com/mbahadou/postenum
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/mbahadou/postenum
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `bash postenum.sh -s` | Basic system information |
| `bash postenum.sh -c` | Container/virtualization detection |
| `bash postenum.sh -n` | Network information |
| `bash postenum.sh -a` | Full run |

## Attack Scenario Playbook

### Quick Linux Foothold Assessment

```bash
bash postenum.sh -a | tee enum.txt
# Kernel version / SUID / cron / docker / cloud metadata all in one pass, to find privilege escalation paths
```

## Notes

Linux privilege escalation enumeration script, with output categorized by MITRE ATT&CK, lighter than LinPEAS.
