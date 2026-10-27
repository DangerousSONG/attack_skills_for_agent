---
name: witnessme-web-shot
description: WitnessMe: Web 资产整段截图。信号:屏幕捕获,截图,单 URL 截图,批量,起 Web 服务看结果。
---

# WitnessMe

- 攻击大类:C34 截图与取证
- 上游仓库:https://github.com/byt3bl33d3r/WitnessMe
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install witnessme
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `witnessme snapshot -t https://t.com` | 单 URL 截图 |
| `witnessme snapshot -f urls.txt` | 批量 |
| `witnessme server -p 8080` | 起 Web 服务看结果 |
| `--no-http` | 仅 HTTP(S) |

## 攻击场景 Playbook

### Web 资产整段截图

```bash
cat subdomains.txt | witnessme snapshot -f -
# 生成带缩略图的 Web 面板,报告用
```

## 注意事项

byt3bl33d3r 出品,headless Chrome 批量网页截图+服务端展示,Web 攻击面可视化。
