---
name: pwcrack-framework
description: 渗透工具 skill:pwcrack 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 pwcrack 时使用。
when-to-use: 渗透工具 skill:pwcrack 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 pwcrack 时使用。
---

# pwcrack

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/L-codes/pwcrack-framework
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/L-codes/pwcrack-framework && cd pwcrack-framework
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pwcrack md5:5d41402abc4b2a76b9719d911017c592` | 在线哈希破解 |
| `./pwcrack md5:f0e1d2c3b4a5968778695a4b3c2d1e0f` | 多引擎 |
| `-f file` | 批量 |

## 攻击场景 Playbook

### 在线哈希破解聚合

```bash
./pwcrack md5:$HASH
# 40+ 在线库一键查
```

## 注意事项

在线哈希破解框架,聚合多库。
