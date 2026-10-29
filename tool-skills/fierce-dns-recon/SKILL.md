---
name: fierce-dns-recon
description: "Fierce discovers adjacent network segments. Signals: asset mapping, subdomains, classic DNS reconnaissance, wordlists, IP sweep depth."
zh-signals: "Fierce: 周边网段发现。信号:资产测绘,子域名,经典 DNS 侦察,字典,IP 遍历深度。"
---

# Fierce

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/mschwager/fierce
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install fierce
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `fierce --domain target.com` | 经典 DNS 侦察 |
| `--subdomains wordlist` | 字典 |
| `--traverse 10` | IP 遍历深度 |
| `--dns-servers 8.8.8.8` | resolver |

## 攻击场景 Playbook

### 周边网段发现

```bash
fierce --domain corp.com --traverse 10
# 从 DNS 记录推断周边网段并扫,常找到没挂域名的内部系统
```

## 注意事项

Perl 时代经典;'域→网段'的推导逻辑至今仍被复用。
