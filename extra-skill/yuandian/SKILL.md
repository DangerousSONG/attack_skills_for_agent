---
name: yuandian
description: "Yuandian Law Database — an all-in-one skill for enterprise due diligence and legal compliance. Provides legal and regulatory retrieval with validity verification, judicial case and judgment document lookup, and full-picture queries of company registration information, equity structure, and litigation records. Use this skill first for due diligence briefs, verification of legal citations in contracts or documents, risk control reviews, and investment decisions."
zh-signals: "元典智库企业尽调与法律合规技能，提供法规检索校验、司法案例查询与企业工商涉诉信息全景查询。信号:企业尽调,法律合规,法规检索,司法案例,工商信息"
when-to-use: "Use when performing due diligence briefs, verifying legal citations in contracts or documents, conducting risk control reviews, or supporting investment decisions with regulatory, case, and company data."
license: MIT
version: 1.0.0
homepage: https://www.chineselaw.com
metadata:
  openclaw:
    requires:
      bins: ["mcporter"]
    primaryEnv: YUANDIAN_API_KEY
---

# Yuandian Law Database — Enterprise Due Diligence and Legal Compliance

Capabilities are delivered through 3 native HTTP MCP servers covering the three core data categories "law", "case", and "company", all driven through `mcporter`.

| MCP Server Name | Purpose | Typical Questions |
|------------|------|----------|
| `yuandian-law` | Legal and regulatory retrieval, validity verification | "Is this cited regulation still in force?" "What is the current text of Article X of the Anti-Unfair Competition Law?" |
| `yuandian-case` | Judicial cases, judgment documents, litigation records | "Which cases has this company been sued in?" "What is the adjudication tendency for similar cases?" |
| `yuandian-company` | Company registration information, equity structure, company overview | "Who are this company's shareholders?" "Who is the actual controller?" "Which affiliated companies exist?" |

## ⚡ Mandatory Initialization (Must Run Every Time the Skill Loads)

**After entering this skill and before performing any user operation, you must first obtain the API Key and register the 3 MCP servers with mcporter. This step must not be skipped.**

### Execution Steps

1. **Obtain the API Key and register the MCP servers** (`SKILL_DIR` is the root directory of this skill):

   - macOS / Linux:
     ```bash
     api_key=$(bash "${SKILL_DIR}/get-token.sh") && \
     mcporter config remove yuandian-law 2>/dev/null; \
     mcporter config remove yuandian-case 2>/dev/null; \
     mcporter config remove yuandian-company 2>/dev/null; \
     mcporter config add yuandian-law "https://open.chineselaw.com/mcp/law/stream" \
       --header "Authorization=Bearer $api_key" \
       --header "Accept=application/json, text/event-stream" \
       --transport http --scope home && \
     mcporter config add yuandian-case "https://open.chineselaw.com/mcp/case/stream" \
       --header "Authorization=Bearer $api_key" \
       --header "Accept=application/json, text/event-stream" \
       --transport http --scope home && \
     mcporter config add yuandian-company "https://open.chineselaw.com/mcp/company/stream" \
       --header "Authorization=Bearer $api_key" \
       --header "Accept=application/json, text/event-stream" \
       --transport http --scope home
     ```

   - Windows (PowerShell):
     ```powershell
     $apiKey = & "${SKILL_DIR}\get-token.ps1"
     mcporter config remove yuandian-law 2>$null
     mcporter config remove yuandian-case 2>$null
     mcporter config remove yuandian-company 2>$null
     mcporter config add yuandian-law "https://open.chineselaw.com/mcp/law/stream" `
       --header "Authorization=Bearer $apiKey" `
       --header "Accept=application/json, text/event-stream" `
       --transport http --scope home
     mcporter config add yuandian-case "https://open.chineselaw.com/mcp/case/stream" `
       --header "Authorization=Bearer $apiKey" `
       --header "Accept=application/json, text/event-stream" `
       --transport http --scope home
     mcporter config add yuandian-company "https://open.chineselaw.com/mcp/company/stream" `
       --header "Authorization=Bearer $apiKey" `
       --header "Accept=application/json, text/event-stream" `
       --transport http --scope home
     ```

2. **After the injection is complete**, call via mcporter:
   ```bash
   mcporter list yuandian-law --schema           # view the tool list of the law service
   mcporter list yuandian-case --schema          # view the tool list of the case service
   mcporter list yuandian-company --schema       # view the tool list of the company service
   mcporter call yuandian-company.<tool> --args '{...}'
   ```

3. **Only when the script execution fails (exit code ≠ 0) or an mcporter call returns 401**, prompt the user to complete the Yuandian authorization in the integration panel.

### 🚫 Forbidden Behaviors

- ❌ **Never** skip `get-token.sh` and ask the user to enter the API Key manually (unless the script fails)
- ❌ **Never** use an API Key value cached from a previous session
- ❌ **Never** print the API Key in plaintext to the terminal
- ❌ **Never** call https://open.chineselaw.com/mcp/* directly with curl — you must go through mcporter

## Usage Guidelines

### Guideline 1: Invocation Method

All tool calls go through `mcporter call <server>.<tool>`; first use `mcporter list <server> --schema` to obtain the tool list and parameter specification, then fill in the parameters according to that specification.

### Guideline 2: Tool Selection

- User asks about "law / statutes / regulations / whether a clause is valid / repealed / the latest text" → `yuandian-law`
- User asks about "cases / judgments / litigation / rulings / precedents" → `yuandian-case`
- User asks about "company / business registration / shareholders / shareholding / affiliated companies / actual controller / basic company information" → `yuandian-company`
- When multiple data categories are involved (for example "the company's litigation records" covers both case and company) → call them separately and have the Agent merge and summarize the results

### Guideline 3: Parameter Acquisition Order

1. The user **has provided an exact entity name or regulation name**: pass it directly
2. The user **only gave keywords or a vague description**: first use the corresponding server's search-type tool to get a candidate list, confirm the target with the user, then call the detail-type tool
3. Never fabricate full company names, regulation article numbers, or case numbers

### Guideline 4: Result Presentation

- Output in Markdown, with key fields (company name, case number, regulation name, effective date, parties, adjudication result) bolded or tabulated
- When citing a regulation, case, or company overview, the original source link or ID field must be preserved (mcporter results usually carry `url` / `id` / `caseNo` / `creditCode`)
- Highlight risk items (litigation, administrative penalties, abnormal equity changes) separately; do not mix them into ordinary information

## Typical Scenario Examples

### Scenario 1: Enterprise Risk Brief

> User: "Look up the basic information, shareholder structure, and litigation records of Beijing Huayu Yuandian Information Services Co., Ltd., and organize them into a risk brief"

Execution order:
1. `mcporter call yuandian-company.<search_or_detail>` — get basic information + shareholder structure
2. `mcporter call yuandian-case.<list_by_company>` — get litigation records
3. The Agent produces the consolidated risk brief:
   - Basic information (Unified Social Credit Code, registered capital, business scope, date of establishment)
   - Equity structure (shareholder names, shareholding percentages, capital contributions)
   - Litigation summary (total case count, typical cases, distribution of adjudication outcomes)
   - Risk warnings (e.g. major litigation, frequent equity changes, administrative penalties)

### Scenario 2: Regulation Validity Verification

> User: "Verify whether the regulations cited in this legal opinion are still in force, and mark the provisions that have expired or been amended"

Execution order:
1. Parse the text provided by the user and extract each "regulation name + article number"
2. For each one, `mcporter call yuandian-law.<verify_or_detail>` to get the current validity status and the latest text
3. The Agent outputs a comparison table:
   - ✅ Valid provision: keep the original text
   - ⚠️ Amended: original text compared against the current text
   - ❌ Expired/repealed: mark the expiry date and the replacement regulation

## Error Handling

| Symptom | Handling Action |
|------|---------|
| `get-token.sh` exit code ≠ 0 | Prompt the user to complete the Yuandian authorization in the integration panel; **never** guide the user to open.chineselaw.com to fetch the Key manually and paste it into the command |
| `mcporter call` returns 401/403 | Re-run the mandatory initialization steps to obtain the latest token |
| `mcporter list` cannot find the server | Check whether initialization ran successfully; you can run `mcporter config list` manually to confirm the 3 servers are registered |
| Incorrect tool parameters | Re-read the output of `mcporter list <server> --schema` and fix the parameters according to the returned schema; **never** proactively modify entity names provided by the user |

## Non-Triggering Scenarios

- General legal consultation and legal opinion drafting (this skill is only used for verifying rule citations)
- Personal credit report queries (different from enterprise credit investigation)
- Real-time public opinion, news, and social media content
