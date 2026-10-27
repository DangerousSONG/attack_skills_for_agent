---
name: sigploit-telecom
description: SigPloit: SS7/Diameter 攻击。信号:vpn漏洞,防火墙,电信信令攻击框架,模块。
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
