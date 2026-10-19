---
name: narthex-pass-gen
description: 渗透工具 skill:narthex 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 narthex 时使用。
---

# narthex

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/MichaelConstant/narthex
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/MichaelConstant/narthex && cd narthex && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./nhance -w wordlist.txt -o out.txt` | 字典增强 |
| `./ncombi -i in -o out` | 组合 |
| `./ninsert -i in -c 123` | 插入 |
| `./nleet -i in` | leet 变换 |

## 攻击场景 Playbook

### 字典增强流水线

```bash
cat base.txt | ./nhance | ./nleet > final.txt
# 组合/插入/变换全家桶
```

## 注意事项

字典操作工具集,hashcat 规则替代。
