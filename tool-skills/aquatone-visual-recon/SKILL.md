---
name: aquatone-visual-recon
description: 渗透工具 skill:Aquatone 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Aquatone 时使用。
---

# Aquatone

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/michenriksen/aquatone
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/michenriksen/aquatone@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cat hosts.txt | aquatone` | 管道输入批量截图 |
| `-ports large` | 端口集(xlarge/large/medium/small) |
| `-out ./aquatone` | 输出目录 |
| `-scan-timeout 90000` | 扫描超时 |
| `-screenshot-timeout 30000` | 截图超时 |

## 攻击场景 Playbook

### 域名飞越式可视化核查

```bash
cat subdomains.txt | aquatone -out report -ports large
# report/aquatone_report.html 按响应相似度聚类,一眼挑管理台
```

## 注意事项

按响应体相似度聚类分组,适合海量子域快速筛目标;项目维护放缓但功能稳定。
