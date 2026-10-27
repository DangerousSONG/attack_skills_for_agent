---
name: shhgit-secret-monitor
description: shhgit: Github 实时监控泄密。信号:攻击面,云资产,扫本地仓库,CSV 输出。
---

# shhgit

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/eth0izzle/shhgit
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/eth0izzle/shhgit@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `shhgit --local path/to/repo` | 扫本地仓库 |
| `--live` | 实时监听 GitHub 事件流 |
| `-config config.yaml` | 配置 |
| `--csv-path out.csv` | CSV 输出 |
| `--entropy-threshold 5.0` | 熵阈值 |

## 攻击场景 Playbook

### Github 实时监控泄密

```bash
shhgit --live --csv-path leaks.csv  # 监听全 GitHub 事件流匹配 org 关键词/密钥模式
```

## 注意事项

实时模式需 GitHub token;与 trufflehog(深度扫)互补做广度监控。
