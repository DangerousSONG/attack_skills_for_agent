---
name: php-vuln-scanner
description: "PHP component version vulnerability detection tool. Scans composer.json / composer.lock or jar/package metadata, matches known vulnerability rules, and outputs a report (including a framework for likely trigger-point analysis)."
zh-signals: "扫描 PHP 项目 Composer 依赖并匹配已知漏洞规则，输出 CVE/Advisory 报告与触发点分析。信号:PHP漏洞扫描,Composer依赖,CVE,依赖审计,漏洞报告"
when-to-use: "Use when you need to scan a PHP project's composer.json or composer.lock for known vulnerable dependencies and produce a vulnerability report with likely trigger points."
---

# PHP Dependency Vulnerability Scanner (php-vuln-scanner)

Scan Composer dependencies of PHP projects, identify known security vulnerabilities (CVE/Advisory), and provide a correlation inference framework against routes/entry points.

## Input
- `source_path`: source code root directory

Supported targets:
- `composer.json`
- `composer.lock`
- Directory recursion (find composer.lock under multiple submodules)

## Rules and Output
- Rule matching: use built-in/external rule sets (e.g. `references/php-vulnerability.yaml`, preferred if it exists)
- Output to:
```
{output_path}/vuln_report/
  {project_name}_composer_vuln_report_{timestamp}.md
```

## Scan Workflow (Required)

> **Cross-validation recommendation**: if `composer audit` can be executed in the project environment, it is recommended to cross-compare its output against this skill's rule matching results to improve CVE coverage. `composer audit` uses the live Packagist advisory database and can supplement the timeliness blind spots that may exist in this skill's built-in rule set. Take the union of both as the final vulnerability list.

1. Dependency enumeration
   - Parse composer.lock to obtain package names and versions
   - When handling multiple modules, output results grouped by module
2. Vulnerability matching
   - Match affected version ranges against known CVE rules
3. Trigger point analysis (framework)
   - Identify the functional domains where known high-risk components may be reached: routing entry points, serialization/templates, upload/download, authentication chains
   - Recommend using `php-route-mapper` to output routes, then perform "affected route inference"
4. Component-to-route correlation inference (required, the pipeline cannot be driven without it)
   - Input dependencies: read `routes_{timestamp}.md` and `params_{timestamp}.md` (consistent with `shared/IO_PATH_CONVENTION.md`; when written independently they are usually the same-named files under `route_mapping/`; when the pipeline is merged, read the equivalent section of the consolidated report)
   - Evidence priority:
     1) The component's class/function referenced directly in the code (e.g. `use Vendor\\Pkg\\{value}`, `new {value}`, `Vendor\\{value}::`)
     2) Identify the functional domain of the component through template/serialization/upload/network-related "known integration points" (then look up the route in reverse)
     3) Naming-based inference alone is the fallback: it must be marked as `⚠️To be verified`
   - For each vulnerable component output:
     - The code reference locations of the component (file path + function/class name; if there is no line number write "to be located" but still give the file path)
     - The sink functional domains the component may trigger (SQL/TPL/DESER/FILE/UPLOAD/SSRF/XSS/AUTH, etc.)
     - Inferred affected routes/entry points (must list every route entry, omissions are forbidden; each entry must give both the `route_id` and the route string so it can be fed back directly to `php-route-tracer`)

## Output Report Structure (Mandatory)
```markdown
# {project_name} - Composer Component Vulnerability Scan Report
Generated at: {timestamp}
Analysis path: {source_path}

## Risk Statistics
(classified by Critical/High/Medium/Low, omissions are forbidden)

## Vulnerability Details (list each one)
=== [CVE-xxxx-xxxx] {component} {version} ===
- Affected versions:
- Current version:
- Severity:
- Possible trigger points (inference framework):
- Code reference locations (evidence):
  - File: path/to/xxx.php
  - Evidence: function/class/call snippet (must give the minimum locatable snippet)
- Affected routes/entry points (combined with route-mapper, give the "inference rationale"):
- Route list (list each one, omissions are forbidden): (must give both the `route_id` and the route string)
- Inference rationale (must state clearly which evidence priority 1/2/3 was used)
- Remediation recommendation:
```

## Key Component Trigger Point Matrix (Mandatory: used to drive pipeline stage 3)
| Component | Rule/Affected Severity | Corresponding sink Functional Domain | Affected Route/Entry Point Count | Affected Routes/Entry Points (list each one) | Evidence Level (direct reference/functional domain/to be verified) |

