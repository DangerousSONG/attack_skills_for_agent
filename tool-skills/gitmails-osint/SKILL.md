---
name: gitmails-osint
description: gitmails: 开发者邮箱收割。信号:攻击面,云资产,仓库提交者邮箱提取,深度。
---

# gitmails

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/mazen160/gitmails
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install gitmails
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `gitmails -u github.com/target` | 仓库提交者邮箱提取 |
| `-u url -d 3` | 深度 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 开发者邮箱收割

```bash
gitmails -u github.com/corp/internal-tool
# 员工邮箱+用户名
```

## 注意事项

git 仓库提交历史邮箱提取。
