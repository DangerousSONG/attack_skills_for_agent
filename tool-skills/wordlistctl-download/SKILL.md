---
name: wordlistctl-download
description: wordlistctl: BlackArch 字典仓库。信号:密码破解,哈希破解,字典下载,列表,搜索。
---

# wordlistctl

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/BlackArch/wordlistctl
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/BlackArch/wordlistctl && cd wordlistctl
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 wordlistctl.py -f rockyou -d` | 字典下载 |
| `-l` | 列表 |
| `-s 'category'` | 搜索 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### BlackArch 字典仓库

```bash
python3 wordlistctl.py -f rockyou -d
# 300+ 字典一键管理
```

## 注意事项

BlackArch 字典管理工具。
