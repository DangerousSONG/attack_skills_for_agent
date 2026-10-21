---
name: rustbuster-content-discover
description: 渗透工具 skill:rustbuster 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 rustbuster 时使用。
when-to-use: 渗透工具 skill:rustbuster 的安装、参数速查与攻击场景 playbook。当任务涉及 Web漏洞扫描与验证 需要调用 rustbuster 时使用。
---

# rustbuster

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/phra/rustbuster
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install rustbuster
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `rustbuster dir -u https://t.com -w wordlist.txt` | 目录爆破 |
| `rustbuster dns -d t.com -w subs.txt` | 子域爆破 |
| `rustbuster vhost -u https://t.com -w vhosts.txt` | 虚拟主机爆破 |
| `rustbuster fuzz -u https://t.com/FUZZ -w params.txt` | 参数 fuzz |
| `-t 40` | 线程 |
| `-x php,txt,bak` | 扩展名 |

## 攻击场景 Playbook

### 多模式内容发现

```bash
rustbuster dir -u https://t.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -t 50
# 一个二进制覆盖 dir/dns/vhost/fuzz 四种模式
```

## 注意事项

Rust 编写,单文件多模式内容发现,速度极快,适合大规模资产。
