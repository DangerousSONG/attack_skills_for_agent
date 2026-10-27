# Attack Skills for Agent · 攻击侧 Skills 集（989 个 · 1k 达成）

> 面向渗透测试 Agent 的即插即用 SKILL.md 能力库。每个 skill 是一个标准化 SKILL.md 文件（frontmatter + 方法论 + 命令 + 攻击链），Agent 按需加载。
>
> **逐条明细见 [INDEX.md](INDEX.md)**：989 个 skill 按 50 个攻击大类全量列出。
>
> ⚠️ 仅限授权安全测试使用（authorized security testing only）。

## 口径

- 攻击侧 only：已剔除无线/硬件（WiFi/蓝牙/SDR/固件/IoT）、纯防御（检测/狩猎/取证响应/加固合规/ZTNA/PAM/IDS）、纯逆向与恶意软件分析
- 跨仓库按 Skill 名称去重，与 mukul975/Anthropic-Cybersecurity-Skills 内部及其余各源零重名
- License 全部开源可二创：Apache-2.0 / MIT / CC BY 4.0（CC BY 内容需署名，见下）
- v1.1 更新：ACS 误伤复议回收 8 个 + 新增 blockint-skills / ctf-skills / awesome-ai-security 三源 20 个（低质量与合规/筛查类目录已剔除）
- v1.9 口径定稿：blockint 移出；MERGES 20 团裁决（13 并/7 不并）再减 13；新增 gadget 决策表 + 纪律元技能 2 个 → 总量 989（现成 435 + 改写 554），仍满足 1k 指标口径
- v2.0 两层部署：990 个 skill 全量注册时每个 step 的 system 区注入约 20K tokens，实验实测 prompt cache 命中率 84.9% → 14.8%，成本放大 3.9 倍 → 改为「3 个注册 + 987 个文件库」两层模型

## 部署（两层模型 · v2.0）

**背景**：v1 把 990 个 skill 全部注册进 agent 的 skills 目录，每个 step 的 system 区都要携带全量 name/description 索引（约 20K tokens）。实测 prompt cache 命中率从 84.9% 跌到 14.8%，token 成本放大 3.9 倍。v2.0 改为两层：

| 层 | 位置 | 内容 | 加载方式 |
| --- | --- | --- | --- |
| 注册层（走 Skill 协议） | `/root/.claude/skills/` | 3 个：`attack-skill-router`（路由主表，13KB）、`engagement-discipline`（纪律元技能）、`java-deserialization-gadget-selector`（gadget 决策表） | Agent 原生 skill 索引 |
| 文件库（走 Read） | `/opt/attack-skill-library/` | 987 个 skill，扁平 `<slug>/SKILL.md`；库根放 `INDEX.md`（全量清单）+ `MERGES.md`（合并裁决） | Agent 按路由表用 Read 按需加载 |

**Agent 入口**：3 个注册 skill 常驻索引（<2K tokens/step）→ 路由表命中场景 → Read 打开 `/opt/attack-skill-library/<slug>/SKILL.md` 获取完整方法论与命令。

**部署命令**：

```bash
python scripts/deploy.py [--dry-run] [--clean] [--skills-dir 注册层目录] [--library-dir 文件库目录]
```

- 默认注册层 `/root/.claude/skills/`、文件库 `/opt/attack-skill-library/`，可用环境变量 `SKILL_LIBRARY` 覆盖文件库路径
- `--dry-run` 只打印不落盘；`--clean` 先清空目标再部署
- 文件库路径在路由表 / 注册层文本中以 `/opt/attack-skill-library` 为基准，换路径需同步改 `attack-skill-router/SKILL.md`

**质量门禁**：`python scripts/govern_skills.py`（frontmatter 校验、断链扫描含"未随库分发"豁免、路径存在性检查）。

## 来源分布（现成 435 = 10 个仓库 + 工具改写 554）

| 来源 | License | 数量 |
| --- | --- | ---: |
| mukul975/Anthropic-Cybersecurity-Skills | Apache-2.0 | 188 |
| yaklang/hack-skills | MIT | 95 |
| tmenov/Claude-Red-pentest-set | MIT | 59 |
| 0xSteph/pentest-ai-agents | MIT | 38 |
| hypnguyen1209/offensive-claude | MIT | 29 |
| elementalsouls/Claude-OSINT | MIT(代码)/CC BY 4.0(内容) | 7 |
| ljagiello/ctf-skills | MIT | 6 |
| gmh5225/awesome-web3-security | MIT | 5 |
| yaklang/yak-skills | MIT | 5 |
| gmh5225/awesome-ai-security | MIT | 3 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 | 2 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause(GhostPack)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 CC BY 4.0(署名)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0(数据库 GPL;脚本自行检查)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT(需Vulners API)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 WTFPL) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION(需人工)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 0BSD) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause(需人工确认)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT(内容库)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause(GhostPack)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 CC BY 4.0(署名)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION(需人工)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION(需人工)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION(需人工)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Unlicense) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION(Apache-2.0 为主)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 NOASSERTION) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AgPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Unlicense) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 WTFPL) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Zlib) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-4-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 CC BY-NC 4.0(非商业)) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 LGPL-2.1) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 ISC) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Unlicense) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 CC0-1.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 0BSD) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Unlicense) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-2-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 AGPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MPL-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 GPL-3.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 Apache-2.0) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 BSD-3-Clause) | 1 |
| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 MIT) | 1 |
| **合计** | | **989** |

注：blockint-skills（11 个区块链情报）已按需求移出；MERGES.md 20 个重叠团已裁决（13 并 / 7 不并），再减 13 个。

## 攻击大类分布（50 类全覆盖 · ATT&CK 骨架）

Top 12：C09 Web应用漏洞利用 176 · C01 资产测绘与指纹识别 62 · C10 API与业务逻辑攻击 54 · C30 AD域渗透与域控攻击 50 · C46 二进制漏洞利用与Pwn 47 · C42 网络扫描与枚举 40 · C50 红队方法论与自动化 38 · C40 嗅探与中间人攻击 37 · C25 哈希与密码破解 33 · C05 外部攻击面与云资产暴露 31 · C03 邮箱与人员OSINT 27 · C08 钓鱼与社会工程 25。

### 矩阵分布（大类 × 来源，50 类全量）

| 攻击大类 | 现成 Skill | 工具改写 Skill | 合计 |
| --- | ---: | ---: | ---: |
| C09 Web应用漏洞利用 | 72 | 99 | 171 |
| C01 资产测绘与指纹识别 | 14 | 48 | 62 |
| C10 API与业务逻辑攻击 | 40 | 14 | 54 |
| C30 AD域渗透与域控攻击 | 26 | 24 | 50 |
| C46 二进制漏洞利用与Pwn | 29 | 17 | 46 |
| C42 网络扫描与枚举 | 7 | 33 | 40 |
| C50 红队方法论与自动化 | 31 | 7 | 38 |
| C40 嗅探与中间人攻击 | 8 | 28 | 36 |
| C25 哈希与密码破解 | 5 | 28 | 33 |
| C05 外部攻击面与云资产暴露 | 17 | 14 | 31 |
| C03 邮箱与人员OSINT | 1 | 26 | 27 |
| C08 钓鱼与社会工程 | 15 | 10 | 25 |
| C07 载荷开发与武器化 | 12 | 12 | 24 |
| C49 密码学攻击 | 5 | 17 | 22 |
| C35 C2框架与远控 | 13 | 8 | 21 |
| C43 移动端攻击 | 14 | 7 | 21 |
| C02 域名与DNS侦察 | 4 | 15 | 19 |
| C22 进程注入与内存执行 | 18 | 1 | 19 |
| C41 Web漏洞扫描与验证 | 7 | 11 | 18 |
| C29 内网发现与枚举 | 0 | 17 | 17 |
| C12 供应链与CI/CD攻击 | 14 | 2 | 16 |
| C18 云与容器提权 | 11 | 3 | 14 |
| C06 漏洞情报与漏洞库 | 8 | 6 | 14 |
| C28 暴力破解与口令喷射 | 0 | 14 | 14 |
| C15 持久化与后门植入 | 9 | 4 | 13 |
| C31 远程服务横向移动 | 4 | 9 | 13 |
| C44 AI与大模型安全 | 9 | 3 | 12 |
| C17 Windows本地提权 | 5 | 6 | 11 |
| C04 网络拓扑与互联网测绘 | 3 | 7 | 10 |
| C32 隧道与内网穿透 | 2 | 8 | 10 |
| C45 恶意软件开发与免杀 | 0 | 9 | 9 |
| C26 Kerberos与票据攻击 | 5 | 3 | 8 |
| C16 Linux本地提权 | 4 | 4 | 8 |
| C13 远程命令执行与WebShell | 0 | 8 | 8 |
| C24 内存转储与LSASS窃取 | 2 | 3 | 5 |
| C48 区块链与Web3安全 | 4 | 1 | 5 |
| C27 本地凭证与浏览器窃取 | 4 | 0 | 4 |
| C33 数据收集与打包暂存 | 1 | 3 | 4 |
| C19 EDR与AV规避 | 4 | 0 | 4 |
| C11 边界设备与VPN攻击 | 2 | 2 | 4 |
| C47 逆向工程 | 1 | 3 | 4 |
| C20 反取证与痕迹清理 | 0 | 4 | 4 |
| C38 隐写与隐藏通道 | 0 | 4 | 4 |
| C39 数据破坏与擦除 | 2 | 1 | 3 |
| C34 屏幕与输入捕获 | 1 | 2 | 3 |
| C14 云与容器执行 | 0 | 3 | 3 |
| C36 隐蔽回连与通信通道 | 0 | 3 | 3 |
| C37 数据外传 | 1 | 1 | 2 |
| C23 无文件与LOLBins滥用 | 0 | 2 | 2 |
| C21 流量混淆与加密隧道 | 1 | 0 | 1 |
| **合计** | **435** | **554** | **989** |

逐条明细（1000 个 · 名称/来源/License/简介/可跳转链接）见 [INDEX.md](INDEX.md)

## 署名与许可

- 各目录内 LICENSE 文件为对应上游仓库原始许可，二次分发请遵守
- elementalsouls/Claude-OSINT 的 SKILL.md 内容以 CC BY 4.0 授权，二次使用须署名 **Sachin Sharma / Claude-OSINT** 并链接原仓库
- 其余仓库均以 Apache-2.0 / MIT 授权，可自由二创
