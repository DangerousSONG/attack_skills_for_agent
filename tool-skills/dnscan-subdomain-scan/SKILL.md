---
name: dnscan-subdomain-scan
description: dnscan: 递归子域爆破。信号:子域名,域名枚举,字典爆破子域,线程,发现子域后递归扫。
---

# dnscan

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/rbsec/dnscan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/rbsec/dnscan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python dnscan.py -d target.com -w wordlist.txt` | 字典爆破子域 |
| `-d domain -w subs.txt -t 30` | 线程 |
| `-D` | 发现子域后递归扫 |
| `-o out.txt` | 输出 |
| `-x example.com` | 排除域名 |

## 攻击场景 Playbook

### 递归子域爆破

```bash
python dnscan.py -d corp.com -w subdomains-top1mil.txt -D -o found.txt
```

## 注意事项

递归模式(-D)对深度子域(如 dev.us.corp.com)有效;支持通配符检测。
