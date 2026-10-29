---
name: untwister-prng
description: "untwister: Token seed recovery. Signals: cryptographic attack, encryption cracking, PRNG seed recovery, glibc rand, upper limit."
zh-signals: "untwister: token 种子恢复。信号:密码学攻击,加密破解,PRNG 种子恢复,glibc rand,上限。"
---

# untwister

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/altf4/untwister
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/altf4/untwister && cd untwister && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./untwister -r mt19937 < randoms.txt` | PRNG 种子恢复 |
| `-r glibc` | glibc rand |
| `-u 1000` | 上限 |

## 攻击场景 Playbook

### token 种子恢复

```bash
seq 1 100 | ./untwister -r mt19937
# 预测 session token
```

## 注意事项

PRNG 种子恢复,多算法支持。
