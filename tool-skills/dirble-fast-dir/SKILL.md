---
name: dirble-fast-dir
description: dirble: 高速目录爆破。信号:web漏洞,注入,目录扫描,字典+线程,递归。
---

# dirble

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/nccgroup/dirble
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install dirble
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dirble https://t.com` | 目录扫描 |
| `dirble url -w wordlist.txt -t 20` | 字典+线程 |
| `-r` | 递归 |
| `-e php,html` | 扩展 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 高速目录爆破

```bash
dirble https://t.com -t 50
# NCC 出品 Rust 编写,速度极快
```

## 注意事项

NCC 出品的 Rust 目录扫描器,性能优于 dirb 系。
