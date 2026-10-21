---
name: pwnedornot-breach
description: 渗透工具 skill:PwnedOrNot 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 PwnedOrNot 时使用。
when-to-use: 渗透工具 skill:PwnedOrNot 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 PwnedOrNot 时使用。
---

# PwnedOrNot

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/thewhiteh4t/pwnedOrNot
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/thewhiteh4t/pwnedOrNot && cd pwnedOrNot
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 pwnedornot.py -e victim@mail.com` | 邮箱泄露查询 |
| `-f emails.txt` | 批量 |
| `-b` | 仅受泄 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 邮箱泄露+密码明文

```bash
python3 pwnedornot.py -e ceo@corp.com
# HaveIBeenPwned 含明文密码泄露部分
```

## 注意事项

whiteh4t 出品,HIBP 增强版,返回泄露密码部分。
