---
name: sccmhunter-sccm-attack
description: SCCMHunter: SCCM 站点资产测绘。信号:ad攻击,域渗透,查看站点详情,票据复用模式,调试输出。
---

# SCCMHunter

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/garrettfoster13/sccmhunter
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/garrettfoster13/sccmhunter && cd sccmhunter && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sccmhunter -u user -p pass -d corp.local http -ip 10.0.0.5` | MECM/SCCM 站点信息枚举 |
| `sccmhunter -u user -p pass -d corp.local show -computer sccm01` | 查看站点详情 |
| `sccmhunter ... smb -ip 10.0.0.5` | SCCM 分发点 shares 枚举 |
| `-reuse-pwd 1` | 票据复用模式 |
| `-debug` | 调试输出 |

## 攻击场景 Playbook

### SCCM 站点资产测绘

```bash
sccmhunter -u lowpriv -p 'Pass1' -d corp.local http -ip 10.0.0.10
# 找到站点服务器→进一步看 DP/MP 角色,为 NAA 凭据窃取铺路
```

## 注意事项

微软配置管理器(MECM/SCCM)攻击工具: HTTP 查询/WMI/SMB 枚举站点信息、DP 内容、NAA 凭据。
