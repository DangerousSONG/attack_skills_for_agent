---
name: duplicut-dedup
description: 渗透工具 skill:duplicut 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 duplicut 时使用。
when-to-use: 渗透工具 skill:duplicut 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 duplicut 时使用。
---

# duplicut

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/nil0x42/duplicut
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nil0x42/duplicut && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./duplicut wordlist.txt -o clean.txt` | 大字典去重 |
| `-i in -o out -l 8` | 长度过滤 |
| `-m 10000000` | 内存限制 |

## 攻击场景 Playbook

### 50GB 字典秒级去重

```bash
./duplicut big.txt -o clean.txt
# 内存映射,比 sort -u 快百倍
```

## 注意事项

nil0x42 出品,大字典去重工具。
