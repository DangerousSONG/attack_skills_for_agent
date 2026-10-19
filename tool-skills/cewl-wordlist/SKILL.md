---
name: cewl-wordlist
description: 渗透工具 skill:CeWL 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 CeWL 时使用。
---

# CeWL

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/digininja/CeWL
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install cewl
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cewl https://target.com -w custom.txt` | 站点生成字典 |
| `-d 3` | 爬深 |
| `-m 8` | 最小长度 |
| `-x 20` | 最大长度 |
| `-e` | 收集邮箱 |
| `-c` | 统计词频 |
| `--with-numbers` | 追加数字变体 |

## 攻击场景 Playbook

### 目标定制口令字典

```bash
cewl https://corp.com -d 2 -m 6 -w corp_words.txt
hashcat -m 5600 ntlm.txt corp_words.txt --rules-file dive.rule
```

## 注意事项

从目标站文本生成高命中率字典;人名/项目代号/口号都在里面。
