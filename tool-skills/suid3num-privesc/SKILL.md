---
name: suid3num-privesc
description: suid3num: SUID 提权路径。信号:linux提权,suid,SUID 枚举,exploit,列表。
---

# suid3num

- 攻击大类:C16 Linux本地提权
- 上游仓库:https://github.com/Anon-Exploiter/SUID3NUM
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Anon-Exploiter/SUID3NUM
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 suid3num.py` | SUID 枚举 |
| `-e` | exploit |
| `-l` | 列表 |

## 攻击场景 Playbook

### SUID 提权路径

```bash
python3 suid3num.py
# GTFOBins 一键提权
```

## 注意事项

SUID 二进制自动枚举+利用。
