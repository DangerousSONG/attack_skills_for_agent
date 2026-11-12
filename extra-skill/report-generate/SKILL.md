---
name: report-generate
description: "Penetration test report generation. Use when a security assessment is complete and a formal report must be produced. Covers the report structure template, risk rating criteria (CVSS), vulnerability description style, and remediation recommendation standards. Suitable for formal penetration test reports and red team assessment reports"
zh-signals: "生成正式渗透测试与红队评估报告，涵盖结构模板、CVSS 评级与修复建议。信号:报告生成,渗透测试报告,CVSS,风险评级,修复建议,模板"
when-to-use: "Use when a security assessment is complete and a formal penetration test or red team report needs to be produced."
metadata:
  tags: "report,summary,documentation,penetration test report,risk rating,remediation recommendation"
  category: "general"
---

# Penetration Test Report Generation Methodology

The report is the final deliverable of a penetration test — however powerful the attack, if the report is poorly written the client cannot understand it, which means the work was wasted.

## Data Collection

First collect all the data you already have:
- `get_store_stats` — overall statistics
- `evidence_list` (filter by type) — asset inventory
- `list_vulns` — vulnerability list
- `evidence_list` + `evidence_read` (filter for credential types) — credentials (redacted before being put into the report)

## Report Structure Template

### 1. Executive Summary (1 page, for management)
Summarize in non-technical language:
- Assessment scope and timeline
- **One-sentence conclusion**: what the overall security posture looks like (e.g. "3 critical vulnerabilities were found, allowing an attacker to gain full control of the server remotely")
- Key numbers: asset count, vulnerability count (distribution by severity)
- The most urgent action items

### 2. Scope and Methodology
- Target list (domains/IPs/applications)
- Test type (black box/gray box/white box)
- Methodologies and tools used
- Limitations (time, out-of-scope exclusions)

### 3. Findings Overview
Vulnerability statistics chart:
```
Critical: ■■ 2
High: ■■■ 3
Medium: ■■■■■ 5
Low: ■■■ 3
Info: ■■■■■■ 6
```

### 4. Vulnerability Details (the core section)
Describe each vulnerability with the following structure:

**[Critical] SQL Injection — user search feature**
- **Location**: `https://target.com/search?q=`
- **Description**: the search parameter is not filtered and is concatenated directly into the SQL query, allowing an attacker to read/modify/delete database content
- **Impact**: all user data (including password hashes) can be obtained, server files can be read
- **Steps to reproduce**:
  1. Visit `https://target.com/search?q=' OR 1=1--`
  2. The page returns all records (normally only matching items should be returned)
  3. Use `UNION SELECT` to extract the users table
- **Remediation recommendation**: use parameterized queries (Prepared Statement), never concatenate SQL strings

### 5. Risk Rating Criteria
Use CVSS 3.1 or a simplified version:

| Severity | CVSS | Typical scenario |
|------|------|----------|
| Critical | 9.0-10.0 | RCE, SQL injection to obtain a shell, complete authentication bypass |
| High | 7.0-8.9 | Sensitive data exposure, privilege escalation, arbitrary file read |
| Medium | 4.0-6.9 | Stored XSS, CSRF, information disclosure |
| Low | 0.1-3.9 | Reflected XSS, directory listing, version disclosure |
| Info | 0 | Security configuration recommendations, best practice deviations |

### 6. Remediation Priority
Sort by remediation urgency:
1. **Fix immediately**: critical and high severity vulnerabilities
2. **Fix on plan**: medium severity vulnerabilities (next release)
3. **Improve when possible**: low and informational severity

### 7. Appendix
- Tool list and versions
- Detailed testing timeline
- Raw scan data (optional)

## Writing Principles
- **Reproducible**: a technical reader should be able to verify the reproduction steps themselves; small PoCs can go in the reproduction steps, while longer PoCs go in the appendix and are referenced from the body
- **Understandable**: management should understand the risk after reading the executive summary; the impact of a vulnerability must land on business consequences rather than only technical jargon
- **Actionable**: remediation recommendations must be specific down to the code/configuration level
- **Not exaggerated**: describe risk objectively; do not raise the severity to look more important
- **Deliverable**: prefer PDF for the final delivery; do not make the editable Word/Markdown/LaTeX file the only deliverable
- Avoid subjective or emotional wording, stay professional

## Delivery Quality Checks

### Sensitive Information Redaction
- Irreversibly mask passwords, tokens, ID documents, personal photos, and customer data — avoid relying on semi-transparent blur alone
- Mask inside the image file before importing screenshots into the document; do not rely on Word overlay shapes, since the original image may still be stored inside the document package
- Keep only the necessary prefix and suffix of credentials for identification, e.g. `AKIA...ABCD`

### Screenshot Standards
- Keep only the minimum area of the screenshot that proves the vulnerability, ensuring commands, URLs, status codes, and key responses stay readable
- Avoid dark, transparent terminals; reports are often printed or compressed, and low-contrast screenshots get distorted
- Add a title or caption to every image and highlight the key evidence in it
- Command line screenshots should include the actual command; pure output screenshots make reproduction harder

### Document Hygiene
- Deduplicate and sort lists (by severity, domain, IP, port, or timeline)
- Avoid vague quantities such as "several" or "some" — quantify whenever possible
- Do not send client sensitive data to uncontrolled online LLMs; for writing assistance, prefer a local model or redact the data first
- Before delivery, check spelling, links, image clarity, table of contents, headers/footers, and whether the attachments are complete
