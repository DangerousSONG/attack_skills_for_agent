---
name: gasmask-osint-all
description: GasMask: 域名/人名/公司多模式 OSINT。信号:资产测绘,指纹识别,全量 OSINT,子域,github。
---

# GasMask

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/twelvesec/gasmask
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/twelvesec/gasmask && cd gasmask && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python gasmask.py -d target.com -A` | 全量 OSINT |
| `-s` | 子域 |
| `-g` | github |
| `-t` | twitter |
| `-b` | shodan |

## 攻击场景 Playbook

### 域名/人名/公司多模式 OSINT

```bash
python gasmask.py -d corp.com -A  # DNS/子域/邮箱/whois/GitHub/Shodan 汇总
```

## 注意事项

twelvesec 出品的多模式 OSINT 聚合;支持按公司名/人名查。
