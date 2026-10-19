---
name: teamsuserenum-teams
description: 渗透工具 skill:TeamsUserEnum 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 TeamsUserEnum 时使用。
---

# TeamsUserEnum

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/immense-mountain/TeamsUserEnum
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/immense-mountain/TeamsUserEnum && cd TeamsUserEnum && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 teamsuserenum.py -u users.txt -d corp.com` | Teams 用户枚举 |
| `-u u.txt -d d -t 10` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### Teams 用户有效性枚举

```bash
python3 teamsuserenum.py -u names.txt -d corp.com
# 错误码判断用户存在,不出日志
```

## 注意事项

Microsoft Teams 用户枚举,域内人员发现。
