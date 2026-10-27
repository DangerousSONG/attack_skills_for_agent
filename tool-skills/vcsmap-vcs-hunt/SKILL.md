---
name: vcsmap-vcs-hunt
description: vcsmap: 代码仓库暴露发现。信号:攻击面,云资产,版本控制仓库发现,平台。
---

# vcsmap

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/melvinsh/vcsmap
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install vcsmap
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `vcsmap scan corp` | 版本控制仓库发现 |
| `scan org -g github,gitlab` | 平台 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 代码仓库暴露发现

```bash
vcsmap scan corp
# github/gitlab/bitbucket 搜敏感仓库
```

## 注意事项

多平台代码仓库发现。
