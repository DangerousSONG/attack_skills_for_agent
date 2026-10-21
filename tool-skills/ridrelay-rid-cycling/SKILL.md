---
name: ridrelay-rid-cycling
description: 渗透工具 skill:ridrelay 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 ridrelay 时使用。
when-to-use: 渗透工具 skill:ridrelay 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 ridrelay 时使用。
---

# ridrelay

- 攻击大类:C29 AD与LDAP枚举
- 上游仓库:https://github.com/skorov/ridrelay
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/skorov/ridrelay && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python ridrelay.py -t 10.0.0.5` | RID 循环枚举域用户 |
| `-t 10.0.0.5 -r 1000-2000` | 指定 RID 范围 |
| `--sam` | 尝试 SAM 枚举 |
| `-o users.txt` | 输出 |

## 攻击场景 Playbook

### 匿名/空会话用户枚举

```bash
python ridrelay.py -t 10.0.0.5
# 利用空会话拿域用户清单,配合 asreproast
```

## 注意事项

利用 SMB 空会话做 RID cycling,无凭据枚举域用户(旧 trick 自动化)。
