---
name: pagodo-dorks
description: "Batch GHDB vulnerability fingerprint dorks. Signals: asset mapping, subdomains, rate limiting, concurrency."
zh-signals: "pagodo: GHDB 漏洞指纹 dork 批跑。信号:资产测绘,子域名,限速,并发。"
when-to-use: "Use during asset mapping and reconnaissance to batch-run Google Hacking Database dorks against a target domain and surface exposed files, leaks, and vulnerable fingerprints. Requires a target domain, a dork list, and rate-limiting/concurrency settings."
---

# pagodo

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/opsdisk/pagodo
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/opsdisk/pagodo && cd pagodo && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python pagodo.py -d target.com -g dorks.txt` | Run a GHDB dork set |
| `-l` | Rate limiting |
| `-j 20` | Concurrency |

## Attack Scenario Playbook

### Batch-running GHDB vulnerability fingerprint dorks

```bash
python pagodo.py -d corp.com -g ~/pagodo/all_google_dorks.txt -j 10
# Run 4000+ vulnerability/leak dorks against the target; the results are potential findings
```

## Notes

Ships with the entire Google Hacking Database; the results can be used directly as a vulnerability lead list.
