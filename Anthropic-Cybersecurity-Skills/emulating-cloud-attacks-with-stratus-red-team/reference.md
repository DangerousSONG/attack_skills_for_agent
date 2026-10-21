# emulating-cloud-attacks-with-stratus-red-team — 详细参考（由 SKILL.md 拆分）

### 6. Validate the detection
Confirm your SIEM/detection fired. Example: query Athena/CloudTrail or check GuardDuty findings.
```bash
aws guardduty list-findings --detector-id "$DETECTOR_ID" \
  --finding-criteria '{"Criterion":{"updatedAt":{"GreaterThanOrEqual":'"$(date -d '-1 hour' +%s)"'000}}}'
```

### 7. Revert side effects to re-detonate
Undo the detonation while keeping prerequisites so you can iterate on a detection.
```bash
stratus revert aws.credential-access.ec2-steal-instance-credentials
stratus detonate aws.credential-access.ec2-steal-instance-credentials   # run again
```

### 8. Clean up all infrastructure
Tear down everything a technique created. Always finish here.
```bash
stratus cleanup aws.credential-access.ec2-steal-instance-credentials
# Nuke everything Stratus ever provisioned in this account
stratus cleanup --all
stratus status   # confirm COLD state for all techniques
```

### 9. Drive it programmatically for coverage runs
Loop over a tactic to measure detection coverage, then clean up. See `scripts/agent.py`.
```bash
python scripts/agent.py --platform aws --tactic credential-access --detonate --cleanup
```

## Tools and Resources

| Resource | Purpose | Link |
|----------|---------|------|
| Stratus Red Team GitHub | Source, releases, technique source | https://github.com/DataDog/stratus-red-team |
| Stratus Red Team docs | Technique catalog and lifecycle reference | https://stratus-red-team.cloud |
| Attack technique list | Full per-platform technique IDs | https://stratus-red-team.cloud/attack-techniques/list/ |
| MITRE ATT&CK Cloud | Tactic/technique reference for mapping | https://attack.mitre.org/matrices/enterprise/cloud/ |
| Atomic Red Team | Complementary endpoint emulation | https://github.com/redcanaryco/atomic-red-team |

## Detection-Validation Mapping

For purple-team value, pair each detonation with the telemetry and detection it should trigger:

| Technique | Expected telemetry | Detection to validate |
|-----------|--------------------|-----------------------|
| `aws.credential-access.ec2-steal-instance-credentials` | CloudTrail use of role creds from a non-EC2 IP | GuardDuty `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration` |
| `aws.persistence.iam-create-admin-user` | `CreateUser` + `AttachUserPolicy` (AdministratorAccess) | CloudTrail/Sentinel rule on admin-policy attach |
| `aws.exfiltration.ec2-share-ebs-snapshot` | `ModifySnapshotAttribute` sharing to external account | GuardDuty `Exfiltration:EC2/...` / custom rule |
| `aws.discovery.ec2-enumerate-from-instance` | Burst of `Describe*` from instance role | Enumeration-burst detection |

After detonation, confirm the alert fired end-to-end (source -> SIEM -> ticket). If it
did not, you have found a coverage gap; document it before cleaning up.

## Cost and Safety Notes

- Some techniques provision billable resources (EC2 instances, EBS snapshots). Always
  run `stratus cleanup --all` and verify `stratus status` returns COLD.
- Never run Stratus with production credentials; use a dedicated lab account/subscription.
- The state directory `~/.stratus-red-team/` holds Terraform state — preserve it until
  cleanup completes, or you may strand resources.

## Lifecycle State Reference

| State | Meaning |
|-------|---------|
| COLD | No prerequisites provisioned; nothing to clean up |
| WARM | Prerequisites provisioned but not yet detonated |
| DETONATED | Attack actions performed; side effects present |

## Validation Criteria

- [ ] Stratus installed and `stratus list` returns the technique catalog
- [ ] Target cloud identity confirmed via `sts get-caller-identity` / equivalent
- [ ] Technique inspected with `stratus show` before detonation
- [ ] Warmup completed and status shows WARM
- [ ] Detonation completed and status shows DETONATED
- [ ] Generated telemetry located in CloudTrail/GuardDuty/SIEM
- [ ] Detection rule confirmed to fire (or coverage gap documented)
- [ ] Technique reverted and re-detonated to confirm repeatability
- [ ] `stratus cleanup --all` run and status returns COLD for every technique
- [ ] No orphaned billable resources remain in the account
