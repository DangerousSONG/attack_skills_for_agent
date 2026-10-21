---
name: fierce-dns-recon
description: 渗透工具 skill:Fierce 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Fierce 时使用。
when-to-use: 渗透工具 skill:Fierce 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Fierce 时使用。
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
