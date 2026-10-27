---
name: pymeta-metadata
description: pymeta: 文档元数据收割。信号:邮箱收集,员工信息,文档元数据提取,类型。
---

# pymeta

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/m8sec/pymeta
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install pymeta3
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `pymeta -d corp.com` | 文档元数据提取 |
| `-d domain -f pdf,docx` | 类型 |
| `-o out.txt` | 输出 |
| `-e 50` | 上限 |

## 攻击场景 Playbook

### 文档元数据收割

```bash
pymeta -d corp.com
# 作者/软件/路径泄露内网信息
```

## 注意事项

搜索引擎+元数据提取,文件 OSINT 工具。
