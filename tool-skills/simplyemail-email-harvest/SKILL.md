---
name: simplyemail-email-harvest
description: "SimplyEmail: bulk email address harvesting. Signals: email collection, employee info, multi-source email collection, detailed, JSON output."
zh-signals: "SimplyEmail: 邮箱地址批量收割。信号:邮箱收集,员工信息,邮箱收集(多源),详细,JSON 输出。"
---

# SimplyEmail

- 攻击大类:C03 OSINT情报收集
- 上游仓库:https://github.com/killswitch-GUI/SimplyEmail
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/killswitch-GUI/SimplyEmail && cd SimplyEmail && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python SimplyEmail.py -e target.com -l` | 邮箱收集(多源) |
| `-s` | 起 HTTP 服务在线查看 |
| `-v` | 详细 |
| `--json email.json` | JSON 输出 |

## 攻击场景 Playbook

### 邮箱地址批量收割

```bash
python SimplyEmail.py -e corp.com -l
# 爬官网/公开源收集邮箱,拼用户名字典做喷洒
```

## 注意事项

多源邮箱收割+在线报告服务,输出可直接喂 spraying 工具的用户名清单。
