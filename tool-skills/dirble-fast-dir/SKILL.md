---
name: dirble-fast-dir
description: 渗透工具 skill:dirble 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 dirble 时使用。
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
