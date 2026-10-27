---
name: metafinder-docs
description: MetaFinder: 文档元数据+泄露文件收集。信号:资产测绘,子域名,搜目标文档,文件类型,输出目录。
---

# MetaFinder

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/Josue87/MetaFinder
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install metafinder
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `metafinder -d target.com -l 20` | 搜目标文档 |
| `-t pdf,docx` | 文件类型 |
| `-o out` | 输出目录 |

## 攻击场景 Playbook

### 文档元数据+泄露文件收集

```bash
metafinder -d corp.com -t pdf,docx,xls -l 50
# 搜索引擎搜到的目标文档: 元数据(作者/软件)泄露+敏感文件名
```

## 注意事项

从搜索引擎批量扒目标文档;元数据里的用户名是社工/爆破的好料。
