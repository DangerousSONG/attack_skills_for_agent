---
name: ad-ldap-enum-ldap
description: 渗透工具 skill:ad-ldap-enum 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 ad-ldap-enum 时使用。
when-to-use: 渗透工具 skill:ad-ldap-enum 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 ad-ldap-enum 时使用。
---

# ad-ldap-enum

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/CroweCybersecurity/ad-ldap-enum
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/CroweCybersecurity/ad-ldap-enum && cd ad-ldap-enum
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 ad-ldap-enum.py -l ldap://10.0.0.1 -u svc@corp.local -p pass -m` | LDAP 全枚举 |
| `-l url -u u -p p -d` | 详情 |
| `-o out/` | 输出 |

## 攻击场景 Playbook

### Crowe 出品 LDAP 枚举

```bash
python3 ad-ldap-enum.py -l ldap://dc01 -u svc@corp.local -p pass
# 用户/组/计算机/OU/GPO 导出
```

## 注意事项

CroweCyber 出品,简单直接的 LDAP 枚举。
