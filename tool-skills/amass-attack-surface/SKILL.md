---
name: amass-attack-surface
description: 渗透工具 skill:Amass 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Amass 时使用。
when-to-use: 渗透工具 skill:Amass 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Amass 时使用。
---

# Amass

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/owasp-amass/amass
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/owasp-amass/amass/v4/...@master 或 snap install amass
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `amass enum -d target.com` | 被动+主动枚举 |
| `-passive` | 纯被动 |
| `-active` | 主动探测含 TLS 指纹 |
| `-src -v` | 显示数据来源 |
| `-o out.txt` | 输出 |
| `amass intel -d target.com -whois` | ASN/whois 情报 |
| `-config config.ini` | API key 配置 |

## 攻击场景 Playbook

### 深度攻击面测绘

```bash
amass enum -d corp.com -active -o subs.txt
amass intel -d corp.com -whois  # 找关联 ASN/域名
```

### 带 API key 的增强枚举

```bash
amass enum -d target.com -config ~/.config/amass/config.ini -passive
```

## 注意事项

OWASP 出品,数据源最全的测绘工具;config.ini 配 Shodan/Censys 等 API key 后效果显著提升。
