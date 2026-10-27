---
name: slackpirate-slack
description: SlackPirate: Slack 工作区渗透。信号:邮箱收集,员工信息,Slack 数据收割,Cookie 模式,全导出。
---

# SlackPirate

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/emtunc/SlackPirate
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/emtunc/SlackPirate && cd SlackPirate && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 SlackPirate.py --token xoxb-xxx` | Slack 数据收割 |
| `--cookie 'd=xxx'` | Cookie 模式 |
| `--dump` | 全导出 |
| `-o out/` | 输出 |

## 攻击场景 Playbook

### Slack 工作区渗透

```bash
python3 SlackPirate.py --token xoxb-leaked
# 搜密钥/文件/用户/频道
```

## 注意事项

Slack 信息收集: 消息/文件/令牌/敏感数据搜索。
