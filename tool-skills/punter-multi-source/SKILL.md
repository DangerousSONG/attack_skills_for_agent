---
name: punter-multi-source
description: Punter: 多源被动子域聚合。信号:资产测绘,子域名,被动子域收集,含主动验证。
---

# Punter

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/nethunteros/punter
- 上游 License:Unlicense(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nethunteros/punter && cd punter && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python punter.py -t target.com` | 被动子域收集 |
| `-a` | 含主动验证 |

## 攻击场景 Playbook

### 多源被动子域聚合

```bash
python punter.py -t corp.com  # DNSDumpster/WhoisXML/证书透明度聚合
```

## 注意事项

免 API key 聚合多源;适合做资产初版底稿。
