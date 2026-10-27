---
name: wordlister-basic
description: Wordlister: 关键词组合字典。信号:密码破解,哈希破解,模式。
---

# Wordlister

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/4n4nk3/Wordlister
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/4n4nk3/Wordlister && cd Wordlister
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 wordlister.py -w 'word1 word2' -m 8 -o out.txt` | 组合字典 |
| `-w words -m min --cap -l -n` | 模式 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 关键词组合字典

```bash
python3 wordlister.py -w 'admin target 2024'
# 大小写+数字+符号组合
```

## 注意事项

轻量关键词组合字典生成。
