---
name: spartan-sharepoint
description: "Spartan: asset mapping and fingerprinting. Signals: asset mapping, subdomain, deep enumeration."
zh-signals: "Spartan: 资产测绘与指纹识别场景。信号:资产测绘,子域名,深度枚举。"
---

# Spartan

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/NETSTAT-AFNL/Spartan
- 上游 License:NOASSERTION(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/NETSTAT-AFNL/Spartan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python spartan.py -u https://t.com` | Frontpage/SharePoint 指纹 |
| `-e` | 深度枚举 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### SharePoint/FrontPage 指纹+漏洞匹配

```bash
python spartan.py -u https://portal.corp.com
# 版本识别→历史 CVE 匹配→敏感路径(_vti_bin 等)探测
```

## 注意事项

SharePoint 专扫;_vti_pvt/service.pwd 之类老洞仍能捡漏。
