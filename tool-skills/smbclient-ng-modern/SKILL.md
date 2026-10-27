---
name: smbclient-ng-modern
description: smbclient-ng: 交互式 SMB 操作。信号:内网枚举,网络发现,现代 SMB 客户端,共享浏览,下载。
---

# smbclient-ng

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/p0dalirius/smbclient-ng
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install smbclientng
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `smbclient-ng -H 10.0.0.5 -u svc -p pass -d corp.local` | 现代 SMB 客户端 |
| `use shares` | 共享浏览 |
| `get secrets.txt` | 下载 |
| `put file` | 上传 |
| `modules` | 后渗透模块 |

## 攻击场景 Playbook

### 交互式 SMB 操作

```bash
smbclient-ng -H dc01 -u svc -p pass -d corp
# p0dalirius 出品,smbclient 现代化替代
```

## 注意事项

现代 SMB 客户端,带彩色界面+模块系统。
