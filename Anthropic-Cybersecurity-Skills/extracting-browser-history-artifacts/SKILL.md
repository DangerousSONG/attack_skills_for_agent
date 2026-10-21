---
name: extracting-browser-history-artifacts
description: Extracts and analyzes browser history, cookies, cache, downloads, and
when-to-use: Extracts and analyzes browser history, cookies, cache, downloads, and
  bookmarks from Chrome, Firefox, and Edge using sqlite3, DB Browser for SQLite,
  Hindsight, and NirSoft tools (BrowsingHistoryView, ChromeCacheView, MZCacheView).
  Use when performing digital forensics or incident response on a disk image or
  live system and you need timeline evidence of a user's web activity.
domain: cybersecurity
subdomain: digital-forensics
tags:
- forensics
- browser-forensics
- chrome
- firefox
- edge
- web-history
- artifact-extraction
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-03
- DE.AE-02
- RS.MA-01
mitre_attack:
- T1005
- T1074
- T1119
- T1070
- T1059
---

# Extracting Browser History Artifacts

## When to Use
- When investigating user web activity as part of a forensic examination
- During insider threat investigations to establish patterns of data exfiltration
- When tracing user visits to malicious or policy-violating websites
- For correlating browser activity with other forensic artifacts and timelines
- When investigating phishing attacks to identify which links were clicked

## Prerequisites
- Forensic image or access to user profile directories
- SQLite3 for querying browser databases
- Hindsight, BrowsingHistoryView, or DB Browser for SQLite
- Knowledge of browser artifact file locations per OS
- Python 3 with sqlite3 module for automated extraction
- Understanding of Chrome, Firefox, and Edge storage formats

## Workflow

### Step 1: Locate Browser Artifact Files

```bash
# Mount forensic image
mount -o ro,loop,offset=$((2048*512)) /cases/case-2024-001/images/evidence.dd /mnt/evidence

# Chrome artifact locations (Windows)
CHROME_WIN="/mnt/evidence/Users/suspect/AppData/Local/Google/Chrome/User Data/Default"
# Key files: History, Cookies, Login Data, Web Data, Bookmarks, Preferences,
#            Cache/, GPUCache/, Local Storage/, Session Storage/, IndexedDB/

# Firefox artifact locations (Windows)
FIREFOX_WIN="/mnt/evidence/Users/suspect/AppData/Roaming/Mozilla/Firefox/Profiles/*.default-release"
# Key files: places.sqlite, cookies.sqlite, formhistory.sqlite, logins.json,
#            key4.db, sessionstore.jsonlz4, webappsstore.sqlite

# Edge (Chromium) artifact locations (Windows)
EDGE_WIN="/mnt/evidence/Users/suspect/AppData/Local/Microsoft/Edge/User Data/Default"

# Copy artifacts to working directory
mkdir -p /cases/case-2024-001/browser/{chrome,firefox,edge}
cp -r "$CHROME_WIN"/{History,Cookies,Downloads,"Login Data","Web Data",Bookmarks} \
   /cases/case-2024-001/browser/chrome/ 2>/dev/null
cp -r $FIREFOX_WIN/{places.sqlite,cookies.sqlite,formhistory.sqlite,logins.json} \
   /cases/case-2024-001/browser/firefox/ 2>/dev/null
cp -r "$EDGE_WIN"/{History,Cookies,Downloads} \
   /cases/case-2024-001/browser/edge/ 2>/dev/null

# Hash artifacts for integrity
find /cases/case-2024-001/browser/ -type f -exec sha256sum {} \; \
   > /cases/case-2024-001/browser/artifact_hashes.txt
```

### Step 2: Extract Chrome Browsing History and Downloads

```bash
# Query Chrome History database
sqlite3 /cases/case-2024-001/browser/chrome/History << 'SQL'
.headers on
.mode csv
.output /cases/case-2024-001/analysis/chrome_history.csv

SELECT
    urls.url,
    urls.title,
    datetime(urls.last_visit_time/1000000-11644473600, 'unixepoch') AS last_visit,
    urls.visit_count,
    urls.typed_count,
    visits.transition & 0xFF AS transition_type
FROM urls
LEFT JOIN visits ON urls.id = visits.url
ORDER BY urls.last_visit_time DESC;
SQL

# Extract Chrome downloads
sqlite3 /cases/case-2024-001/browser/chrome/History << 'SQL'
.headers on
.mode csv
.output /cases/case-2024-001/analysis/chrome_downloads.csv

SELECT
    current_path,
    tab_url AS source_url,
    total_bytes,
    datetime(start_time/1000000-11644473600, 'unixepoch') AS start_time,
    datetime(end_time/1000000-11644473600, 'unixepoch') AS end_time,
    state,
    danger_type,
    mime_type
FROM downloads
ORDER BY start_time DESC;
SQL

# Extract Chrome search terms
sqlite3 /cases/case-2024-001/browser/chrome/History << 'SQL'
.headers on
.mode csv
.output /cases/case-2024-001/analysis/chrome_searches.csv

SELECT
    term,
    urls.url,
    datetime(urls.last_visit_time/1000000-11644473600, 'unixepoch') AS search_time
FROM keyword_search_terms
JOIN urls ON keyword_search_terms.url_id = urls.id
ORDER BY urls.last_visit_time DESC;
SQL
```

### Step 3: Extract Firefox Browsing History

```bash

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
