---
name: rustscan-speed
description: 渗透工具 skill:RustScan 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 RustScan 时使用。
---

# RustScan

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/bee-san/RustScan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
docker run -it --rm --name rustscan rustscan/rustscan:latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `rustscan -a 10.0.0.5` | 单 IP 全端口 3 秒级 |
| `-a ips.txt` | 批量文件 |
| `-- -sV` | 透传参数给 nmap |
| `-b 2500` | batch 速率 |
| `-t 1500` | 超时 ms |

## 攻击场景 Playbook

### 单机全端口秒扫

```bash
rustscan -a 10.0.0.5 -- -sV -sC -oN deep.txt
# RustScan 先出开放端口,再自动带 nmap 指纹
```

## 注意事项

自适应 batch 扫描绕开 IDS 单 IP 阈值告警;Windows 下用 WSL 跑。
