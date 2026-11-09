---
name: gobuster-dir-dns
description: "gobuster discovers directories, admin panels, and subdomains for asset mapping. Signals: web scanning, vulnerability scanning, directory/file brute-forcing, virtual host brute-forcing."
zh-signals: "gobuster: 目录与后台发现、子域名枚举接资产梳理。信号:web扫描,漏洞扫描,目录/文件爆破,虚拟主机爆破。"
---

# gobuster

- 攻击大类:C41 Web漏洞扫描与验证
- 上游仓库:https://github.com/OJ/gobuster
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/OJ/gobuster/v3@latest
# 或 apt install gobuster (Kali 自带)
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dir -u URL -w wordlist.txt` | 目录/文件爆破 |
| `dns -d target.com -w subdomains.txt` | 子域名枚举 |
| `vhost -u URL -w vhosts.txt` | 虚拟主机爆破 |
| `fuzz -u URL/FUZZ -w params.txt` | 参数/路径点 fuzz |
| `-t 50` | 线程数 |
| `-x php,txt,bak` | 目录模式追加扩展名 |
| `-s 200,204,301,302,307` | 只显示这些状态码 |
| `-k` | 忽略 HTTPS 证书错误 |
| `--wildcard` | DNS 模式处理泛解析 |
| `-o result.txt` | 输出到文件 |

## 攻击场景 Playbook

### 目录与后台发现

```bash
gobuster dir -u https://target.com -w /usr/share/seclists/Discovery/Web-Content/common.txt -x php,html,bak -t 80 -o dirs.txt
```

### 子域名枚举接资产梳理

```bash
gobuster dns -d target.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -o subs.txt
cat subs.txt | awk '{print $2}' | sort -u
```

### 隐藏虚拟主机与参数点发现

```bash
gobuster vhost -u https://target.com -w vhost-wordlist.txt -t 50
gobuster fuzz -u "https://target.com/api/FUZZ" -w api-endpoints.txt -mc 200,401,403
```

## 注意事项

与 dirsearch/feroxbuster 功能重叠时优先选它做 DNS 与 vhost 模式;DNS 模式记得加 `--wildcard` 排除泛解析污染结果。
