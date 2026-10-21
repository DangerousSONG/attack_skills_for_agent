---
name: gowitness-screenshot
description: 渗透工具 skill:gowitness 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 gowitness 时使用。
when-to-use: 渗透工具 skill:gowitness 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 gowitness 时使用。
---

# gowitness

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/sensepost/gowitness
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/sensepost/gowitness@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `gowitness scan --url https://target.com` | 单 URL 截图+指纹 |
| `file -f urls.txt --threads 20` | 批量截图 |
| `server` | 启动结果浏览服务 |
| `report export -f csv` | 导出报告 |

## 攻击场景 Playbook

### 资产可视化核查(先看脸再决定打谁)

```bash
naabu -host target.com -top-ports 1000 | httpx | gowitness file -f - --threads 30
gowitness server  # 浏览器翻截图挑管理后台
```

## 注意事项

Chrome headless 截图入库(SQLite),配 httpx 管道效果最佳。
