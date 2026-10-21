---
name: pydictor-wordlist
description: 渗透工具 skill:pydictor 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 pydictor 时使用。
when-to-use: 渗透工具 skill:pydictor 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 pydictor 时使用。
---

# pydictor

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/LandGrey/pydictor
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/LandGrey/pydictor && cd pydictor
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 pydictor.py -base d -len 6 8 -o out.txt` | 基础字典生成 |
| `-extend word --level 4` | 扩展模式 |
| `-plug pid6` | 插件 |
| `--sedb` | 社工模式 |

## 攻击场景 Playbook

### 全模式密码字典

```bash
python3 pydictor.py --sedb
# 交互社工字典工厂
```

## 注意事项

强大密码字典生成框架,50+ 模式。
