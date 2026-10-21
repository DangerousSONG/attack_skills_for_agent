# continuous-llm-red-teaming-with-promptfoo — 详细参考（由 SKILL.md 拆分）

# .github/workflows/llm-redteam.yml
name: LLM Red Team
on: [pull_request]
jobs:
  redteam:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm install -g promptfoo
      - name: Run red team (fails build on new vulns)
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: promptfoo redteam run --no-progress-bar
      - name: Export machine-readable results
        if: always()
        run: promptfoo redteam report --output results.json
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: redteam-report, path: results.json }
```

### 6. Track regressions over time
Persist `results.json` per run and compare attack-success-rate per plugin between releases. A rising rate for any OWASP LLM category is a regression to triage before release. Promptfoo's `--filter-failing` lets you re-run only previously failing cases to confirm a fix.

```bash
promptfoo redteam run --filter-failing results.json
```

## Tools and Resources

| Resource | Link |
|----------|------|
| Promptfoo red-team docs | https://www.promptfoo.dev/docs/red-team/ |
| Promptfoo red-team configuration | https://www.promptfoo.dev/docs/red-team/configuration/ |
| Promptfoo CI/CD integration | https://www.promptfoo.dev/docs/integrations/ci-cd/ |
| Promptfoo MITRE ATLAS mapping | https://www.promptfoo.dev/docs/red-team/mitre-atlas/ |
| DeepTeam (Confident AI) | https://github.com/confident-ai/deepteam |
| DeepTeam docs | https://www.trydeepteam.com/docs/getting-started |
| OWASP Top 10 for LLM Applications | https://genai.owasp.org/ |

## Plugin / Strategy Reference

| Promptfoo item | Type | Maps to |
|----------------|------|---------|
| `owasp:llm` | preset | OWASP LLM Top 10 suite |
| `owasp:agentic` | preset | OWASP Agentic threats |
| `prompt-extraction` | plugin | LLM07 system-prompt leakage |
| `pii:direct` | plugin | LLM06 sensitive-info disclosure |
| `harmful` | plugin | harmful content generation |
| `jailbreak` / `jailbreak:composite` | strategy | AML.T0054 LLM jailbreak |
| `crescendo` | strategy | multi-turn jailbreak |
| `prompt-injection` | strategy | AML.T0051 prompt injection |

## Validation Criteria

- [ ] `promptfooconfig.yaml` created with target, `owasp:llm`, and `owasp:agentic` plugins.
- [ ] Jailbreak and prompt-injection strategies enabled.
- [ ] `promptfoo redteam run` executes and produces a per-plugin pass/fail report.
- [ ] DeepTeam suite runs against the same target via `model_callback`.
- [ ] CI/CD job fails the build on new red-team failures (non-zero exit).
- [ ] `results.json` artifact archived per run for regression tracking.
- [ ] Attack-success-rate per OWASP category trended across releases.
