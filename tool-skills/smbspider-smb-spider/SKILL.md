---
name: smbspider-smb-spider
description: 渗透工具 skill:smbspider 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 smbspider 时使用。
---

# smbspider

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/T-S-A/smbspider
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/T-S-A/smbspider
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./smbspider.py -h 10.0.0.5 -u user -p pass -d corp.local` | SMB 文件爬取 |
| `-h ip -s share` | 指定共享 |
| `-f 'password|secret'` | 内容匹配 |

## 攻击场景 Playbook

### SMB 敏感文件内容搜

```bash
./smbspider.py -h dc01 -u svc -p pass -f 'passw|secret'
# 域内共享全文搜
```

## 注意事项

SMB 共享文件内容搜索。
