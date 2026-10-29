---
name: spray365-o365
description: "Spray365: smart O365 password spraying. Signals: brute force, password spraying, O365 spray, adaptive."
zh-signals: "Spray365: O365 智能喷洒。信号:暴力破解,口令喷射,O365 喷洒,自适应。"
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
