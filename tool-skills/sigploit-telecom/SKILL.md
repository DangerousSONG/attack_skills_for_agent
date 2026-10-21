---
name: sigploit-telecom
description: 渗透工具 skill:SigPloit 的安装、参数速查与攻击场景 playbook。当任务涉及 边界设备与VPN攻击 需要调用 SigPloit 时使用。
when-to-use: 渗透工具 skill:SigPloit 的安装、参数速查与攻击场景 playbook。当任务涉及 边界设备与VPN攻击 需要调用 SigPloit 时使用。
---

# SigPloit

- 攻击大类:C11 边界设备与VPN攻击
- 上游仓库:https://github.com/SigPloiter/SigPloit
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/SigPloiter/SigPloit
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python sigploit.py` | 电信信令攻击框架 |
| `use ss7/location_tracking` | 模块 |
| `set target +1234` | 目标 |

## 攻击场景 Playbook

### SS7/Diameter 攻击

```bash
python sigploit.py && use ss7/intercept_sms
# 运营商信令
```

## 注意事项

电信协议攻击框架。
