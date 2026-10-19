---
name: snallygaster-secret-scan
description: 渗透工具 skill:snallygaster 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 snallygaster 时使用。
---

# snallygaster

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/hannob/snallygaster
- 上游 License:0BSD(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install snallygaster
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `snallygaster target.com` | 秘密文件扫描 |
| `-d` | 调试 |
| `--nohttp` | 禁 HTTP |
| `-n` | 忽略证书错误 |

## 攻击场景 Playbook

### Web 服务器敏感文件普查

```bash
snallygaster corp.com
# 默认查 /.git/.env/.svn/备份文件/phpinfo/数据库 dump 等 50+ 高危路径
```

## 注意事项

覆盖最全的'秘密文件'扫描器之一;纯被动 GET,授权边界内无侵入。
