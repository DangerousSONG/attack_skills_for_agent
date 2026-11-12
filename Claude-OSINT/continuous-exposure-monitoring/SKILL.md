---
name: continuous-exposure-monitoring
description: "Turns one-time external recon into continuous monitoring: scheduled diff scans, six-source adversary intelligence, watchlist matching, finding lifecycle state machine, alert pacing. Signals: continuous monitoring, exposure monitoring, attack surface diff, intelligence monitoring, alert fatigue."
zh-signals: "把一次性外部侦察升级为持续监控:定时重扫diff、六源对抗情报监控、watchlist匹配、发现生命周期状态机与告警节奏控制。信号:持续监控,暴露面监控,攻击面diff,情报监控,告警疲劳。"
when-to-use: >-
  Turns one-shot external recon into a continuous monitoring program. Covers the scheduled re-scan-and-diff loop (baseline snapshot -> interval sleep -> re-scan -> asset/finding delta -> threshold-gate
version: 1.0
sources: asm_reference_impl, public_research
triggers:
  - continuous monitoring
  - continuous exposure monitoring
  - retainer monitoring
  - MSSP monitoring
  - scheduled rescan
  - scheduled scan
  - scan diff
  - diff scans
  - monitor a target
  - monitor continuously
  - re-scan and diff
  - delta alert
  - alert on delta
  - drift detection
  - attack surface drift
  - perimeter drift
  - what changed since last scan
  - ransomware leak site monitoring
  - leak site monitoring
  - adversary chatter
  - dark web monitoring
  - brand mention monitoring
  - IAB monitoring
  - paste site monitoring
  - telegram brand monitoring
  - CTI feed
  - threat intel feed
  - chatter watchlist
  - retroactive rescan
  - infrastructure tracking over time
  - certificate transparency monitoring
  - CT log monitoring
  - passive DNS deltas
  - new subdomain alert
  - typosquat monitoring
  - typosquat surveillance
  - finding lifecycle
  - false positive triage
  - risk accepted
  - finding suppression
  - alert fatigue
  - durable alert delivery
  - alert outbox
  - retry backoff
  - finding SLA
  - overdue finding
  - cron recon
  - scheduled task recon
  - monitoring cadence
  - fleet monitoring
  - cross-scan tracking
  - queued vs delivered
---

# Continuous Exposure Monitoring — Loop, Diff, Chatter, Lifecycle

> Companion skills: [`osint-methodology`](../osint-methodology/) (the 5-stage pipeline this skill
> loops — see its §7.2 "ongoing weekly diff" profile, which this skill fills in with concrete
> mechanics), [`offensive-osint`](../offensive-osint/) (§29 Threat Intel & IOCs — this skill
> **deepens** that section's advisory/IOC-feed directory with the continuous adversary-chatter
> watch loop and CTI-feed cadence it explicitly lacks; use §29 for indicator enrichment and
> vulnerability-prioritization data sources, this skill for the standing collection loop),
> [`org-attack-surface`](../org-attack-surface/) (the org-first discovery this skill's re-scans
> re-run on a schedule), [`exposure-risk-quantification`](../exposure-risk-quantification/) (reads
> this skill's finding-lifecycle suppression state to compute `risk_trend` and the FAIR score — see
> its risk-score model). This skill answers a different question than all four: not "what does the
> target expose right now," but **"is what the target exposes changing, and should anyone be told."**

## 0. When to Use / When NOT

**Use this skill when:**

- Standing up ongoing monitoring for a retainer, MSSP, or bug-bounty program instead of a one-shot
  engagement — the client wants to know about *new* exposure, not to re-read yesterday's report.
- Deciding how often to re-run which recon stage (daily vs. weekly vs. monthly) without either
  wasting API quota / detection budget on cheap-to-skip stages or missing real drift.
- Building or tuning adversary-chatter monitoring (ransomware leak sites, forum/paste mentions,
  Telegram brand mentions) for a target's brand/domain.
- Deciding whether a finding that keeps showing up in every re-scan should keep alerting, or has
  already been triaged/accepted and should go quiet.
- Debugging "the webhook never fired" or "the webhook fired twice" — alert delivery reliability,
  dedup, and backoff behavior.
- Writing a "what changed on the perimeter since last week" deliverable.

**Do NOT use this skill when:**

- You need the one-shot discovery methodology itself — that's `osint-methodology` (5-stage
  pipeline) and `offensive-osint` (the per-technique arsenal). This skill assumes discovery already
  happened at least once and is about the *second and every subsequent* run.
- You need a new active-intrusion technique. This skill is a scheduling, diffing, and alerting
  layer over recon that is already authorized and already running — see §5.
- The target's authorization isn't established, or a **recurring** cadence hasn't been explicitly
  agreed — see §1's monitoring-specific authorization note.

---

## 1. Authorization & Legal Posture

Same base posture as the companion skills: intended for assets the operator owns or has **written
authorization** to assess — see `osint-methodology` §1 for the full soft-scope-check script.

**The monitoring-specific nuance:** a point-in-time engagement authorization does not automatically
cover an indefinite recurring cadence. Before standing up a `monitor`/`chatter watch` daemon or a
dashboard-scheduled job against a target, confirm the authorization window explicitly covers the
monitoring period (retainer end date, RoE renewal terms), not just "the engagement." A scheduled job
that outlives its authorization is a standing violation, not a one-off mistake — it fires every
interval until someone notices and tears it down.

**Always-on guardrail specific to this skill:** a monitoring loop must never silently escalate its
own authorization tier. The `monitor` CLI command's flag surface only exposes `--only`/`--exclude`
module filters — it has no path to enable `--validate` (the credential/token-submission tier), so a
scheduled `asm-cli monitor` loop cannot accidentally re-arm that tier. The dashboard job
scheduler is different: a job's `flags` field accepts the same flags a manual scan does, so an
operator *can* configure a recurring job with `--validate`/`--validate-creds` set. Treat that as a
standing-authorization decision that needs its own explicit sign-off, not a monitoring-cadence
decision — see §5.

---

## 2. Confidence Levels

Same three-tier scale as the companion skills — **TENTATIVE / FIRM / CONFIRMED** — answers "how sure
am I this is real." This skill adds one axis that is easy to conflate with confidence and must not
be:

**Confidence is not lifecycle status.** A chatter hit can be HIGH severity and still TENTATIVE
confidence (adversary-controlled content is always TENTATIVE by design — see §7.6). A finding can be
CONFIRMED confidence and still be `risk_accepted` in the lifecycle (§9) — the client acknowledged a
*real* exposure and chose to keep it. Never let a severity or confidence label imply anything about
whether a human has already triaged the finding, and never let a lifecycle status imply anything
about whether the underlying evidence was independently verified. They are orthogonal axes recorded
in different places (the Finding's `confidence` field vs. `finding_lifecycle.status`).

---

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
