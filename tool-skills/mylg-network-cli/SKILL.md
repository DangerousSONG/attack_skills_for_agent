---
name: mylg-network-cli
description: 渗透工具 skill:mylg 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 mylg 时使用。
---

# mylg

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/mehrdadrad/mylg
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/mehrdadrad/mylg@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `mylg scan 10.0.0.0/24` | 综合网络扫描 |
| `mylg trace 8.8.8.8` | 路由跟踪 |
| `mylg dns t.com` | DNS 查询 |
| `mylg whois t.com` | WHOIS |

## 攻击场景 Playbook

### 瑞士军刀式网络诊断

```bash
mylg scan 10.0.0.0/24 --ping
# 扫描+ping 一体化
```

## 注意事项

网络工程师工具集: ping/trace/dns/scan/whois 一体。
