---
name: webhandler-shell
description: webhandler: WebShell 管理。信号:web漏洞,注入,WebShell 客户端,单命令,交互。
---

# webhandler

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/lnxg33k/webhandler
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/lnxg33k/webhandler && cd webhandler
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python webhandler.py --url 'https://t.com/shell.php' --password x` | WebShell 客户端 |
| `--url url --cmd id` | 单命令 |
| `--interactive` | 交互 |

## 攻击场景 Playbook

### WebShell 管理

```bash
python webhandler.py --url 'https://t.com/c99.php' --password pass
# 文件管理+命令执行+数据库
```

## 注意事项

PHP WebShell 客户端,支持密码认证+交互终端。
