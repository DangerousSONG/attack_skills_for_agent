---
name: acquiring-disk-image-with-dd-and-dcfldd
description: "对目标磁盘做逐位取证镜像采集固证,MD5/SHA 哈希校验保证证据完整。信号:磁盘镜像,取证镜像采集,dd,dcfldd,证据固定。"
when-to-use: Create forensically sound bit-for-bit disk images with dd or dcfldd on a Linux forensic workstation, preserving evidence integrity through hash verification (MD5/SHA) during acquisition. Use when imag
domain: cybersecurity
subdomain: digital-forensics
tags:
- forensics
- disk-imaging
- evidence-acquisition
- dd
- dcfldd
- hash-verification
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-03
- DE.AE-02
- RS.MA-01
mitre_attack:
- T1006
- T1005
- T1025
- T1074.001
---

# Acquiring Disk Image with dd and dcfldd

## When to Use
- When you need to create a forensic copy of a suspect drive for investigation
- During incident response when preserving volatile disk evidence before analysis
- When law enforcement or legal proceedings require a verified bit-for-bit copy
- Before performing any destructive analysis on a storage device
- When acquiring images from physical drives, USB devices, or memory cards

## Prerequisites
- Linux-based forensic workstation (SIFT, Kali, or any Linux distro)
- `dd` (pre-installed on all Linux systems) or `dcfldd` (enhanced forensic version)
- Write-blocker hardware or software write-blocking configured
- Destination drive with sufficient storage (larger than source)
- Root/sudo privileges on the forensic workstation
- SHA-256 or MD5 hashing utilities (`sha256sum`, `md5sum`)

## Workflow

### Step 1: Identify the Target Device and Enable Write Protection

```bash
# List all connected block devices to identify the target
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,MODEL

# Verify the device details
fdisk -l /dev/sdb

# Enable software write-blocking (if no hardware blocker)
blockdev --setro /dev/sdb

# Verify read-only status
blockdev --getro /dev/sdb
# Output: 1 (means read-only is enabled)

# Alternatively, use udev rules for persistent write-blocking
echo 'SUBSYSTEM=="block", ATTRS{serial}=="WD-WCAV5H861234", ATTR{ro}="1"' > /etc/udev/rules.d/99-writeblock.rules
udevadm control --reload-rules
```

### Step 2: Prepare the Destination and Document the Source

```bash
# Create case directory structure
mkdir -p /cases/case-2024-001/{images,hashes,logs,notes}

# Document source drive information
hdparm -I /dev/sdb > /cases/case-2024-001/notes/source_drive_info.txt

# Record the serial number and model
smartctl -i /dev/sdb >> /cases/case-2024-001/notes/source_drive_info.txt

# Pre-hash the source device
sha256sum /dev/sdb | tee /cases/case-2024-001/hashes/source_hash_before.txt
```

### Step 3: Acquire the Image Using dd

```bash
# Basic dd acquisition with progress and error handling
dd if=/dev/sdb of=/cases/case-2024-001/images/evidence.dd \
   bs=4096 \
   conv=noerror,sync \
   status=progress 2>&1 | tee /cases/case-2024-001/logs/dd_acquisition.log

# For compressed images to save space
dd if=/dev/sdb bs=4096 conv=noerror,sync status=progress | \
   gzip -c > /cases/case-2024-001/images/evidence.dd.gz

# Using dd with a specific count for partial acquisition
dd if=/dev/sdb of=/cases/case-2024-001/images/first_1gb.dd \
   bs=1M count=1024 status=progress
```

### Step 4: Acquire Using dcfldd (Preferred Forensic Method)

```bash
# Install dcfldd if not present
apt-get install dcfldd

# Acquire image with built-in hashing and split output
dcfldd if=/dev/sdb \
   of=/cases/case-2024-001/images/evidence.dd \
   hash=sha256,md5 \
   hashwindow=1G \
   hashlog=/cases/case-2024-001/hashes/acquisition_hashes.txt \
   bs=4096 \
   conv=noerror,sync \
   errlog=/cases/case-2024-001/logs/dcfldd_errors.log

# Split large images into manageable segments
dcfldd if=/dev/sdb \
   of=/cases/case-2024-001/images/evidence.dd \
   hash=sha256 \
   hashlog=/cases/case-2024-001/hashes/split_hashes.txt \
   bs=4096 \
   split=2G \
   splitformat=aa

# Acquire with verification pass
dcfldd if=/dev/sdb \
   of=/cases/case-2024-001/images/evidence.dd \
   hash=sha256 \
   hashlog=/cases/case-2024-001/hashes/verification.txt \
   vf=/cases/case-2024-001/images/evidence.dd \
   verifylog=/cases/case-2024-001/logs/verify.log
```

### Step 5: Verify Image Integrity

```bash
# Hash the acquired image
sha256sum /cases/case-2024-001/images/evidence.dd | \
   tee /cases/case-2024-001/hashes/image_hash.txt

# Compare source and image hashes
diff <(sha256sum /dev/sdb | awk '{print $1}') \
     <(sha256sum /cases/case-2024-001/images/evidence.dd | awk '{print $1}')

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
