---
name: statsprocessor-maskgen
description: 渗透工具 skill:Statsprocessor 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 Statsprocessor 时使用。
---

# Statsprocessor

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/hashcat/statsprocessor
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hashcat/statsprocessor && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./statsgen.bin wordlist.txt -o stats` | 从字典生成马尔可夫统计 |
| `./sp64.bin stats --threshold 30 -o candidates.txt` | 按统计生成候选 |
| `--pw-min 8 --pw-max 12` | 长度范围 |

## 攻击场景 Playbook

### 基于语料的定向字典生成

```bash
./statsgen.bin leaked_corp_passwords.txt -o corp.stats && ./sp64.bin corp.stats -o corp_candidates.txt
# 生成与目标组织口令习惯高度吻合的候选
```

## 注意事项

hashcat 团队出品,马尔可夫链模型从泄露口令学习,生成高命中率候选字典。
