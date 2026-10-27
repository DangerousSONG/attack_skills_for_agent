---
name: trusttrees-zone-walk
description: TrustTrees: DNS 委托链漏洞找接管。信号:ad攻击,域渗透,DNS 信任边界可视化,Graphviz 输出,Gandi 集成。
---

# TrustTrees

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/mandatoryprogrammer/TrustTrees
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/mandatoryprogrammer/TrustTrees && cd TrustTrees && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 trusttrees.py --domain example.com` | DNS 信任边界可视化 |
| `-o report.dot` | Graphviz 输出 |
| `--gandi-apikey X` | Gandi 集成 |
| `--aws-access-key X` | Route53 集成 |

## 攻击场景 Playbook

### DNS 委托链漏洞找接管

```bash
python3 trusttrees.py --domain target.com
# 发现 dangling NS 委托(子域可注册接管)→ 挂恶意站点钓鱼/偷 Cookie
```

## 注意事项

枚举 DNS 委托链并可视化,专找 dangling delegation 导致的子域接管面。
