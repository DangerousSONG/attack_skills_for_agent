---
name: waybackpack-archive
description: waybackpack: 历史快照取证。信号:资产测绘,指纹识别,列归档 URL,只列不下载,从 2015 年。
---

# waybackpack

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/jsvine/waybackpack
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install waybackpack
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `waybackpack target.com` | 列归档 URL |
| `--list` | 只列不下载 |
| `-d 2015` | 从 2015 年 |
| `--uniques-only` | 去重 |
| `-o dir` | 下载快照 |

## 攻击场景 Playbook

### 历史快照取证

```bash
waybackpack corp.com -d 2018 --uniques-only -o snapshots/
# 翻旧版页面找已下线的接口/注释里的密钥/硬编码地址
```

## 注意事项

把 Wayback 快照整体拉到本地比对历史变更;找'曾经暴露过的秘密'专用。
