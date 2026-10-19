---
name: shuffledns-brute
description: 渗透工具 skill:shuffledns 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 shuffledns 时使用。
---

# shuffledns

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/projectdiscovery/shuffledns
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-d corp.com -w subdomains.txt -r resolvers.txt` | 子域爆破 |
| `-list targets.txt` | 批量 |
| `-massdns /opt/massdns/bin/massdns` | massdns 路径 |
| `-o out.txt` | 输出 |
| `-strict-wildcard` | 严格通配符检测 |

## 攻击场景 Playbook

### 大规模子域爆破

```bash
shuffledns -d corp.com -w ~/wordlists/all.txt -r ~/resolvers/resolvers.txt -massdns /usr/local/bin/massdns -o subs.txt
cat subs.txt | dnsx -a -resp
```

## 注意事项

pd 生态的 massdns 封装,通配符过滤准;大字典(百万级)爆破的主力。
