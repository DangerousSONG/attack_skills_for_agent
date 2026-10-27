---
name: ccrawldns-commoncrawl
description: ccrawldns: CommonCrawl 数据源利用。信号:资产测绘,指纹识别。
---

# ccrawldns

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/ghostlulzhacks/ccrawldns
- 上游 License:NOASSERTION(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ghostlulzhacks/ccrawldns
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python ccrawldns.py -t target.com` | 从 CommonCrawl 提子域/URL |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### CommonCrawl 数据源利用

```bash
python ccrawldns.py -t corp.com
# CommonCrawl 免费索引,含 Wayback 没有的新站
```

## 注意事项

CommonCrawl 是常被忽略的被动数据源;与 gau/waybackurls 三源齐下。
