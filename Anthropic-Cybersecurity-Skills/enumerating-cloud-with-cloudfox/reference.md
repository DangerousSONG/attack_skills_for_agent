# enumerating-cloud-with-cloudfox — 详细参考（由 SKILL.md 拆分）

# Loot files contain ready-to-run follow-ups, e.g. aws s3 ls / ssm start-session lines
```
See `scripts/agent.py` to run a curated set of commands and summarize output files.

## Tools and Resources

| Resource | Purpose | Link |
|----------|---------|------|
| CloudFox GitHub | Source, releases, full command list | https://github.com/BishopFox/cloudfox |
| CloudFox docs/wiki | Per-command output explanations | https://github.com/BishopFox/cloudfox/wiki |
| Bishop Fox CloudFox blog | Design and usage walkthrough | https://bishopfox.com/blog/introducing-cloudfox |
| AWS CLI reference | Follow-up exploitation commands | https://docs.aws.amazon.com/cli/latest/reference/ |
| Pacu | Active exploitation after enumeration | https://github.com/RhinoSecurityLabs/pacu |

## OPSEC and Detection Considerations

CloudFox is read-only, but its enumeration is far from silent. Each command issues
many `Describe*`/`List*`/`Get*` API calls in a short burst, which is highly visible
to defenders:

- **CloudTrail** records every read call. A spike of `iam:ListUsers`, `iam:ListRoles`,
  `secretsmanager:ListSecrets`, `ec2:DescribeInstances`, and `sts:GetCallerIdentity`
  from one principal within seconds is a strong enumeration signal.
- **GuardDuty** finding types such as `Discovery:IAMUser/AnomalousBehavior` and
  `Discovery:S3/MaliciousIPCaller` can fire on this burst pattern.
- Defenders should baseline normal API-call rates per principal and alert on
  enumeration bursts, especially from new IPs/ASNs or newly created credentials.

For an authorized assessment, document the source IP and timestamp of CloudFox runs
so the blue team can correlate, and prefer running from an in-scope, attributable host.

## Recommended Operator Workflow

1. Run `all-checks` once to populate the full output directory.
2. Open `role-trusts` first — it reveals the assume-role graph for lateral movement.
3. Cross-reference `secrets` and `env-vars` for credentials that unlock new principals.
4. Use `endpoints` + `instances` to map externally reachable attack surface.
5. Feed confirmed assume-role / privesc candidates into Pacu for active exploitation.

## High-Value Command Reference

| Command | Why it matters |
|---------|----------------|
| `all-checks` | Runs the full enumeration battery with defaults |
| `role-trusts` | Maps assume-role paths — core for lateral movement/privesc |
| `endpoints` | Surfaces internet-reachable attack surface |
| `secrets` | Exposes credentials in Secrets Manager / SSM |
| `permissions` | Lists effective IAM permissions per principal |
| `instances` | EC2 with IPs and attached instance-profile roles |
| `access-keys` | Active access keys (potential credential targets) |

## Validation Criteria

- [ ] CloudFox installed and runs `cloudfox aws --help`
- [ ] Cloud credentials confirmed via `sts get-caller-identity` / `az account show`
- [ ] `all-checks` completed and output directory populated
- [ ] Internet-reachable endpoints and instances identified
- [ ] IAM principals, permissions, and role-trusts enumerated
- [ ] Exposed secrets located and documented
- [ ] Azure enumeration run (if Azure in scope)
- [ ] Loot files triaged for pivot opportunities
- [ ] Findings exported to a structured directory for reporting
- [ ] Enumeration confirmed to stay within authorized scope
