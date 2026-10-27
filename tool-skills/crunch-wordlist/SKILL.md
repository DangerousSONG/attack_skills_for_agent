---
name: crunch-wordlist
description: crunch: 掩码定向字典生成。信号:密码破解,哈希破解,按字符集生成,纯数字,掩码模板。
---

# crunch

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://sourceforge.net/projects/crunch-wordlist
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install crunch
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `crunch 8 10 -f /usr/share/crunch/charset.lst lalpha-numeric` | 按字符集生成 |
| `crunch 6 8 0123456789 -o num.txt` | 纯数字 |
| `crunch 8 8 -t admin@@@@` | 掩码模板 |
| `-s start -e end` | 起止范围 |
| `-b 500mb` | 按体积分卷 |

## 攻击场景 Playbook

### 掩码定向字典生成

```bash
crunch 10 10 -t '2024@@@@@' -o candidates.txt  # 公司前缀+年份模式掩码爆破
```

## 注意事项

经典字典生成器;掩码模板(-t)适合已知部分口令结构的定向爆破。
