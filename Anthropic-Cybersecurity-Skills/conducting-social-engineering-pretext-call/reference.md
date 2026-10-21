# conducting-social-engineering-pretext-call — 详细参考（由 SKILL.md 拆分）

### Pretext Checklist

- [ ] Is the pretext believable for this organization?
- [ ] Does it create appropriate urgency without being threatening?
- [ ] Does it align with OSINT findings (real dept names, real systems)?
- [ ] Does it have a plausible reason for requesting information?
- [ ] Is there a fallback if the target pushes back?
- [ ] Has the client approved this specific pretext?

## Phase 3: Call Execution

### Call Structure

1. **Introduction** (10 seconds): State name, department, reason for calling
2. **Building rapport** (30 seconds): Reference something real (recent event, shared context)
3. **Authority establishment** (20 seconds): Reference manager name, ticket number, urgency
4. **Information request** (30 seconds): Ask for the target information naturally
5. **Handling objections**: If challenged, respond calmly with prepared answers
6. **Closing** (10 seconds): Thank them, leave no suspicion

### Objection Handling

| Objection | Response |
|---|---|
| "Can I call you back?" | "Of course, call the main helpdesk line and ask for [name]. But this needs to be done by EOD." |
| "I need to verify this" | "Absolutely, I appreciate your diligence. You can check with [manager name]." |
| "I was told never to give passwords" | "You're right, and normally we wouldn't ask. This is a special case because [reason]. I can have my manager call you." |
| "What's your employee ID?" | Pivot: "It's [made-up ID]. Listen, I have 50 more people to call today. Can we just get this done?" |
| "I'll email IT instead" | "Sure, but the system migration happens tonight. If it's not done by then..." |

## Phase 4: Data Collection and Metrics

Track the following for each call:

| Metric | Description |
|---|---|
| Target Name | Employee called |
| Department | Target's department |
| Date/Time | When call was made |
| Duration | Length of call |
| Pretext Used | Which scenario |
| Information Obtained | What was disclosed |
| Credential Disclosed | Yes/No (and type) |
| Verification Attempted | Did target try to verify caller? |
| Reported to Security | Did target report the call? |
| Social Engineering Score | 1-5 susceptibility rating |

## Phase 5: Reporting

### Success Metrics

| Metric | Target | Result |
|---|---|---|
| Credential Disclosure Rate | <10% | XX% |
| Sensitive Info Disclosure Rate | <20% | XX% |
| Verification Rate | >80% | XX% |
| Security Reporting Rate | >50% | XX% |

## Ethical and Legal Considerations

1. **Always obtain written authorization** before conducting vishing tests
2. **Never use threatening language** or create genuine fear
3. **Document consent** and legal requirements for call recording
4. **Protect disclosed credentials** - immediately report to client
5. **Debrief targets** after the engagement if client approves
6. **Never publicly identify** specific employees who failed
7. **Comply with telecommunications laws** in your jurisdiction

## References

- Verizon DBIR 2025: 74% of breaches involve human element
- MITRE ATT&CK T1598: https://attack.mitre.org/techniques/T1598/
- Social Engineering Penetration Testing by Gavin Watson (Syngress)
- The Art of Deception by Kevin Mitnick (Wiley)
- NIST SP 800-50: Building an Information Technology Security Awareness and Training Program
