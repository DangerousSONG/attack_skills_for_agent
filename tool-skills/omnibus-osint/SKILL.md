---
name: omnibus-osint
description: "Fast IP/domain intelligence. Signals: email collection, employee info, OSINT CLI, IP intelligence, domain intelligence."
zh-signals: "Omnibus: IP/域名快速情报。信号:邮箱收集,员工信息,OSINT CLI,IP 情报,域名情报。"
---

# Omnibus

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/InQuest/Omnibus
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/InQuest/Omnibus && cd Omnibus && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 omnibus.py` | OSINT CLI |
| `intel 1.2.3.4` | IP 情报 |
| `intel evil.com` | 域名情报 |
| `report` | 生成报告 |

## 攻击场景 Playbook

### IP/域名快速情报

```bash
python3 omnibus.py intel corp.com
# InQuest 出品,威胁情报聚合
```

## 注意事项

InQuest 出品的 OSINT CLI,简洁高效。
