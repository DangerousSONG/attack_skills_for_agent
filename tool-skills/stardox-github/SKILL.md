---
name: stardox-github
description: 渗透工具 skill:Stardox 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 Stardox 时使用。
when-to-use: 渗透工具 skill:Stardox 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 Stardox 时使用。
---

# Stardox

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/0xPrateek/Stardox
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0xPrateek/Stardox && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 stardox.py -r target/repo` | stargazer 分析 |
| `-r repo -d` | 详情 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 仓库 star 用户分析

```bash
python3 stardox.py -r corp/internal
# 谁在看内部仓库(内部人员?
```

## 注意事项

Github 仓库 star 者 OSINT。
