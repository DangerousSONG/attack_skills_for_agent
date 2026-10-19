---
name: waybackurls-history
description: 渗透工具 skill:waybackurls 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 waybackurls 时使用。
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
