# 维护指南 · 新增 / 修改 Skill 标准流程

> 面向维护者：向本仓库新增、删除、修改 skill 时必须按本文流程执行，保证 INDEX.md / 路由表 / CSV 三处资产同步，不静默过期。

## 一、SKILL.md 格式要求（新增前自检）

| 项 | 要求 |
| --- | --- |
| 目录名 | 全库唯一 slug，小写字母/数字/连字符；与 frontmatter `name` **必须一致**（检索键 = 路径键） |
| frontmatter | `name` + `description` 必备；description ≤100 字、含中文信号词尾（`信号:xxx,xxx`），供 TF-IDF 检索命中 |
| 攻击大类 | tool-skills/ 下每个 SKILL.md 正文必须有 `- 攻击大类:Cxx 大类名` 一行；分类以 INDEX.md 为准 |
| 版权 | 注明上游仓库与上游 License；本仓库二创统一 Apache-2.0 |

现成来源（上游仓库）新增条目时，大类归属在 INDEX.md 中确定，不写 `- 攻击大类` 行也可以。

## 二、级联再生成（顺序不可乱）

```bash
python scripts/regenerate_index.py     # 1. INDEX.md 刷新（分类权威，新增条目在此入库）
python attack-skill-router/gen_router.py  # 2. 路由表两层重生成（主表 SKILL.md + 展开层 reference.md）
python scripts/export_csv.py           # 3. 攻击侧Skills清单.csv 重导出
```

- 只改了某条 description → 只需第 1 步（刷新 INDEX 里的简介）
- 新增/删除/改大类 → 三步全跑

## 三、质量验证（提交前必须全过）

```bash
python scripts/govern_skills.py   # 门禁: frontmatter/断链/描述长度 — 必须全零(100-400字警告也应清零)
python scripts/eval_recall.py     # 检索不回退: AFTER 的 Recall@5/@20 不得低于 BEFORE(HEAD)
```

- 门禁有 `!!` 或警告 → 先修再提交
- eval 回退 → 检查新/改 skill 的 description 信号词是否覆盖中文任务表述
- 高价值工具记得加入 `attack-skill-router/gen_router.py` 的 `FORCE_PRIMARY` 名单，否则可能挤不进主表 top5

## 四、部署到 Agent 环境

```bash
python scripts/deploy.py --dry-run   # 预演
python scripts/deploy.py             # 注册层(3个) → /root/.claude/skills/  文件库(993个) → /opt/attack-skill-library/
```

## 五、红线

1. **MERGES.md 是人工裁决产物**（20 团，13 并 7 不并），任何脚本不得覆盖；gen_router.py 已移除 MERGES 生成逻辑
2. 推送前跑 `git status`，不得带入 `scripts/_*` 临时文件（.gitignore 已屏蔽）
3. 口径数字（996 = 现成 435 + 改写 561）分散在 README / INDEX / 路由表 / deploy.py，改动总量后必须全文同步
