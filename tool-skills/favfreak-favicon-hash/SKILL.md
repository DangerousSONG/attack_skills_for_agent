---
name: favfreak-favicon-hash
description: "FavFreak: group assets by same framework. Signals: asset mapping, subdomain, threads."
zh-signals: "FavFreak: 同框架资产归并。信号:资产测绘,子域名,线程。"
---

# FavFreak

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/devanshbatham/FavFreak
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/devanshbatham/FavFreak && cd FavFreak
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cat urls.txt | python3 favfreak.py` | favicon 哈希聚类 |
| `-o out.txt` | 输出 |
| `-t 20` | 线程 |

## 攻击场景 Playbook

### 同框架资产归并

```bash
cat subs.txt | httpx -silent | python3 favfreak.py
# murmurhash 聚类,同 CMS 资产一键归组
```

## 注意事项

favicon murmurhash 聚类,快速识别同框架资产(管理后台/同 CMS 站点)。
