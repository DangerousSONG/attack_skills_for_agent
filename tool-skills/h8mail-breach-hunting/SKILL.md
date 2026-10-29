---
name: h8mail-breach-hunting
description: "h8mail checks emails in breach databases and prepares bulk employee credential stuffing. Signals: email collection, employee information, JSON output."
zh-signals: "h8mail: 查邮箱是否在泄露库中出现、批量员工邮箱撞库前置。信号:邮箱收集,员工信息,JSON 输出。"
---

# h8mail

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/khast3x/h8mail
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install h8mail
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-t victim@corp.com` | 单邮箱 breach 查询 |
| `-t targets.txt` | 批量 |
| `-q 'CorpName'` | 按关键字查 breach 集合 |
| `-ch chase_keys.txt` |  chase 模式(多字段关联) |
| `-o results.json` | JSON 输出 |
| `-lb /opt/breach/` | 本地 breach 库查询 |

## 攻击场景 Playbook

### 查邮箱是否在泄露库中出现

```bash
h8mail -t ceo@corp.com -o out.json
cat out.json | jq -r '.[].breaches[]?' | sort -u
```

### 批量员工邮箱撞库前置

```bash
h8mail -t emails.txt -lb /data/breachcompilation/ -o creds.json
```

## 注意事项

查询 HaveIBeenPwned/EmoLogger 等公开源;配本地 breach 库可离线查。
