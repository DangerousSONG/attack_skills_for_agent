# red-teaming-llms-with-garak — 详细参考（由 SKILL.md 拆分）

### Phase 4: Probe an Arbitrary REST Endpoint
1. garak can target any HTTP API via a JSON generator spec. Create `rest.json`:
   ```json
   {
     "rest": {
       "RestGenerator": {
         "name": "my-llm-gateway",
         "uri": "https://llm.internal.example/v1/chat",
         "method": "post",
         "headers": { "Authorization": "Bearer $ENV_TOKEN", "Content-Type": "application/json" },
         "req_template_json_object": { "model": "internal-bot", "prompt": "$INPUT" },
         "response_json": true,
         "response_json_field": "$.output"
       }
     }
   }
   ```
2. Run garak against it:
   ```bash
   export ENV_TOKEN="..."
   python -m garak \
     --target_type rest \
     -G rest.json \
     --probes promptinject,dan \
     --report_prefix internal_gateway
   ```

### Phase 5: Run a Curated Config and Full Sweep
1. For repeatable assessments, pin everything in a YAML/JSON config and pass `--config`:
   ```bash
   python -m garak --config assessment.yaml
   ```
   ```yaml
   # assessment.yaml
   plugins:
     model_type: openai
     model_name: gpt-4o-mini
     probe_spec: promptinject,latentinjection,dan,leakreplay,xss,malwaregen
   run:
     generations: 5
     parallel_attempts: 8
   reporting:
     report_prefix: quarterly_llm_assessment
   ```
2. For an exhaustive sweep (slow, expensive) run all probes by omitting `--probes` entirely.

### Phase 6: Interpret the Hit-Rate Report
1. Read the terminal summary. Each row is `probe.Class  detector: PASS|FAIL  ok on N/M`. A FAIL with a low `ok` fraction means the model frequently produced the unsafe behavior — a high-severity finding.
2. Open the machine-readable report and aggregate failures:
   ```bash
   # Every attempt with detector verdicts is one JSON line
   jq -r 'select(.entry_type=="eval") | "\(.probe)\t\(.detector)\t\(.passed)/\(.total)"' \
     garak.<timestamp>.report.jsonl | sort
   ```
3. Open the generated `.report.html` in a browser for the formatted scorecard and per-probe breakdown.
4. Pull the actual successful attack strings from the hit log to use as proof-of-concept evidence.

### Phase 7: Mitigate and Re-Test
1. Apply a control (tighten the system prompt, add an input/output guardrail such as Llama Guard or LLM Guard, or change the model).
2. Re-run the identical probe set with a new `--report_prefix`.
3. Compare hit rates between runs to quantify risk reduction for the report.

## Tools and Resources

| Resource | Purpose | Link |
|----------|---------|------|
| NVIDIA/garak | Source, probe list, issues | https://github.com/NVIDIA/garak |
| garak documentation | CLI reference, generator configs | https://docs.garak.ai/ and https://reference.garak.ai/ |
| garak paper (arXiv:2406.11036) | Methodology and design | https://arxiv.org/abs/2406.11036 |
| OWASP Top 10 for LLM Applications | Risk taxonomy probes map to | https://genai.owasp.org/ |
| MITRE ATLAS | AML technique definitions | https://atlas.mitre.org/ |

## Probe Family Reference

| Probe family | Targets | OWASP LLM mapping |
|--------------|---------|-------------------|
| `promptinject` | Direct prompt injection | LLM01 |
| `latentinjection` | Indirect / hidden-context injection | LLM01 |
| `dan` | Jailbreak / guardrail bypass | LLM01 / safety |
| `leakreplay` | Training-data & prompt leakage | LLM02 / LLM07 |
| `encoding` | Encoding-based filter bypass | LLM01 |
| `xss` | Markdown/HTML exfiltration payloads | LLM02 |
| `malwaregen` | Malicious code generation | misuse |

## Validation Criteria

- [ ] garak installed and `garak --version` succeeds.
- [ ] Probes and detectors enumerated with `--list_probes` / `--list_detectors`.
- [ ] At least one probe run completed against the target with a `--report_prefix` set.
- [ ] `.report.jsonl`, `.report.html`, and `garak.log` produced and located.
- [ ] Per-probe hit rates extracted and ranked by severity.
- [ ] Successful attack strings captured from the hit log as evidence.
- [ ] A mitigation applied and a comparison re-run completed showing changed hit rates.
- [ ] Findings documented against OWASP LLM Top 10 and MITRE ATLAS for the risk assessment.
