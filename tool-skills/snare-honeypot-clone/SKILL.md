---
name: snare-honeypot-clone
description: SNARE: 克隆目标站钓鱼。信号:web漏洞,注入,起蜜罐,克隆站点,联动 Tanner 判定。
---

# SNARE

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/mushorg/snare
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install snare
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `snare --port 8080 --host-ip 0.0.0.0` | 起蜜罐 |
| `snare --clone https://t.com` | 克隆站点 |
| `--tanner tanner.mushmush.org` | 联动 Tanner 判定 |

## 攻击场景 Playbook

### 克隆目标站钓鱼

```bash
snare --clone https://login.t.com --port 443
# 镜像登录页+记录凭据,配合 DNS 劫持
```

## 注意事项

蜜罐/站点克隆工具,高保真复刻任意站点。
