---
name: webanalyze-tech-fingerprint
description: webanalyze: 技术栈指纹识别(挑 CVE 用)。信号:资产测绘,子域名,批量技术栈识别,单目标,爬取页数。
---

# webanalyze

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/rverton/webanalyze
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/rverton/webanalyze@latest && webanalyze -update
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `webanalyze -hosts hosts.txt` | 批量技术栈识别 |
| `-host https://x.com` | 单目标 |
| `-crawl 3` | 爬取页数 |
| `-apps apps.json` | 自定义指纹库 |
| `-output csv` | CSV 输出 |

## 攻击场景 Playbook

### 技术栈指纹识别(挑 CVE 用)

```bash
httpx -l subs.txt -silent | webanalyze -hosts - -output csv
# 按指纹过滤: grep -i 'wordpress\|jenkins\|shiro' tech.csv
```

## 注意事项

Wappalyzer 的 Go 移植版,适合大规模指纹批扫;识别出的组件直接映射漏洞库。
