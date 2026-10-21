---
name: performing-cloud-asset-inventory-with-cartography
description: Run Cartography to sync AWS, GCP, or Azure resources into a Neo4j graph database,
when-to-use: Run Cartography to sync AWS, GCP, or Azure resources into a Neo4j graph database,
  mapping relationships such as IAM permission chains, network paths, and cross-account trust.
  Use when building a cloud asset inventory, querying the graph to identify attack paths, or
  generating security reports across multi-cloud infrastructure.
domain: cybersecurity
subdomain: cloud-security
tags:
- cartography
- neo4j
- cloud-security
- asset-inventory
- attack-path
- graph-database
- cncf
- lyft
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
mitre_attack:
- T1078.004
- T1530
- T1537
- T1580
---

# Performing Cloud Asset Inventory with Cartography

## Overview

Cartography is a CNCF sandbox project (originally created at Lyft) that consolidates infrastructure assets and their relationships into a Neo4j graph database. It queries cloud APIs to discover resources, maps relationships between them, and enables security teams to identify attack paths, generate asset reports, and find areas for security improvement. The graph model reveals hidden connections such as IAM permission chains, network paths, and cross-account trust relationships.


## When to Use

- When conducting security assessments that involve performing cloud asset inventory with cartography
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Python 3.8+
- Neo4j 4.x or 5.x database
- Cloud provider credentials (AWS, GCP, Azure)
- Docker (optional, for Neo4j deployment)
- Minimum 4GB RAM for Neo4j, more for large environments

## Installation

```bash
# Install Cartography
pip install cartography

# Verify installation
cartography --help
```

### Deploy Neo4j with Docker

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/changethispassword \
  -e NEO4J_PLUGINS='["apoc"]' \
  -v neo4j_data:/data \
  neo4j:5-community
```

## Running Cartography

### Basic AWS Sync

```bash
# Sync AWS account data to Neo4j
cartography \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-password-env-var NEO4J_PASSWORD
```

### Sync specific AWS modules

```bash
cartography \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-password-env-var NEO4J_PASSWORD \
  --aws-sync-all-profiles
```

### GCP Sync

```bash
cartography \
  --neo4j-uri bolt://localhost:7687 \
  --neo4j-user neo4j \
  --neo4j-password-env-var NEO4J_PASSWORD \
  --gcp-requested-syncs compute iam storage
```

## Security-Focused Cypher Queries

### Find all S3 buckets with public access

```cypher
MATCH (b:S3Bucket)
WHERE b.anonymous_access = true
   OR b.anonymous_actions IS NOT NULL
RETURN b.name, b.anonymous_actions, b.region, b.arn
ORDER BY b.name
```

### Identify IAM users with admin policies

```cypher
MATCH (user:AWSUser)-[:POLICY]->(policy:AWSPolicy)
WHERE policy.name = 'AdministratorAccess'
   OR policy.arn CONTAINS 'AdministratorAccess'
RETURN user.name, user.arn, policy.name, user.password_last_used
```

### Find EC2 instances exposed to internet

```cypher
MATCH (instance:EC2Instance)-[:MEMBER_OF_EC2_SECURITY_GROUP]->(sg:EC2SecurityGroup)
      -[:MEMBER_OF_EC2_SECURITY_GROUP_RULE]->(rule:IpRule)
WHERE rule.fromport <= 22 AND rule.toport >= 22
  AND rule.protocol IN ['tcp', '-1']
  AND '0.0.0.0/0' IN rule.ipranges
RETURN instance.instanceid, instance.publicipaddress, sg.groupid, sg.name
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
