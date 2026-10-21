---
name: maryam-osint-framework
description: 渗透工具 skill:Maryam 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 Maryam 时使用。
when-to-use: 渗透工具 skill:Maryam 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 Maryam 时使用。
---

# Maryam

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/saeeddhqan/Maryam
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/saeeddhqan/Maryam && cd Maryam && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `maryam` | OSINT 框架 CLI |
| `use osint/dns_search` | 模块选择 |
| `set SOURCE google,bing` | 数据源 |
| `set QUERY corp.com` | 查询 |
| `run` | 执行 |

## 攻击场景 Playbook

### 模块化 OSINT 调查

```bash
maryam && use osint/domain_search && set QUERY corp.com && run
# OWASP 出品,元数据/泄漏/人员全覆盖
```

## 注意事项

OWASP 开源情报框架,200+ 模块的 OSINT 调查工具。
