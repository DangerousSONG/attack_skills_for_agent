---
name: assetfinder-quick-subs
description: assetfinder: 侦察流水线第一棒。信号:资产测绘,子域名,只列子域名,子域+关联域名,静默输出便于管道。
---

# assetfinder

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/tomnomnom/assetfinder
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/tomnomnom/assetfinder@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `assetfinder --subs-only target.com` | 只列子域名 |
| `assetfinder target.com` | 子域+关联域名 |
| `--silent` | 静默输出便于管道 |

## 攻击场景 Playbook

### 侦察流水线第一棒

```bash
assetfinder --subs-only corp.com | sort -u | tee subs.txt
subfinder -d corp.com -silent >> subs.txt && sort -u subs.txt -o subs.txt
```

## 注意事项

tomnomnom 出品的轻量件,速度快;与 subfinder 互补去重后送 dnsx。
