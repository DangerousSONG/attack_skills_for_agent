---
name: activedirectoryenum-ad
description: 渗透工具 skill:ActiveDirectoryEnum 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 ActiveDirectoryEnum 时使用。
when-to-use: 渗透工具 skill:ActiveDirectoryEnum 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 ActiveDirectoryEnum 时使用。
---

# ActiveDirectoryEnum

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/CasperGN/ActiveDirectoryEnum
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install activedirectoryenum
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `active-directory-enum -u svc -p pass -d corp.local -dc 10.0.0.1` | AD 枚举+攻击面 |
| `-u u -p p -d d -dc ip -s` | BloodHound |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### AD 枚举+攻击面分析

```bash
active-directory-enum -u svc -p pass -d corp.local
# 枚举+漏洞路径+输出报告
```

## 注意事项

AD 枚举+攻击路径分析一体。
