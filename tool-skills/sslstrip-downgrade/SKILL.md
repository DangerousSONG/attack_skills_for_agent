---
name: sslstrip-downgrade
description: "sslstrip downgrades HTTPS to HTTP. Signals: MITM, mitm, logging, POST only"
zh-signals: "sslstrip: HTTPS 降级 HTTP。信号:中间人,mitm,日志,仅 post。"
---

# sslstrip

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/moxie0/sslstrip
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install sslstrip
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sslstrip -l 8080` | HTTPS 降级 |
| `-w log.txt` | 日志 |
| `-p` | 仅 post |

## 攻击场景 Playbook

### HTTPS 降级 HTTP

```bash
sslstrip -l 8080
# 配合 ARP 欺骗,明文收割
```

## 注意事项

经典 HTTPS 降级攻击工具。
