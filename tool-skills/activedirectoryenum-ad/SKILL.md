---
name: activedirectoryenum-ad
description: "ActiveDirectoryEnum: performs AD enumeration and attack surface analysis. Signals: ad attack, domain pentest, BloodHound"
zh-signals: "ActiveDirectoryEnum: AD 枚举+攻击面分析。信号:ad攻击,域渗透,BloodHound。"
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
