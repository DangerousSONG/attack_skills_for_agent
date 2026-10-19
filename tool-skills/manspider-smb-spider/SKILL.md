---
name: manspider-smb-spider
description: 渗透工具 skill:MANSPIDER 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 MANSPIDER 时使用。
---

# MANSPIDER

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/blacklanternsecurity/MANSPIDER
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install man-spider
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `man-spider 10.0.0.0/24 -f 'password|secret'` | SMB 文件内容搜索 |
| `-e txt,xml,config` | 扩展名 |
| `-u admin -p pass -d corp.local` | 凭据 |
| `-t 50` | 线程 |

## 攻击场景 Playbook

### 全网 SMB 敏感文件收割

```bash
man-spider 10.0.0.0/24 -f 'passw|secret|cred' -e txt,xml,ini,config
# 域内共享搜密码,Black Lantern 出品
```

## 注意事项

SMB 共享批量爬取+内容匹配,域内凭据发现神器。
