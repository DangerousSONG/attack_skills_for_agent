---
name: pwndora-network-map
description: pwndora: 企业网段资产图谱。信号:网络拓扑,互联网测绘,大规模网络测绘。
---

# pwndora

- 攻击大类:C04 网络拓扑与互联网测绘
- 上游仓库:https://github.com/alechilczenko/pwndora
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/alechilczenko/pwndora && cd pwndora
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 main.py -t 10.0.0.0/16` | 大规模网络测绘 |
| `-t cidr -o out.json` | 输出 |
| `-p top1000` | 端口 |
| `-v` | 详细 |

## 攻击场景 Playbook

### 企业网段资产图谱

```bash
python3 main.py -t 10.0.0.0/16
# 端口+banner+指纹识别+Web 标题
```

## 注意事项

大规模网络资产测绘,输出结构化 JSON。
