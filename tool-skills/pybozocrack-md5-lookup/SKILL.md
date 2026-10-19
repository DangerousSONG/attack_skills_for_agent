---
name: pybozocrack-md5-lookup
description: 渗透工具 skill:PyBozoCrack 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 PyBozoCrack 时使用。
---

# PyBozoCrack

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/ikkebr/PyBozoCrack
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install pybozocrack
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `pybozocrack 1b8c...` | MD5 在线库查询 |
| `pybozocrack -f hashes.txt` | 批量 |
| `-s` | 含特殊字符 |

## 攻击场景 Playbook

### 弱哈希秒查

```bash
pybozocrack 5f4dcc3b5aa765d61d8327deb882cf99
# 已收录的常见口令直接返明文
```

## 注意事项

只查 Google 已索引的彩虹表结果,不破解复杂口令,但零成本秒查弱口令,适合快速初筛。
