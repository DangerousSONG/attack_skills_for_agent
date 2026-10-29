---
name: cracken-fast-crack
description: "cracken: Filters billion-scale dictionaries using masks. Signals: password cracking, hash cracking, high-speed mask filtering, range."
zh-signals: "cracken: 亿级字典掩码过滤。信号:密码破解,哈希破解,掩码高速过滤,范围。"
---

# cracken

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/shmuelamar/cracken
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install cracken
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cracken 'h?s?a' -w wordlist.txt` | 掩码高速过滤 |
| `-p pattern -m min-max` | 范围 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 亿级字典掩码过滤

```bash
cracken '?u?l?l?l?l?l?d' -w rockyou.txt
# Rust 性能,亿行秒级
```

## 注意事项

Rust 掩码过滤工具,配合现有字典用。
