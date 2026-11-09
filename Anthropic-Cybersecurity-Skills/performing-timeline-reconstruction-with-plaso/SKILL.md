---
name: performing-timeline-reconstruction-with-plaso
description: "Performs timeline reconstruction with Plaso. Signals: asset mapping, fingerprinting, technology stack identification."
zh-signals: "Performing Timeline Reconstruction with Plaso 信号:资产测绘,指纹识别,技术栈识别。"
when-to-use: >-
  Builds comprehensive forensic super-timelines using Plaso (log2timeline and
  psort) to correlate events across file system metadata, event logs, browser
  history, and registry artifacts into a unified chronological view. Use
  during complex forensic investigations that need cross-source event
  correlation, or when standard log analysis is insufficient to establish the
  sequence of activities for reporting findings.
domain: cybersecurity
subdomain: digital-forensics
tags:
- forensics
- timeline-analysis
- plaso
- log2timeline
- super-timeline
- event-correlation
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

# Performing Timeline Reconstruction with Plaso

## When to Use
- When building a comprehensive forensic timeline from multiple evidence sources
- For correlating events across file system metadata, event logs, browser history, and registry
- During complex investigations requiring chronological reconstruction of activities
- When standard log analysis is insufficient to establish the sequence of events
- For presenting investigation findings in a visual, chronological format

## Prerequisites
- Plaso (log2timeline/psort) installed on forensic workstation
- Forensic disk image(s) in raw (dd), E01, or VMDK format
- Sufficient storage for Plaso output (can be 10x+ the image size)
- Minimum 8GB RAM (16GB+ recommended for large images)
- Timeline Explorer (Eric Zimmerman) or Timesketch for visualization
- Understanding of timestamp types (MACB: Modified, Accessed, Changed, Born)

## Workflow

### Step 1: Install Plaso and Prepare the Environment

```bash
# Install Plaso on Ubuntu/Debian
sudo add-apt-repository ppa:gift/stable
sudo apt-get update
sudo apt-get install plaso-tools

# Or install via pip
pip install plaso

# Or use Docker (recommended for dependency isolation)
docker pull log2timeline/plaso

# Verify installation
log2timeline.py --version
psort.py --version

# Create output directory
mkdir -p /cases/case-2024-001/timeline/

# Verify the forensic image
img_stat /cases/case-2024-001/images/evidence.dd
```

### Step 2: Generate the Plaso Storage File with log2timeline

```bash
# Basic processing of a disk image (all parsers)
log2timeline.py \
   --storage-file /cases/case-2024-001/timeline/evidence.plaso \
   /cases/case-2024-001/images/evidence.dd

# Process with specific parsers for faster targeted analysis
log2timeline.py \
   --parsers "winevtx,prefetch,mft,usnjrnl,lnk,recycle_bin,chrome_history,firefox_history,winreg" \
   --storage-file /cases/case-2024-001/timeline/evidence.plaso \
   /cases/case-2024-001/images/evidence.dd

# Process with a filter file to focus on specific paths
cat << 'EOF' > /cases/case-2024-001/timeline/filter.txt
/Windows/System32/winevt/Logs
/Windows/Prefetch
/Users/*/NTUSER.DAT
/Users/*/AppData/Local/Google/Chrome
/Users/*/AppData/Roaming/Mozilla/Firefox
/$MFT
/$UsnJrnl:$J
/Windows/System32/config
EOF

log2timeline.py \
   --filter-file /cases/case-2024-001/timeline/filter.txt \
   --storage-file /cases/case-2024-001/timeline/evidence.plaso \
   /cases/case-2024-001/images/evidence.dd

# Using Docker
docker run --rm -v /cases:/cases log2timeline/plaso log2timeline \
   --storage-file /cases/case-2024-001/timeline/evidence.plaso \
   /cases/case-2024-001/images/evidence.dd

# Process multiple evidence sources into one timeline
log2timeline.py \
   --storage-file /cases/case-2024-001/timeline/combined.plaso \
   /cases/case-2024-001/images/workstation.dd

log2timeline.py \
   --storage-file /cases/case-2024-001/timeline/combined.plaso \
   /cases/case-2024-001/images/server.dd
```

### Step 3: Filter and Export Timeline with psort

```bash
# Export full timeline to CSV (super-timeline format)
psort.py \
   -o l2tcsv \
   -w /cases/case-2024-001/timeline/full_timeline.csv \
   /cases/case-2024-001/timeline/evidence.plaso

# Export with date range filter (focus on incident window)
psort.py \
   -o l2tcsv \
   -w /cases/case-2024-001/timeline/incident_window.csv \
   /cases/case-2024-001/timeline/evidence.plaso \
   "date > '2024-01-15 00:00:00' AND date < '2024-01-20 23:59:59'"

# Export in JSON Lines format (for ingestion into SIEM/Timesketch)
psort.py \
   -o json_line \
   -w /cases/case-2024-001/timeline/timeline.jsonl \
   /cases/case-2024-001/timeline/evidence.plaso

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
