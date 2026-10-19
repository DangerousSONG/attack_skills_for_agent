---
name: dvcs-ripper-vcs
description: 渗透工具 skill:dvcs-ripper 的安装、参数速查与攻击场景 playbook。当任务涉及 供应链与CI/CD攻击 需要调用 dvcs-ripper 时使用。
---

# dvcs-ripper

- 攻击大类:C12 供应链与CI/CD攻击
- 上游仓库:https://github.com/kost/dvcs-ripper
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/kost/dvcs-ripper && cd dvcs-ripper
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `rip-git.pl -v -u https://t.com/.git/` | 远程 .git 下载+还原 |
| `rip-svn.pl -u URL/.svn/` | SVN |
| `rip-hg.pl -u URL/.hg/` | Mercurial |
| `rip-bzr.pl` | Bazaar |

## 攻击场景 Playbook

### 泄露的 .git 全量还原

```bash
./rip-git.pl -v -u https://target.com/.git/
git log --oneline  # 翻历史提交找密钥;checkout 早期版本比对
```

## 注意事项

.git/.svn 暴露=源码+历史+密钥全泄露;比 githack 支持更多 VCS 且处理不完整下载。
