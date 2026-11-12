---
name: beroot-privesc-check
description: "BeRoot: checks local privilege escalation on Windows and Linux. Signals: windows privilege escalation, UAC bypass, Linux privilege escalation full checks, specify modules, actionable exploitation advice"
zh-signals: "BeRoot: 双平台本地提权体检。信号:windows提权,uac绕过,Linux 提权全检测,指定模块,写可执行漏洞利用建议。"
when-to-use: >-
  Use after obtaining a local shell on Windows or Linux to check privilege escalation paths such as sudo misconfigurations, SUID, UAC bypass and weak service permissions.
---

# BeRoot

- Attack Category: C17 Windows Local Privilege Escalation
- Upstream Repository: https://github.com/AlessandroZ/BeRoot
- Upstream License: LGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/AlessandroZ/BeRoot && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python beroot.py --modules all` | Full Linux privilege escalation check |
| `Beroot.exe` | Full Windows privilege escalation check |
| `--modules sudo/suid/kernel` | Specify modules |
| `-w` | Write actionable exploitation advice |
| `-o report.txt` | Output |

## Attack Scenario Playbook

### Dual-Platform Local Privilege Escalation Health Check

```bash
python beroot.py --modules all
# Checks sudo misconfiguration/SUID/writable services/AlwaysInstallElevated/group policy and more
```

## Notes

Dual-platform local privilege escalation enumeration for Linux and Windows, modular in design, and it outputs concrete, executable exploitation commands.
