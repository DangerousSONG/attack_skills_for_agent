---
name: ttpassgen-mask
description: "ttpassgen generates multi-encoding masks. Signals: password cracking, hash cracking, statistics"
zh-signals: "ttpassgen: 多编码掩码生成。信号:密码破解,哈希破解,统计。"
---

# ttpassgen

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/tp7309/TTPassGen
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install TTpassgen
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ttpassgen -t '?l?l?l?d?d' -o out.txt` | 掩码生成 |
| `-t pattern -s` | 统计 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 多编码掩码生成

```bash
ttpassgen -t '?l?l?d?d?d'
# 支持 GBK/Big5 等编码
```

## 注意事项

多编码掩码字典生成,中文场景适用。
