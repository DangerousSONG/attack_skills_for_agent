---
name: filebuster-dav-buster
description: filebuster: WebDAV/虚拟主机 fuzz。信号:web漏洞,注入,HTTP fuzz,扩展,自定义头。
---

# filebuster

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/henshin/filebuster
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/henshin/filebuster
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `perl filebuster.pl -u https://t.com/FUZZ -w wordlist.txt` | HTTP fuzz |
| `-u url -w w.txt -x php,txt` | 扩展 |
| `-H 'Cookie: x=1'` | 自定义头 |
| `-t 20` | 线程 |

## 攻击场景 Playbook

### WebDAV/虚拟主机 fuzz

```bash
perl filebuster.pl -u https://t.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
# Perl 高性能,支持递归
```

## 注意事项

Perl 编写的 HTTP fuzzer,支持 header/POST/自定义方法。
