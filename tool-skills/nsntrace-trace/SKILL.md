---
name: nsntrace-trace
description: 渗透工具 skill:nsntrace 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 nsntrace 时使用。
---

# nsntrace

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/jonasdn/nsntrace
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install nsntrace
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `nsntrace -o out.pcap ping 8.8.8.8` | 按进程抓包 |
| `-o file -d` | 调试 |
| `-f filter` | 过滤 |

## 攻击场景 Playbook

### 进程级流量捕获

```bash
nsntrace -o malware.pcap ./suspect.bin
# 精确到进程的网络取证
```

## 注意事项

Linux 按进程名抓包工具。
