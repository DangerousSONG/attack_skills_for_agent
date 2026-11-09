# Skill 底座同步规则（多方案分支协作）

> 本仓库有多个**方案分支**（外层方案不同），但**攻击 skill 底座只有一套**。本规则定义底座与方案层的边界，以及底座修改如何同步到所有方案分支。
>
> 生效日期：2026-11-09 ｜ 适用分支：main、rfc-audit-skills、static-router、flat-skills、song_1030

## 一、两层边界（先看这个）

**底座层（skill 本体，全分支必须一致）**——只允许在 `main` 上修改：

| 路径 | 说明 |
|---|---|
| `Anthropic-Cybersecurity-Skills/` | 攻击 skill 源目录 |
| `Claude-OSINT/` | 攻击 skill 源目录 |
| `Claude-Red-pentest-set/` | 攻击 skill 源目录 |
| `awesome-ai-security/` | 攻击 skill 源目录 |
| `awesome-web3-security/` | 攻击 skill 源目录 |
| `ctf-skills/` | 攻击 skill 源目录 |
| `hack-skills/` | 攻击 skill 源目录 |
| `offensive-claude/` | 攻击 skill 源目录 |
| `pentest-ai-agents/` | 攻击 skill 源目录 |
| `yak-skills/` | 攻击 skill 源目录 |
| `tool-skills/` | 攻击 skill 源目录（1000 skills 主力目录） |
| `extra-skill/` | 外部安全 skill 导入目录（1216 个，cfdba5f 起） |
| `INDEX.md` | 全库索引（由底座变更驱动重生成） |
| `攻击侧Skills清单.csv` | 清单数据 |

**方案层（各分支自由演进，互不同步）**：

| 路径 / 项 | 归属 |
|---|---|
| `attack-skill-router/` | router 方案（static-router / rfc-audit-skills / song_1030 各自演进） |
| `rfc-audit-skills/` | RFC 审计规则层方案 |
| `engagement-discipline/`、`java-deserialization-gadget-selector/` | meta/注册层 skill（flat-skills 方案明确移除，属方案层决策） |
| `README.md`、`SKILL-PLAN.md`、`SKILL-RESEARCH.md`、`SKILL-SOLUTION.md`、`CONTRIBUTING.md` | main 上的流程/规划文档；方案分支可自带自己的版本 |
| `scripts/` | 配套脚本（main 演进，方案分支不强制跟随） |

## 二、铁律

1. **底座唯一写入口是 main**。任何人（含方案分支开发中）要新增/修改/删除攻击 skill，一律先提交到 main（**入库流程按 [CONTRIBUTING.md](CONTRIBUTING.md)：regenerate_index → gen_router → export_csv 级联 + govern/eval 门禁全零**），再同步回方案分支；**禁止直接在方案分支改底座路径**。
2. **方案分支只做 merge，不做底座改写**。方案分支与 main 的合并冲突中，凡涉及底座路径，一律 `git checkout --ours origin/main` 取 main 版本，再把改动重做到 main 上。
3. **INDEX.md / 清单 CSV 跟随底座**。底座变更后重生成索引，与底座同 commit 进 main。
4. **方案层互不同步**。router 的改动不进入 flat-skills，rag 的文档不进入 rfc-audit-skills——除非方案主动 merge 对方（不推荐）。

## 三、同步机制（自动）

- GitHub Action `skill-base-sync`（见 `.github/workflows/skill-base-sync.yml`）：main 上底座路径有 push 时，自动向各方案分支开「sync: skill 底座同步 ← main」PR。
- PR 由方案分支负责人合并；合并冲突说明有人违反铁律 1/2，按第二节规则裁决。
- **Gitee（pjlab）镜像不运行 Action**：同步 PR 只在 GitHub 产生；推到 Gitee 靠日常 `git push` 双远端（origin 已配置双 push URL），如需 Gitee 自动同步可后续在 Gitee 侧配流水线。

## 四、日常工作流（同事无感版）

```bash
# 同事新增 attack skill（在任意工作区）：
git checkout main
# …新增/修改 tool-skills/xxx/SKILL.md…
git commit -m "feat: 新增 xxx 攻击 skill"
git push origin main          # 自动触发各方案分支的同步 PR

# 方案分支开发者（如 rfc-audit-skills）：
git checkout rfc-audit-skills
git merge origin/main         # 或直接合入自动 PR
```

## 五、遗留裁决记录

| 事项 | 裁决 | 理由 |
|---|---|---|
| flat-skills 移除 `engagement-discipline/`、`java-deserialization-gadget-selector/` | **维持移除，不算漂移** | 55c7540 系方案层决策（平铺部署模型去注册层），两目录属 meta/注册层而非底座 |
