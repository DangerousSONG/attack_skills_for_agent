---
name: dublin-traceroute-nat
description: 渗透工具 skill:dublin-traceroute 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 dublin-traceroute 时使用。
when-to-use: 渗透工具 skill:dublin-traceroute 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 dublin-traceroute 时使用。
---

# dublin-traceroute

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/insomniacslk/dublin-traceroute
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install dublin-traceroute
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dublin-traceroute 8.8.8.8` | NAT 感知 traceroute |
| `-o out.json` | JSON |
| `--indent` | 可读 |

## 攻击场景 Playbook

### NAT 路径测绘

```bash
dublin-traceroute corp.com
# 识别 NAT 设备+多路径
```

## 注意事项

insomniacslk 出品,NAT 感知的 traceroute。
