---
name: waymore-archive-urls
description: 渗透工具 skill:waymore 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 waymore 时使用。
---

# waymore

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/xnl-h4ck3r/waymore
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install waymore
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `waymore -i t.com` | Wayback+CC+OTX URL 收割 |
| `-i t.com -mode U` | 仅 URL |
| `-i t.com -oU out.txt` | 输出 |
| `-n 50000` | 上限 |

## 攻击场景 Playbook

### 历史 URL 全量收割

```bash
waymore -i corp.com -oU urls.txt
# 比 waybackurls 更全(含 CC/OTX),喂 dalfox
```

## 注意事项

xnl-h4ck3r 出品,Wayback/Common Crawl/AlienVault 三源 URL 提取,适合大规模资产。
