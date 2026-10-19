---
name: davtest-webdav
description: 渗透工具 skill:davtest 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 davtest 时使用。
---

# davtest

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/cldrn/davtest
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/cldrn/davtest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `perl davtest.pl -url http://t.com/webdav` | WebDAV 上传测试 |
| `-auth user:pass` | 认证 |
| `-directory dir` | 上传目录 |
| `-cleanup` | 测后清理 |

## 攻击场景 Playbook

### WebDAV 可写验证

```bash
perl davtest.pl -url http://target:8080/webdav -auth user:pass
# 自动尝试上传多种脚本(jsp/php/aspx)并访问验证
```

## 注意事项

配合 cadaver 交互操作;WebDAV 可写基本等于 webshell 到手。
