---
name: exposure-risk-quantification
description: "FAIR 对齐的暴露风险量化:发现项打成 0-100/A-F 分与美元损失估算、所有权降权、攻击路径放大、董事会一页纸报告。信号:风险量化,fair,风险评分,攻击路径,董事会报告。"
when-to-use: "FAIR-aligned exposure quantification: turns a pile of recon findings into a defensible 0-100 + A-F org risk score (Likelihood x Impact, three ownership-aware factors: exposure/threat/impact), an owne
version: 1.0
sources: asm_reference_impl, ibm_ponemon, public_research
triggers:
  - risk score
  - risk quantification
  - cyber risk quantification
  - CRQ
  - FAIR methodology
  - FAIR score
  - loss event frequency
  - loss magnitude
  - risk grade
  - letter grade risk
  - A-F grade
  - 0-100 risk score
  - board report
  - board deliverable
  - board ready
  - executive summary risk
  - CISO report
  - hero number
  - dollar exposure
  - breach cost estimate
  - loss estimate
  - annualized loss expectancy
  - ALE
  - per-record cost
  - IBM Ponemon
  - cost of a data breach
  - exposed record count
  - quantify risk
  - risk translation
  - attack path
  - kill chain
  - shared fate exposure
  - attack path amplification
  - ownership confidence
  - proof demotion cap
  - confidence cap
  - TENTATIVE inflate score
  - risk trend
  - risk delta
  - the ask
  - remediation ask
  - one-pager
  - exposure risk
  - business impact translation
  - dominant risk driver
---

# Exposure Risk Quantification — FAIR Scoring, $-Loss, and the Board Deliverable

> Companion skill: `osint-methodology` (the "how to think" recon skill — see its §9 severity
> rubric and §16 client deliverable templates). This skill is the "how to quantify and
> present" layer on top of a finished recon pass: it takes findings the methodology skill's
> pipeline already produced and turns them into a number a board will act on.

## 0. When to Use / When NOT

**Use this skill when:** you have a completed set of recon findings (from any engagement,
not just one tool's output) and need to (a) compute a defensible 0–100 + A–F risk score,
(b) estimate a $-denominated loss range, (c) rank attack-path chains by exploitability, or
(d) assemble a board/exec one-pager. Also use it to *explain* a score — "why did this grade
come out D and not F" is exactly what §7 is for.

**Do NOT use this skill when:** you still need to go collect findings — that's
`osint-methodology` (methodology) / `offensive-osint` (arsenal). This skill does not probe
anything; it has nothing to say until a recon pass has already produced findings, assets,
and (ideally) ownership/proof annotations.

---

## 1. Posture: Passive Analysis, Not New Recon

Every computation in this skill is a **pure function over findings + assets you already
hold** — no network calls, no new probes, no target traffic. The reference implementation
(`reporting/{risk_score,loss_model,board_report,board_render,attack_paths,
attack_graph,owner_confidence,proof}.py`) is explicit about this: `risk_score.py` docstring
calls itself "Pure compute over `scan.db` — no network, no schema change"; `loss_model.py`
calls itself "Pure, no network"; `attack_graph.py` calls itself "Pure + offline."

That means this skill inherits the authorization posture of whatever collected the inputs
(see `osint-methodology` §1) but adds none of its own — quantifying findings you already
lawfully hold is never itself an intrusive act. It also means the outputs are only as good
as the inputs: garbage findings (unowned namesakes, unverified snippet matches) produce a
garbage score unless you apply the demotion cap in §7.5 first.

---

## 2. Confidence Levels

Reuses `osint-methodology` §2 verbatim — every finding you're about to score already
carries one of:

| Level | Meaning |
|---|---|
| **TENTATIVE** | Plausible, unverified. |
| **FIRM** | Directly observed, uncorroborated. |
| **CONFIRMED** | Multiple independent corroborations OR directly verified. |

What this skill adds is a second, orthogonal axis — **ownership certainty** — and the rule
for how the two combine so neither one alone can inflate a number (§7.5).

---

## 3. Output Format

Three artifacts, each a pure dataclass with a `to_dict()`:

```
OrgRisk:
  risk: float            # 0-100 headline
  grade: str              # A|B|C|D|F
  exposure, breach_likelihood, impact: float   # the three factors x100
  dominant_driver: str    # "exposure" | "breach-likelihood" | "business-impact"
  narrative: str          # 2-3 sentence board-language explanation

LossEstimate:
  records: int
  low, expected, high: float     # $ range
  annualized: float | None
  basis: str              # human-readable "N records x $X/record (source)" string

BoardSummary:
  target, hero (HeroNumbers), top_findings[], top_paths[], the_ask[], methodology, narrative
```

**Rule: every number ships with its basis.** `LossEstimate.basis` and `OrgRisk.narrative`
are not optional decoration — never present the bare `risk` float or `expected` dollar
figure without the sentence that explains what drove it. §4 and §12 make this a hard rule,
not a style preference.

---

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
