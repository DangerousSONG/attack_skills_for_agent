---
name: gitgraber-secrets
description: 渗透工具 skill:gitGraber 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 gitGraber 时使用。
when-to-use: 渗透工具 skill:gitGraber 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 gitGraber 时使用。
---

# gitGraber

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/hisxo/gitGraber
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hisxo/gitGraber && cd gitGraber && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 gitGraber.py -k 'corp.com'` | Github 实时监控 |
| `-k keyword -d` | 深度 |
| `-t 100` | 线程 |
| `-o out/` | 输出 |

## 攻击场景 Playbook

### Github 密钥实时监控

```bash
python3 gitGraber.py -k 'corp.com internal'
# 新 commit 中 AWS key/密码即时告警
```

## 注意事项

Github 密钥泄露监控工具。
