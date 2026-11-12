---
name: oa-system-attack
description: "Exploitation of domestic Chinese OA/intranet systems. Use when domestic OA systems such as Seeyon, Weaver/E-cology, Yonyou/NC/U8, Landray, Tongda, Ezoffice, Kingdee, or iOffice are discovered in an intranet. Covers the typical vulnerabilities, default credentials, and RCE paths of each system. These appear very frequently in Chinese HW/CTF intranet environments, so this skill must be used"
zh-signals: "国产 OA 与内网系统漏洞利用技能，覆盖致远、泛微、用友、蓝凌、通达、万户等系统的默认口令与 RCE 路径。信号:OA漏洞,致远,泛微,用友,RCE,内网"
when-to-use: "Use when encountering domestic OA or intranet systems such as Seeyon, Weaver, Yonyou, Landray, Tongda, Ezoffice, Kingdee, or iOffice during internal engagements or competitions, to exploit their known vulnerabilities, default credentials, and RCE paths."
metadata:
  tags: "oa,seeyon,weaver,ecology,yonyou,nc,landray,tongda,ezoffice,kingdee,intranet,domestic-system,office-system"
  category: "lateral"
---

# Exploitation of Domestic OA/Intranet Systems

Chinese CTF intranet environments almost always contain OA systems—they have many historical vulnerabilities, a low patch rate, and typically high privileges.

## ⛔ Further Reading (Must Read)

- Detailed exploitation of Seeyon/Weaver/Yonyou → [references/oa-exploits.md](references/oa-exploits.md)
- Detailed exploitation of Tongda/Landray/other systems → [references/oa-exploits-more.md](references/oa-exploits-more.md)

---

## Phase 1: OA System Identification

```bash
# Web fingerprinting
whatweb http://TARGET
curl -sI http://TARGET | grep -i "Server"
curl -s http://TARGET | grep -iE "seeyon|weaver|ecology|yonyou|tongda|landray|ezoffice"

# Common path fingerprints
curl -s http://TARGET/seeyon/           # Seeyon OA
curl -s http://TARGET/weaver/           # Weaver E-cology
curl -s http://TARGET/mobile/           # Weaver E-mobile
curl -s http://TARGET/ispirit/          # Tongda OA
curl -s http://TARGET/sys/             # Landray OA
curl -s http://TARGET/portal/          # Yonyou NC
```

## Phase 2: System → Vulnerability Quick Reference

### Seeyon OA — the most vulnerabilities

| Vulnerability | Path | Type |
|------|------|------|
| Session leak | /seeyon/thirdpartyController.do | arbitrary user login |
| File upload | /seeyon/htmlofficeservlet | RCE |
| Deserialization | /seeyon/autoinstall.do.css | RCE |
| SSRF | /seeyon/ajax.do | SSRF |
| SQL injection | /seeyon/webmail.do | SQLi |

### Weaver OA (E-cology) — the most frequently encountered

| Vulnerability | Path | Type |
|------|------|------|
| SQL injection | /mobile/browser/WorkflowCenterTreeData.jsp | SQLi |
| File upload | /weaver/bsh.servlet.BshServlet | RCE |
| SSRF | /ssrf/proxy | SSRF |
| Database configuration read | /mobile/DBconfigReader.jsp | information disclosure |
| Command execution | /api/integration/workflowToDoc | RCE |

### Yonyou NC — usually high privileges

| Vulnerability | Path | Type |
|------|------|------|
| Deserialization | /servlet/~ic/bsh.servlet.BshServlet | RCE |
| File upload | /servlet/FileReceiveServlet | arbitrary file upload |
| Path traversal | /NCFindWeb | information disclosure |
| SSRF | /servlet/~uap/nc.itf.iufo.FunctionServlet | SSRF |

### Tongda OA — an entry-level target

| Vulnerability | Path | Type |
|------|------|------|
| File upload + inclusion | /ispirit/im/upload.php + /ispirit/interface/gateway.php | RCE |
| Arbitrary user login | /logincheck_code.php | authentication bypass |
| SQL injection | /general/approve_center/archive/getTableInfo.php | SQLi |

### Landray OA — SSRF to RCE

| Vulnerability | Path | Type |
|------|------|------|
| SSRF → RCE | /sys/ui/extend/varkind/custom.jsp | RCE |
| Arbitrary file read | /sys/ui/extend/varkind/custom.jsp | file read |
| Deserialization | /sys/search/sys_search_main/sysSearchMain.do | RCE |

→ Detailed payloads → references

## Phase 3: Generic Attack Strategy

```
After discovering an OA system:
1. Confirm the system type and version
2. Try default credentials
3. Look up known CVEs / Ndays
4. nuclei scan: nuclei -u TARGET -tags oa,seeyon,weaver,tongda
5. Manually verify high severity vulnerabilities (RCE > file upload > SQLi > information disclosure)
6. After obtaining a shell, collect intranet credentials
```

### Default Credential Quick Reference
| System | Username | Default password |
|------|--------|---------|
| Seeyon OA | system | system |
| Seeyon OA | admin | seeyon123456 |
| Weaver OA | sysadmin | 1 |
| Yonyou NC | admin | admin |
| Tongda OA | admin | admin00 |
| Landray OA | admin | admin |
