---
name: performing-sca-dependency-scanning-with-snyk
description: "Implements Software Composition Analysis (SCA). Signals: supply chain, CI/CD, pipeline attacks."
zh-signals: "This skill covers implementing Software Composition Analysis (SCA) using 信号:供应链,cicd,流水线攻击。"
when-to-use: 'This skill covers implementing Software Composition Analysis (SCA) using
  Snyk to detect vulnerable open-source dependencies in CI/CD pipelines. It addresses
  scanning package manifests and lockfiles, automated fix pull request generation,
  license compliance checking, continuous monitoring of deployed applications, and
  integration with GitHub, GitLab, and Jenkins pipelines.

  '
domain: cybersecurity
subdomain: devsecops
tags:
- devsecops
- cicd
- sca
- snyk
- dependency-scanning
- secure-sdlc
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- GV.SC-07
- ID.IM-04
- PR.PS-04
mitre_attack:
- T1195
- T1554
- T1059.004
---

# Performing SCA Dependency Scanning with Snyk

## When to Use

- When applications use open-source packages that may contain known vulnerabilities
- When compliance requires tracking and remediating vulnerable dependencies (PCI DSS, SOC 2)
- When needing automated fix PRs for vulnerable dependencies in CI/CD
- When license compliance requires visibility into open-source license obligations
- When continuous monitoring is needed for newly disclosed vulnerabilities in deployed dependencies

**Do not use** for scanning proprietary application code for logic vulnerabilities (use SAST), for runtime vulnerability detection (use DAST), or for container OS package scanning alone (use Trivy for a free alternative).

## Prerequisites

- Snyk account (free tier covers up to 200 tests per month for open source)
- Snyk CLI installed or Snyk GitHub/GitLab integration configured
- SNYK_TOKEN environment variable set with API authentication token
- Project with supported package manifests: package.json, requirements.txt, pom.xml, go.mod, Gemfile, etc.

## Workflow

### Step 1: Install and Authenticate Snyk CLI

```bash
# Install Snyk CLI
npm install -g snyk

# Authenticate with Snyk
snyk auth $SNYK_TOKEN

# Test the connection
snyk test --json | jq '.summary'
```

### Step 2: Scan Dependencies in CI/CD Pipeline

```yaml
# .github/workflows/dependency-scan.yml
name: Dependency Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 8 * * 1'  # Weekly Monday 8am

jobs:
  snyk-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: >
            --severity-threshold=high
            --fail-on=upgradable
            --json-file-output=snyk-results.json

      - name: Upload results to Snyk
        if: always()
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          command: monitor
          args: --project-name=${{ github.repository }}

      - name: Upload SARIF
        if: always()
        run: |
          npx snyk-to-html -i snyk-results.json -o snyk-report.html
```

### Step 3: Configure Snyk for Multiple Languages

```bash
# Python project scanning
snyk test --file=requirements.txt --severity-threshold=high --json > snyk-python.json

# Java/Maven project
snyk test --file=pom.xml --severity-threshold=medium --json > snyk-java.json

# Go module scanning
snyk test --file=go.mod --severity-threshold=high --json > snyk-go.json

# Docker image dependency scanning
snyk container test myapp:latest --severity-threshold=high --json > snyk-container.json

# Monorepo: scan all projects
snyk test --all-projects --severity-threshold=high --json > snyk-all.json

# IaC scanning (bonus)
snyk iac test terraform/ --severity-threshold=medium --json > snyk-iac.json
```

### Step 4: Configure Snyk Policies for Organization

```yaml

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
