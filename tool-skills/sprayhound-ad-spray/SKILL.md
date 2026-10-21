---
name: sprayhound-ad-spray
description: 渗透工具 skill:sprayhound 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 sprayhound 时使用。
when-to-use: 渗透工具 skill:sprayhound 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 sprayhound 时使用。
---

# sprayhound

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/Hackndo/sprayhound
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Hackndo/sprayhound && cd sprayhound && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sprayhound -d corp.local -u users.txt -p passwords.txt` | 喷洒+BH 联动 |
| `-d d -u u.txt -p p.txt -b` | BloodHound 集成 |
| `-t 5` | 线程 |

## 攻击场景 Playbook

### 喷洒结果直通攻击路径

```bash
sprayhound -d corp.local -u users.txt -p pass.txt -b
# 命中后自动查 BH 最短路径
```

## 注意事项

Hackndo 出品,密码喷洒+BloodHound 集成,命中即出攻击路径。
