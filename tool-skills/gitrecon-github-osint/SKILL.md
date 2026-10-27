---
name: gitrecon-github-osint
description: GitRecon: GitHub 组织信息收集。信号:资产测绘,子域名,token。
---

# GitRecon

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/GONZOsint/gitrecon
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/GONZOsint/gitrecon && cd gitrecon && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python gitrecon.py -s target` | 按用户/组织搜 GitHub |
| `-t X` | token |

## 攻击场景 Playbook

### GitHub 组织信息收集

```bash
python gitrecon.py -s targetcorp -t $GITHUB_TOKEN
# 员工账号/repos/gists/事件全列,盯密钥泄露
```

## 注意事项

GitHub 账户级 OSINT;盯组织成员的 public gists 是密钥泄露重灾区。
