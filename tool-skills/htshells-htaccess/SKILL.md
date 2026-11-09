---
name: htshells-htaccess
description: "htshells provides .htaccess webshells. Signals: webshell, RCE, PHP execution, CGI execution."
zh-signals: "htshells: .htaccess webshell。信号:webshell,rce,PHP 执行,CGI 执行。"
---

# htshells

- 攻击大类:C13 远程命令执行与WebShell
- 上游仓库:https://github.com/wireghoul/htshells
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/wireghoul/htshells
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `.htaccess 上传` | 把 shell 作为 .htaccess 上传 |
| `mod_php 模式` | PHP 执行 |
| `mod_cgi 模式` | CGI 执行 |

## 攻击场景 Playbook

### .htaccess webshell

```bash
# 上传受控 .htaccess 到可写 Apache 目录
# 通过特定 UA/URI 触发隐藏的 PHP 后门
```

## 注意事项

.htaccess 本身就是 webshell 的冷门技巧;适合文件名白名单严格但允许 .htaccess 的场景。
