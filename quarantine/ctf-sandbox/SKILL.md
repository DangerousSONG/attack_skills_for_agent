---
name: ctf-sandbox
description: Thin PRIMARY for CTF / AWD / lab range multi-type orchestration. Hands off to the sidecar CTF-Sandbox-Orchestrator. Use when the user says CTF, AWD, lab range, or competition challenge and no more specific pwn/APK/IDA route already won.
zh-signals: "CTF/AWD/靶场多类型编排的入口门闩，转交 CTF-Sandbox-Orchestrator 处理。信号:CTF,AWD,靶场,竞赛,pwn,沙箱编排"
when-to-use: "Use when the user mentions CTF, AWD, lab range, or a competition challenge and no more specific pwn/APK/IDA route applies."
---

# CTF sandbox entry (sidecar, not a second router)

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: Run `../scripts/case-init.ps1`; do not ACT against the real public Internet before `auth.status=granted`. Use `-NetworkProfile lab` or `offline` for competitions/lab ranges.
2. `NOW`: Open `../../CTF-Sandbox-Orchestrator/ctf-sandbox-orchestrator/SKILL.md` at the package root and continue under its sandbox assumptions.
3. `MUST NOT` write the 40+ `competition-*` sub-skills into `routing.json`. This entry point is only a single PRIMARY gate.
4. `ACT`: Let the orchestrator select one downstream `competition-*`. When the challenge type is already clear (pwn/ROP, APK, IDA), the earlier rule in `routing.json` should have won; do not compete for it again.

## Why a Separate Layer

`CTF-Sandbox-Orchestrator/` is a **GPL sidecar package** whose default authorization is confined to the sandbox. The core routing package remains MIT + the `scope.md` gate. This skill is only a keyword entry point and does not merge the competition tree into the core.

## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I go through case-init / scope first, instead of treating "the user said CTF" as authorized public-Internet access?
- [ ] Did I open the sidecar orchestrator instead of treating the 40 sub-skills as PRIMARY?
- [ ] If the task was really pwn/APK/IDA, did I let the more specific PRIMARY take over?
