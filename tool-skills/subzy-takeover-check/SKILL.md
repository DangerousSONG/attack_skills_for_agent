---
name: subzy-takeover-check
description: 渗透工具 skill:Subzy 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 Subzy 时使用。
when-to-use: 渗透工具 skill:Subzy 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 Subzy 时使用。
---

# Subzy

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/LukaSikic/subzy
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/LukaSikic/subzy@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `subzy run --targets subs.txt` | 批量接管检测 |
| `--concurrency 20` | 并发 |
| `--hide_fails` | 只显示命中 |
| `--https` | 强制 HTTPS |
| `--output out.json` | JSON 输出 |

## 攻击场景 Playbook

### 子域接管终检

```bash
subzy run --targets subs.txt --hide_fails --output takeover.json
cat takeover.json | jq '.[].subdomain'
```

## 注意事项

并发高指纹全;与 subjack 互补,两个都跑降低漏报。
