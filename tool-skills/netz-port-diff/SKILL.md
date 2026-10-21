---
name: netz-port-diff
description: 渗透工具 skill:netz 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 netz 时使用。
when-to-use: 渗透工具 skill:netz 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 netz 时使用。
---

# netz

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/spectralops/netz
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/spectralops/netz@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `netz 10.0.0.0/24` | 网段快照 |
| `netz diff snap1.json snap2.json` | 变化检测 |
| `-o out.json` | 输出 |

## 攻击场景 Playbook

### 网络变化监控

```bash
netz 10.0.0.0/24 -o before.json
# 渗透期间发现新上线服务
```

## 注意事项

SpectralOps 出品,网段快照+差异对比。
