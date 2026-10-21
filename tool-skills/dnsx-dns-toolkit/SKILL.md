---
name: dnsx-dns-toolkit
description: 渗透工具 skill:dnsx 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 dnsx 时使用。
when-to-use: 渗透工具 skill:dnsx 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 dnsx 时使用。
---

# dnsx

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/projectdiscovery/dnsx
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-l subdomains.txt` | 批量解析 |
| `-resp` | 只显示有响应的 |
| `-a -aaaa -cname` | 拉 A/AAAA/CNAME 记录 |
| `-txt` | 拉 TXT(SPF/验证 token 泄露) |
| `-retry 3` | 重试次数 |
| `-rcode noerror,servfail` | 按响应码过滤 |
| `-mx -ns` | MX/NS 记录 |

## 攻击场景 Playbook

### 子域存活+记录枚举

```bash
subfinder -d target.com | dnsx -a -aaaa -cname -txt -resp -o resolved.txt
```

### SPF/DMARC 邮件 spoof 面评估

```bash
dnsx -d target.com -txt -resp | grep -i spf
dig _dmarc.target.com txt +short
```

## 注意事项

projectdiscovery 生态,管道接 subfinder/naabu 最顺;-resp 过滤 NXDOMAIN 噪音。
