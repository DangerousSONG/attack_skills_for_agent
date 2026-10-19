---
name: bbot-automated-recon
description: 渗透工具 skill:BBOT 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 BBOT 时使用。
---

# BBOT

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/blacklanternsecurity/bbot
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install bbot
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bbot -t target.com -p subdomain-enum` | 子域名枚举 preset |
| `-p web-basic` | web 指纹+截图基础 preset |
| `-p cloud-enum` | 云资产(S3/GCP bucket)枚举 |
| `-f passive` | 纯被动(不触目标) |
| `-f active` | 允许主动探测 |
| `-o .` | 输出目录 |
| `--output-modules neo4j` | 结果直接进 neo4j |

## 攻击场景 Playbook

### 全域资产测绘一站式

```bash
bbot -t corp.com -p subdomain-enum web-basic cloud-enum -f passive -o out
# out/ 下有 JSON/CSV/TXT 全部资产与 URL
```

### 被动前置→主动补漏

```bash
bbot -t corp.com -p subdomain-enum -f passive
bbot -t corp.com -p web-basic -f active -o out2
```

## 注意事项

模块化 pipeline 设计,preset 决定调用哪些模块;被动模式不发送任何包到目标,合规友好。
