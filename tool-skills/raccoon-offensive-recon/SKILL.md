---
name: raccoon-offensive-recon
description: Raccoon: 单目标一站式摸底。信号:资产测绘,指纹识别,一站式侦察,输出目录,走 Tor。
---

# Raccoon

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/evyatarmeged/Raccoon
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install raccoon-scanner
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `raccoon target.com` | 一站式侦察 |
| `-o out` | 输出目录 |
| `--tor` | 走 Tor |
| `-f` | 强制全部模块 |
| `--dns` | 仅 DNS |
| `--subdomains` | 仅子域 |

## 攻击场景 Playbook

### 单目标一站式摸底

```bash
raccoon corp.com -o raccoon_out
# DNS/WHOIS/子域/端口/指纹/Nmap 一次跑完
```

## 注意事项

聚合式侦察,输出目录结构清晰;Nmap 集成让它出报告即附端口结论。
