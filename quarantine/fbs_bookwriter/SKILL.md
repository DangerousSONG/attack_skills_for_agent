---
name: fbs_bookwriter
description: "FBS Fu helper long-form document writing: the full workflow for books/manuals/whitepapers/long-form reporting; driven by Node scripts for intake, session resume, S/P/C/B quality checks and MD/HTML delivery. Enable when the user mentions writing a book, publishing a book, chapters, outline, source material, quality checks, export, expansion, or exiting and saving."
zh-signals: "FBS 福帮手长文档写作技能，通过 Node 脚本驱动书稿的 intake、会话恢复、质检与 MD/HTML 交付。信号:长文档写作,写书,章节大纲,质检,导出"
when-to-use: "Use when the user wants to write a book, manual, whitepaper, or long-form report and needs intake, outline, chapter writing, quality checks, or MD/HTML delivery."
homepage: https://clawhub.ai/skills/fbs-bookwriter
metadata:
  openclaw:
    skillKey: fbs_bookwriter
    requires:
      bins: ["node", "npm"]
---

# FBS-BookWriter (OpenClaw packaged version)

> **Upstream version**: 2.1.2 (same source as the `FBS-BookWriter` repository)  
> **Adaptation target**: the [OpenClaw](https://docs.openclaw.ai/tools/creating-skills) skill model: `SKILL.md` + `metadata.openclaw` (snake_case `name`, `skillKey` used for `skills.entries` / agent allowlist in `openclaw.json`).

This directory is the **OpenClaw-specific entry point**: decoupled from the WorkBuddy / CodeBuddy **marketplace channel** (the published package does **not** contain `workbuddy/`, `codebuddy/`, `.codebuddy-plugin/`), while still keeping the complete `references/`, `scripts/`, `scene-packs/`, `assets/` and `package.json`, making it convenient to invoke the same Node toolchain via **shell/exec** inside the Gateway.

**Cognitive asset and commercial positioning (consistent with the main repository)**: the value proposition is uniformly phrased as "evolvable, distributable, value-adding"; capability layering is uniformly phrased as "scene packs + premium packs + offline/online membership". Machine-readable form is in the root `fbs-runtime-hints.json` → `cognitiveAsset`; the first-response JSON is at `firstResponseContext.cognitiveAssetSnapshot`. See [`references/05-ops/cognitive-asset-threeization.md`](./references/05-ops/cognitive-asset-threeization.md) for details.

---

## Installation (OpenClaw)

**Install from ClawHub (recommended, requires publication):** in a logged-in environment run `openclaw skills install fbs-bookwriter` or `npx clawhub@latest install fbs-bookwriter`, then run `npm install` in the skill root. See [fbs-bookwriter on ClawHub](https://clawhub.ai/skills/fbs-bookwriter) for the list and version.

1. Put the skill root directory (folder name recommended as **`fbs_bookwriter`**, matching `name`) into any scan path, for example:
   - Workspace: `./skills/fbs_bookwriter/` (highest priority)
   - Or `~/.openclaw/workspace/skills/fbs_bookwriter/`
   - Or `~/.openclaw/skills/fbs_bookwriter/`
   - Or add the parent directory to `skills.load.extraDirs` in `~/.openclaw/openclaw.json`  
   See [Skills](https://docs.openclaw.ai/tools/skills) and [skills-config](https://docs.openclaw.ai/tools/skills-config) (`load.watch` hot-reloads skill snapshots by default).
2. Run the dependency installation once in the skill root:  
   `npm install` (Node ≥18; optional dependencies cover HTML/Docx, etc., see `package.json` `optionalDependencies`).
3. Restart the session or run `openclaw gateway restart` / `/new` in chat, and confirm the load with `openclaw skills list`.

---

## OpenClaw Host Differences (relative to WorkBuddy)

| Capability | WorkBuddy | OpenClaw (this package) |
|------|-----------|-------------------|
| Entry display | `intake-router --json` + host consumes `userFacingOneLiner` | Runs the same script to get JSON; show the user **only** the one-line summary given by the script + at most 3 options; do not dump the full text |
| Execution command | host bash / terminal | Use OpenClaw **exec / shell**; **cwd must be the skill root** (containing `package.json` and `scripts/`) |
| Search | host `web_search` | Use the **web search / browser** provided by OpenClaw (if enabled); if unavailable, fall back offline per `search-policy` and the scripts |
| File tools | `list_dir` / `read_file` / `search_file` | **Do not** probe files inside `.fbs/` by searching only on file names (some environments do not index dot directories); for `.fbs/workbuddy-resume.json`, `esm-state.md`, etc., **`read_file` the known path** or **`list_dir`** the book root to confirm `.fbs` exists |
| Marketplace manifest | `workbuddy/channel-manifest.json` etc. | **Not included in this package**; does not affect the scripted writing main chain |

---

## Execution Quick Reference (every session)

1. **Unified entry point (mandatory)** (`bookRoot` is the absolute path to the user's manuscript root):

   ```bash
   node scripts/intake-router.mjs --book-root "<bookRoot>" --intent auto --json --enforce-required
   ```

   Add `--full` to the command only when the full online scene pack is needed (it may be slow).
   If the JSON returns `projectAnchor.status=ambiguous`, first have the user confirm the project root path, then rerun with the confirmed `--book-root`; do not read any `.fbs/*` content before confirmation.

2. **Resume**: prefer **`read_file`** of `<bookRoot>/.fbs/workbuddy-resume.json`; if absent, read `chapter-status.md` or enter the S0.5 guide. Do not use "search the whole repo by file name" as a substitute for an existence check.

3. **Exit**: when the user says to exit, ask softly first, then execute:

   ```bash
   node scripts/fbs-cli-bridge.mjs exit -- --book-root "<bookRoot>" --json
   ```

   The reply must include the **`userMessage`** from the script JSON (the session is recorded and can be continued next time).

4. **Stages and gates**: read `.fbs/esm-state.md` before advancing a stage; S3.5 expansion requires a user-confirmed `.fbs/expansion-plan.md` first, and the expansion word count must be measured with `node scripts/expansion-word-verify.mjs` or `expansion-gate.mjs` (pure model estimation is forbidden).
   When the user says "continue", apply the advance-priority thresholds: when the S0 material count reaches "track count×2", S2 has chapter titles + target word counts, and S3 has ≥3 completed chapters, prioritize proposing the next stage.
   Before advancing S0→S1, you may run `node scripts/s0-exit-gate.mjs --book-root "<bookRoot>" --json --confirm-advance` as a mandatory gate check.

5. **Writing constraints**: serial execution first; by default modify at most **2** files per round; see [`references/05-ops/agent-task-strategy.md`](./references/05-ops/agent-task-strategy.md).
   Back up the source file before expansion/polishing: `node scripts/source-write-backup.mjs --book-root "<bookRoot>" --scope expansion --json` (`expansion-gate` backs up automatically by default).
   When entering the S3.7 polishing step, run `node scripts/polish-gate.mjs --book-root "<bookRoot>"` first (back up before quality checking) to avoid bypassing the gate and editing the manuscript directly.
   Before delivery closure, run `node scripts/release-governor.mjs --book-root "<bookRoot>"`, which automatically keeps a single final manuscript and archives old versions.
   Before external delivery, run `node scripts/material-marker-governor.mjs --book-root "<bookRoot>" --fix` to clean up the pending-verification MAT marker and the `[DISCARDED-*]` markers.
   Before publishing the full manuscript/final manuscript/final-reviewed manuscript, you must run `node scripts/final-manuscript-clean-gate.mjs --book-root "<bookRoot>"`; if process markers are detected, delivery is not allowed.
   Any "completed/passed" conclusion must be backed by script evidence (the command or output path); verbal claims alone are forbidden.

---

## Intent → Script (Excerpt)

The complete table is in the **WorkBuddy version `SKILL.md` mirror** shipped alongside this package at the repository root, or in [`references/01-core/intake-and-routing.md`](./references/01-core/intake-and-routing.md).

| Scenario | Command |
|------|------|
| Initialize the writing studio | `node scripts/init-fbs-multiagent-artifacts.mjs --book-root "<bookRoot>"` |
| Environment preflight | `node scripts/env-preflight.mjs` (see the script's `--help` for parameters; includes `glob`/`iconv-lite` dependency checks) |
| Chapter merging / health snapshot / consistency audit | `merge-chapters.mjs`, `book-health-snapshot.mjs`, `consistency-audit.mjs`, etc. (`--book-root` / `--skill-root` pointing to the corresponding root) |
| CLI bus | `node scripts/fbs-cli-bridge.mjs help` |

---

## Output Format

- To the user: short status + actionable next step (≤3 items), avoiding leakage of internal specification clauses and complete JSON.
- When mentioning a term/file name, add a sentence on "purpose + value" (e.g. `chapter-status.md` = the progress ledger, valuable because it avoids missing chapters and duplicated writing).
- Files on disk: `<bookRoot>/.fbs/`, `deliverables/`, `releases/` are the source of truth; see [`references/01-core/skill-full-spec.md`](./references/01-core/skill-full-spec.md).

---

## Error Handling

- **Node/script failure**: explain the failing step to the user; if only an optional dependency is missing, suggest `npm install` or skip the non-essential feature.
- **Manuscript root not ready**: guide the user to run `init-fbs-multiagent-artifacts` first, or take the S0 minimal set (see the script-unavailable fallback section in [`references/01-core/intake-and-routing.md`](./references/01-core/intake-and-routing.md)).
- **Sandbox without environment variables**: if OpenClaw runs in a Docker sandbox without the host `env` injected, configure `sandbox.docker.env` for the agent in `openclaw.json` or disable the sandbox (see the official skills-config documentation).

---

## Authoritative Documentation Index

- General specification: [`references/01-core/skill-full-spec.md`](./references/01-core/skill-full-spec.md)  
- Workflow: [`references/01-core/section-3-workflow.md`](./references/01-core/section-3-workflow.md)  
- NLU: [`references/01-core/section-nlu.md`](./references/01-core/section-nlu.md)  
- Runtime contract: [`references/01-core/runtime-mandatory-contract.md`](./references/01-core/runtime-mandatory-contract.md)

---

*OpenClaw packaging maintenance notes: kept in sync with the `pack:openclaw` output; `metadata.openclaw.skillKey` and the directory name `fbs_bookwriter` should be aligned so that `skills.entries` can be configured.*
