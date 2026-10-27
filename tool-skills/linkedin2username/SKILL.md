---
name: linkedin2username
description: linkedin2username: LinkedIn 员工用户名。信号:邮箱收集,员工信息,员工用户名生成,深挖。
---

# linkedin2username

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/initstring/linkedin2username
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/initstring/linkedin2username
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 linkedin2username.py -c target -u user@mail.com -p pass` | 员工用户名生成 |
| `-c company -n` | 深挖 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### LinkedIn 员工用户名

```bash
python3 linkedin2username.py -c 'Target Corp' -u me@mail.com
# 登录态爬员工名录转用户名
```

## 注意事项

initstring 出品,LinkedIn 公司页转用户名字典。
