---
name: smbmap-share-enum
description: 渗透工具 skill:smbmap 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 smbmap 时使用。
when-to-use: 渗透工具 skill:smbmap 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 smbmap 时使用。
---

# smbmap

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/ShawnDEvans/smbmap
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install smbmap
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `smbmap -H 10.0.0.5` | 匿名/当前会话列共享 |
| `-u user -p pass -d corp -H ip` | 指定凭据 |
| `-R SHARE --depth 3` | 递归列目录 |
| `-A '.conf|.yml|.xml'` | 按扩展名搜文件 |
| `--upload path local SHARE/remote` | 上传 |
| `--download` | 下载 |
| `-x 'whoami'` | 远程执行(x 需配置) |

## 攻击场景 Playbook

### 共享盘敏感文件收割

```bash
smbmap -u svc -p Pass123 -d corp -H 10.0.0.5 -R DATA --depth 2 | grep -iE 'pass|secret|key|config'
```

### 批量可写共享排查

```bash
smbmap -u user -p pass -d corp --host-file ips.txt | grep -E 'READ,WRITE|WRITE'
```

## 注意事项

比 crackmapexec 共享枚举更细;--download 整个目录树效率高。
