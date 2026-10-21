---
name: hexstrike-ai
description: 渗透工具 skill:HexStrike-AI 的安装、参数速查与攻击场景 playbook。当任务涉及 AI与大模型安全 需要调用 HexStrike-AI 时使用。
when-to-use: 渗透工具 skill:HexStrike-AI 的安装、参数速查与攻击场景 playbook。当任务涉及 AI与大模型安全 需要调用 HexStrike-AI 时使用。
---

# HexStrike-AI

- 攻击大类:C44 AI与大模型安全
- 上游仓库:https://github.com/0x4m4/hexstrike-ai
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0x4m4/hexstrike-ai && cd hexstrike-ai && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 hexstrike.py -t 'https://t.com'` | AI 辅助渗透 |
| `-t url -m nmap` | 模块 |
| `-t url -ai` | AI 分析 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### LLM 辅助渗透测试

```bash
python3 hexstrike.py -t corp.com
# 多 agent AI 渗透,自动生成命令
```

## 注意事项

AI 驱动的渗透测试助手。
