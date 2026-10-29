---
name: platypus-shell-manager
description: "Centralized reverse shell management. Signals: webshell, rce, start service :7331, listening port, interaction."
zh-signals: "Platypus: 反弹 shell 集中管控。信号:webshell,rce,起服务(:7331),监听端口,交互。"
---

# Platypus

- 攻击大类:C13 远程命令执行与WebShell
- 上游仓库:https://github.com/WangYihang/Platypus
- 上游 License:LGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/WangYihang/Platypus@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./platypus` | 起服务(:7331) |
| `listen 0.0.0.0 13337` | 监听端口 |
| `JumpServer` | 交互 |
| `Upgrade` | 会话升级为 meterpreter |
| `RESTful API` | 自动化集成 |

## 攻击场景 Playbook

### 反弹 shell 集中管控

```bash
./platypus
platypus > listen 0.0.0.0 4444
# Web UI 管理所有回连会话,支持批量命令与一键升级
```

## 注意事项

Go 写的多会话管理器,带 Web UI 和 RESTful API,方便 Agent 自动化集成。
