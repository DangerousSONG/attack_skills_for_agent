---
name: fav-up-favicon-lookup
description: 渗透工具 skill:Fav-up 的安装、参数速查与攻击场景 playbook。当任务涉及 网络拓扑与互联网测绘 需要调用 Fav-up 时使用。
---

# Fav-up

- 攻击大类:C04 网络拓扑与互联网测绘
- 上游仓库:https://github.com/pielco11/fav-up
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/pielco11/fav-up && cd fav-up && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 favUp.py -fw favicon.ico` | favicon 反查 IP |
| `-sc` | 同时查 Shodan/Censys |
| `-w targets.txt` | 批量 favicon |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 真实 IP 反查(favicon 哈希)

```bash
curl -s https://target.com/favicon.ico -o fav.ico
python3 favUp.py -fw fav.ico -sc  # hash 匹配 Shodan 上的同图标资产 → 源站 IP
```

## 注意事项

WAF/CDN 后源站定位三板斧之一(favicon 哈希/DNS 记录/证书透明度);配合 cloudmare 类工具验证。
