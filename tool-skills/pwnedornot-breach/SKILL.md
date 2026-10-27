---
name: pwnedornot-breach
description: PwnedOrNot: 邮箱泄露库查询拿明文口令。信号:邮箱收集,员工信息,邮箱泄露查询,批量,仅受泄。
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

### 邮箱泄露库查询拿明文口令

```bash
python3 pwnedornot.py -e ceo@corp.com
# HaveIBeenPwned 含明文密码泄露部分
```

## 注意事项

whiteh4t 出品,HIBP 增强版,返回泄露密码部分。
