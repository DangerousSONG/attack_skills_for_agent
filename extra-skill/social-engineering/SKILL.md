---
name: social-engineering
description: "Personnel intelligence gathering and social engineering attack preparation for the target organization. Use when you need to collect target email formats, key personnel information, organizational structure, or prepare phishing attacks / watering hole attacks / credential guessing. Suitable for the social engineering preparation phase of a penetration test"
zh-signals: "收集目标组织的人员情报（邮箱格式、关键人员、组织架构），为钓鱼、水坑和凭据猜测等社工攻击做准备。信号:社会工程,邮箱收集,人员情报,组织架构,钓鱼准备"
when-to-use: >-
  Use when performing authorized social-engineering preparation against an
  organization — gathering email formats, key personnel, and org structure to plan
  phishing, watering-hole, or credential-guessing activities.
metadata:
  tags: "osint,social,email,people,phishing,social-engineering,mail,personnel,organization,phishing"
  category: "recon"
---

# Social Engineering Intelligence Gathering Methodology

> **⛔ Further Reading**: phishing email templates, pretexting scripts, credential guessing scripts, and watering hole attack techniques see `references/social-engineering-techniques.md`

The success rate of social engineering attacks depends on the quality of earlier reconnaissance. This skill focuses on intelligence gathering at the personnel and organizational level, providing ammunition for subsequent phishing / watering hole / credential guessing.

## Phase 1: Email Format Discovery
Use `http_request` or `curl` to query the Hunter API and search for email addresses associated with the target domain.

**Key objectives**:
- Determine email naming rules (e.g. `first.last@`, `f.last@`, `flast@`)
- Collect a list of known email addresses (for later phishing or password spraying)
- Identify generic mailboxes (`info@`, `hr@`, `support@`) — usually shared by several people, easier to compromise

## Phase 2: Organization Information Gathering
Use `http_request` or `curl` to query the FOFA API and search for assets associated with the target domain, focusing on:

**Internal system exposure**:
- OA/ERP systems → leaks organizational structure
- VPN portals → remote work entry points
- Mail systems (OWA/Zimbra) → credential attack targets
- HR/recruiting systems → leaks job posting and tech stack information
- Wiki/Confluence → may host knowledge bases without authentication

**Information leak checks**:
- Document metadata (author names, internal paths in PDF/Word files)
- Public GitHub/GitLab repositories (search the organization name or domain)
- Job postings leaking the tech stack ("familiar with Spring Boot + MySQL")

## Phase 3: Key Personnel Identification
Prioritize identifying the following roles (ordered by social engineering value):
1. **IT administrators** — hold system privileges, technical emails easier to forge
2. **HR/administrative staff** — used to opening attachments (resumes, contracts, etc.)
3. **Finance staff** — common BEC (business email compromise) targets
4. **Executives** — CEO/CFO identities can be used for internal phishing
5. **New employees** — unfamiliar with internal processes, easier to deceive

## Phase 4: Social Engineering Attack Plan
Based on the collected intelligence, evaluate feasible attack directions:

| Attack Type | Prerequisites | Success Rate |
|----------|----------|--------|
| Phishing email | Has email list + email format | High |
| Password spraying | Has email list + login entry point | Medium |
| Watering hole attack | Knows the sites the target frequently visits | Medium |
| Credential guessing | Has personnel names + email format | Low-Medium |
| Phone social engineering | Has org structure + key personnel | Scenario dependent |

## Notes
- Use `evidence_save` to save key findings (email lists, personnel information) for later use
- Social engineering intelligence has a shelf life; personnel may leave or change roles
- Tag every information source with its confidence level (search engine / official site / speculation)

## Target Selection
- Role ranking: select targets by priority (IT admin > regular employee)

## Password Pattern Guessing
- Common patterns: company name + year (2026), season, and other time-dependent values
- Mind the account lockout policy (lockout), it usually locks after 5 attempts
