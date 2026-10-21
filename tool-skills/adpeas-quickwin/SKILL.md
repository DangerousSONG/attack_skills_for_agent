---
name: adpeas-quickwin
description: 渗透工具 skill:adPEAS 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与横向移动 需要调用 adPEAS 时使用。
when-to-use: 渗透工具 skill:adPEAS 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与横向移动 需要调用 adPEAS 时使用。
---

# adPEAS

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/ajm4n/adpeas
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ajm4n/adpeas && cd adpeas
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 adPEAS.py -d corp.local -u svc -p pass -dc 10.0.0.1` | 一键 AD 提权枚举 |
| `-a` | 全模块 |
| `-m kerberoast` | 单模块(Kerberoast/AS-REP/BloodHound) |
| `-o report.txt` | 输出报告 |

## 攻击场景 Playbook

### 低权限 AD 快速摸底

```bash
python3 adPEAS.py -d corp.local -u svc -p pass -dc 10.0.0.1 -a
# Kerberoast/AS-REP/敏感组/密码策略/GPO 一把梭
```

## 注意事项

自动化 AD 权限提升枚举,类似 linPEAS 的域版,输出可直接执行的提权建议。
