---
name: git-wild-hunt-secrets
description: git-wild-hunt: 公开仓库密钥泄露挖掘。信号:攻击面,云资产,批量,自定义规则。
---

# git-wild-hunt

- 攻击大类:C05 云资产发现
- 上游仓库:https://github.com/d1vious/git-wild-hunt
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/d1vious/git-wild-hunt && cd git-wild-hunt && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python git-wild-hunt.py -i https://github.com/org/repo` | GitHub 仓库密钥挖掘 |
| `-i repos.txt` | 批量 |
| `--regex custom.txt` | 自定义规则 |
| `-o out.json` | 输出 |

## 攻击场景 Playbook

### 公开仓库密钥泄露挖掘

```bash
python git-wild-hunt.py -i https://github.com/corp/web
# AWS key/密码/token 正则全扫,拿云凭据
```

## 注意事项

d1vious 出品,对 GitHub 仓库做全历史密钥扫描,正则覆盖主流云/服务凭据。
