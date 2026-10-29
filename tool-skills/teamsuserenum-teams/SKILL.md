---
name: teamsuserenum-teams
description: "TeamsUserEnum enumerates valid Teams users. Signals: email collection, employee information, Teams user enumeration, threads"
zh-signals: "TeamsUserEnum: Teams 用户有效性枚举。信号:邮箱收集,员工信息,Teams 用户枚举,线程。"
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
