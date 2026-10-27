---
name: phpsploit-c2-console
description: phpsploit: 隐蔽 PHP C2 客户端。信号:webshell,rce,连接 PHP shell,混淆载荷,文件传输。
---

# phpsploit

- 攻击大类:C13 远程命令执行与WebShell
- 上游仓库:https://github.com/nil0x42/phpsploit
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nil0x42/phpsploit && cd phpsploit
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./phpsploit --target https://t.com/shell.php` | 连接 PHP shell |
| `set PAYLOAD obfuscate` | 混淆载荷 |
| `upload/download` | 文件传输 |
| `exploit` | 执行模块 |

## 攻击场景 Playbook

### 隐蔽 PHP C2 客户端

```bash
./phpsploit --target https://t.com/files/shell.php
# 全功能控制台: 代理/编码/TLS 指纹伪装,常驻后门管理
```

## 注意事项

PHP shell 全功能客户端,流量混淆+隧道+插件系统,渗透场景的后门管理器。
