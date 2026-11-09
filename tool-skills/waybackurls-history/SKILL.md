---
name: waybackurls-history
description: "waybackurls: Historical URL harvesting. Signals: asset mapping, subdomains, with timestamps, without subdomains, waybackurls."
zh-signals: "waybackurls: 历史 URL 收割。信号:资产测绘,子域名,带时间戳,不含子域,waybackurls`。"
---

# waybackurls

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/tomnomnom/waybackurls
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/tomnomnom/waybackurls@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `waybackurls corp.com` | 拉 Wayback 全部 URL |
| `-dates` | 带时间戳 |
| `-no-subs` | 不含子域 |
| `cat domains.txt | waybackurls` | 批量 |

## 攻击场景 Playbook

### 历史 URL 收割

```bash
echo corp.com | waybackurls | sort -u > urls.txt
grep -Ei 'login|admin|token|key' urls.txt  # 敏感端点优先测
```

## 注意事项

tomnomnom 出品的被动数据源管道件;与 gau 互补,两边都跑减少遗漏。
