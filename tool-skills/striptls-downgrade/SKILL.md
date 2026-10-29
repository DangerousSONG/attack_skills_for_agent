---
name: striptls-downgrade
description: "striptls performs STARTTLS downgrade attacks. Signals: MITM, mitm, IMAP downgrade, transparent mode"
zh-signals: "striptls: STARTTLS 降级攻击。信号:中间人,mitm,IMAP 降级,透明模式。"
---

# striptls

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/tintinweb/striptls
- 上游 License:CC0-1.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install striptls
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `striptls --server 0.0.0.0:25` | SMTP STARTTLS 降级 |
| `--server 0.0.0.0:143` | IMAP 降级 |
| `-f` | 透明模式 |

## 攻击场景 Playbook

### STARTTLS 降级攻击

```bash
striptls --server 0.0.0.0:25
# 邮件协议降级嗅探
```

## 注意事项

STARTTLS 降级框架,tintinweb 出品。
