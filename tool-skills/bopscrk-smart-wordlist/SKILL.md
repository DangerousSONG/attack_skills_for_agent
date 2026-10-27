---
name: bopscrk-smart-wordlist
description: bopscrk: 社工字典智能生成。信号:密码破解,哈希破解,交互生成定向字典,关键字+年份。
---

# bopscrk

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/r3nt0n/bopscrk
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/r3nt0n/bopscrk && cd bopscrk
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 bopscrk.py -i` | 交互生成定向字典 |
| `-w 'John,Target' -y 1990-2000` | 关键字+年份 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 社工字典智能生成

```bash
python3 bopscrk.py -i
# 姓名+生日+爱好→高命中率字典
```

## 注意事项

社工信息转定向密码字典。
