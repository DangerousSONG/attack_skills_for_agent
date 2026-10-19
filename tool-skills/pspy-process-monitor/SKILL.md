---
name: pspy-process-monitor
description: 渗透工具 skill:pspy 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 pspy 时使用。
---

# pspy

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/DominicBreuker/pspy
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
release 下载 pspy64 / pspy32 静态二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pspy64` | 监控全部进程+定时任务(无需 root) |
| `-pf` | 只监控进程 fork |
| `-i 1000` | 打印间隔 |
| `-c` | 高亮新进程 |

## 攻击场景 Playbook

### 定时任务提权线索捕捉

```bash
./pspy64  # 观察 root cron 调用了哪些脚本/二进制,找可写路径劫持
```

## 注意事项

64/32 位与静态/动态版本四选;容器/老内核用 pspy32s。
