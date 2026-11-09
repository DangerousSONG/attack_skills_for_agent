---
name: finduncommonshares-smb-hunt
description: "pyFindUncommonShares finds sensitive data via uncommon shares. Signals: internal enumeration, network discovery, whole-network uncommon-share scan, specific share-name types, current-user readability checks."
zh-signals: "pyFindUncommonShares: 非常规共享找敏感数据。信号:内网枚举,网络发现,全网非常规共享扫描,特定共享名类型,顺带检查当前用户可读。"
---

# pyFindUncommonShares

- 攻击大类:C29 AD与LDAP枚举
- 上游仓库:https://github.com/p0dalirius/pyFindUncommonShares
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install git+https://github.com/p0dalirius/pyFindUncommonShares.git
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `finduncommonshares -u svc -p pass -d corp.local --dc-ip 10.0.0.1` | 全网非常规共享扫描 |
| `-t DFS-R` | 特定共享名类型 |
| `--check-user-access` | 顺带检查当前用户可读 |
| `-v` | 详细 |

## 攻击场景 Playbook

### 非常规共享找敏感数据

```bash
finduncommonshares -u svc -p pass -d corp.local --dc-ip 10.0.0.1
# backup$/scripts$/transfer$ 等共享,含密码脚本/凭据文件金矿
```

## 注意事项

p0dalirius 出品,扫域内所有机器的非默认 SMB 共享,并验证访问权限。
