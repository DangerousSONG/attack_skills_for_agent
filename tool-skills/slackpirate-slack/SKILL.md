---
name: slackpirate-slack
description: 渗透工具 skill:SlackPirate 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 SlackPirate 时使用。
when-to-use: 渗透工具 skill:SlackPirate 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 SlackPirate 时使用。
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
