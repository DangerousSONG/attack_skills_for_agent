---
name: mentalist-wordlist
description: 渗透工具 skill:Mentalist 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 Mentalist 时使用。
when-to-use: 渗透工具 skill:Mentalist 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 Mentalist 时使用。
---

# Mentalist

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/sc0tfree/mentalist
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/sc0tfree/mentalist && cd mentalist && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 mentalist.py` | 可视化字典生成 |
| `-w base.txt -m 'A1@'` | 变异 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### GUI 字典工厂

```bash
python3 mentalalist.py
# 交互构建高命中字典
```

## 注意事项

可视化密码字典生成器。
