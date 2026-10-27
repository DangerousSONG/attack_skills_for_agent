---
name: knockpy-subdomain
description: Knock: 子域枚举+接管检测。信号:子域名,域名枚举,被动+字典枚举,自定义字典,纯爆破模式。
---

# Knock

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/guelfoweb/knock
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install knockpy
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `knockpy target.com` | 被动+字典枚举 |
| `-w wordlist.txt` | 自定义字典 |
| `--bruteforce` | 纯爆破模式 |
| `-o json` | JSON 输出 |
| `--resolve` | 解析验证 |
| `-t 5` | 线程 |

## 攻击场景 Playbook

### 子域枚举+接管检测

```bash
knockpy corp.com -o json
jq -r '.subdomains[] | select(.zone_transfer==true)' report/*.json  # zone transfer 直接通关
```

## 注意事项

内置接管(three/others)检测;发现 zone transfer 时直接输出全部区域。
