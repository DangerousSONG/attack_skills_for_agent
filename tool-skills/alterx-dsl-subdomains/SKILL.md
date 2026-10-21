---
name: alterx-dsl-subdomains
description: 渗透工具 skill:alterx 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 alterx 时使用。
when-to-use: 渗透工具 skill:alterx 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 alterx 时使用。
---

# alterx

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/projectdiscovery/alterx
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/alterx/cmd/alterx@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-l known_subdomains.txt` | 基于已知子域生成候选 |
| `-list target.com` | 直接指定目标 |
| `-enrich` | 用 resolver 富化 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 被动结果驱动的新候选生成

```bash
subfinder -d corp.com -silent | alterx -enrich | dnsx -silent -a
# 从已知子域学习模式生成 api2/dev-v2 等新候选并解析
```

## 注意事项

pd 生态 DSL 置换引擎;比 altdns 模式更丰富,配合已知子域效果最佳。
