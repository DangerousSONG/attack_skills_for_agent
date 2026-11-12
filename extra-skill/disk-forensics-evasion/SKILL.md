---
name: disk-forensics-evasion
description: "Disk forensics and anti-disk-forensics methodology. Understand how blue teams recover deleted files from disk, extract timelines, and analyze filesystem artifacts, and how red teams perform anti-forensics (secure deletion, timestomping, trace cleanup). Use when disk forensics must be evaded or disk analysis must be performed"
zh-signals: "磁盘取证与反取证方法论，兼顾蓝队恢复证据与红队清除痕迹。信号:磁盘取证,反取证,安全删除,时间戳篡改,MFT分析。"
when-to-use: "Use when performing disk forensics with Sleuth Kit, plaso or analyzeMFT, recovering deleted files and building timelines from NTFS or ext4 artifacts, or conducting anti-forensics such as secure deletion with shred or sdelete, timestomping, USN Journal deletion, and log artifact cleanup."
metadata:
  tags: "disk,forensics,anti-forensics,timestomp,file-recovery,MFT,NTFS,ext4,artifact,disk forensics,anti-forensics,timestamp"
  category: "dfir"
  mitre_attack: "T1070,T1070.004,T1070.006,T1036.006,T1564.001"
---

# Disk Forensics and Anti-Disk-Forensics

> **Two-sided view**: the blue team recovers evidence from disk → the red team ensures the evidence cannot be recovered

## ⛔ Further Reading

- Detailed Windows NTFS artifacts and cleanup methods → [references/ntfs-artifacts.md](references/ntfs-artifacts.md)
- Linux ext4 forensics and anti-forensics → [references/linux-disk-forensics.md](references/linux-disk-forensics.md)

---

## Part A: Blue Team Perspective — Disk Forensics

### Phase 1: Evidence Acquisition

```bash
# Full image with dcfldd (including hash verification)
dcfldd if=/dev/sdb of=/evidence/disk.dd \
  hash=sha256 hashlog=/evidence/disk.sha256 \
  bs=4096 conv=noerror,sync

# Use the E01 format (compressed + split)
ewfacquire /dev/sdb -t /evidence/disk \
  -c deflate -S 2G -e "Case INC-2025"

# Verify integrity
sha256sum /evidence/disk.dd
```

### Phase 2: File System Analysis Decision Tree

```
Which file system type?
├─ NTFS (Windows) → MFT analysis / USN Journal / $LogFile
├─ ext4 (Linux) → inode / journal / superblock
├─ APFS (macOS) → diskutil / apfs_parser
└─ FAT32 (USB) → simple file table / cluster analysis
```

### Phase 3: Key Windows NTFS Artifacts

| Artifact | Location | Content |
|----------|------|------|
| $MFT | Volume root | Metadata for every file (timestamps, size, path) |
| $UsnJrnl | $Extend\ | File change log (create/delete/rename) |
| $LogFile | Volume root | NTFS transaction log |
| Prefetch | C:\Windows\Prefetch\ | Program execution records (last 8 execution times) |
| Amcache | C:\Windows\AppCompat\ | First program execution + SHA1 |
| Shimcache | Registry | Program compatibility cache |
| LNK files | Recent\ | Recently accessed file records |
| Jump Lists | CustomDestinations\ | Taskbar program history |
| $Recycle.Bin | Volume root | Recycle Bin ($I=metadata $R=content) |
| VSS | System Volume Information | Volume shadow copies (historical snapshots) |

```bash
# Sleuth Kit analysis
fls -r -p /evidence/disk.dd        # recursively list files (including deleted ones)
icat /evidence/disk.dd <inode>     # extract file content by inode
tsk_recover -r /evidence/disk.dd /output/  # recover deleted files

# MFT parsing
python3 analyzeMFT.py -f \$MFT -o mft_output.csv

# Timeline generation
log2timeline.py /evidence/timeline.plaso /evidence/disk.dd
psort.py -o l2tcsv /evidence/timeline.plaso > timeline.csv
```

### Phase 4: Key Linux ext4 Artifacts

| Artifact | Content |
|----------|------|
| /var/log/ | System logs (auth.log, syslog, wtmp, btmp) |
| .bash_history | Command history |
| /tmp/ | Temporary files (a directory commonly used by attackers) |
| crontab | Persistence via scheduled task |
| /etc/passwd + shadow | Newly added accounts |
| journal (ext4) | File system operation log |
| inode timestamps | atime/mtime/ctime/crtime |

---

## Part B: Red Team Perspective — Anti-Disk-Forensics

### Strategy 1: Secure Deletion (Unrecoverable)

```bash
# ⛔ A normal rm only removes the MFT entry, the data is still on disk!

# Linux secure deletion
shred -vfz -n 3 target_file      # multiple overwrites + zero fill
srm -sz target_file               # secure delete

# Windows secure deletion
cipher /w:C:\path\                # overwrite free space
sdelete -p 3 target_file          # Sysinternals secure delete

# In-memory file system operations (never touch the disk)
# Linux: work in /dev/shm or tmpfs
mkdir /dev/shm/.work && cd /dev/shm/.work
# Windows: use a Named Pipe / in-memory mapped file
```

### Strategy 2: Timestomping (T1070.006)

```bash
# Linux: touch modifies atime/mtime
touch -t 202301011200.00 malware.elf    # disguise it as an old file
touch -r /bin/ls malware.elf            # match the timestamps of a legitimate file

# Windows: PowerShell
$(Get-Item file.exe).CreationTime = "01/01/2023 12:00:00"
$(Get-Item file.exe).LastWriteTime = "01/01/2023 12:00:00"
$(Get-Item file.exe).LastAccessTime = "01/01/2023 12:00:00"

# ⛔ Note: NTFS has 4 sets of timestamps!
# Timestamps in $STANDARD_INFORMATION → modifiable with the methods above
# Timestamps in $FILE_NAME → modifiable only through low-level NTFS operations
# Blue teams compare the two sets → they detect timestomping
```

### Strategy 3: Artifact Cleanup Checklist

```
Clean up after Windows operations:
├─ Prefetch → delete C:\Windows\Prefetch\TOOLNAME-*.pf
├─ Amcache → delete the registry entries (requires SYSTEM privileges)
├─ Shimcache → cached in memory, modify the registry before reboot
├─ USN Journal → fsutil usn deletejournal /d C:
├─ Event Log → wevtutil cl Security/System/Application
├─ Recent/LNK → delete %APPDATA%\Microsoft\Windows\Recent\*
├─ Jump Lists → delete CustomDestinations\*
├─ $Recycle.Bin → manually deleted items never reach the Recycle Bin
└─ Thumbcache → delete %LocalAppData%\Microsoft\Windows\Explorer\thumbcache*

Clean up after Linux operations:
├─ .bash_history → unset HISTFILE or export HISTSIZE=0
├─ /var/log/ → modify precisely (do not truncate, it will be noticed)
├─ wtmp/btmp → utmpdump → edit → utmpdump -r
├─ auth.log → sed -i to delete specific lines
├─ journal → journalctl --vacuum-time=1h
└─ /tmp/ files → shred then delete
```

### Strategy 4: Best Practice — Leave Few Traces From the Start

```
The optimal OPSEC approach (prevention > cleanup):
├─ Tools never touch the disk → in-memory execution (reflective loading / fileless)
├─ Use a RAM disk → /dev/shm or tmpfs
├─ unset HISTFILE before operating → commands are not recorded
├─ Use LOLBins → introduce no new files
├─ Transfer through a pipe → curl | python leaves nothing on disk
├─ Encrypt files written to disk → even if found they cannot be analyzed
└─ Minimal dwell time → delete as soon as you are done
```

## Comparison Table: Forensic Techniques vs Red Team Countermeasures

| Blue team technique | Red team exposure | Red team countermeasure |
|----------|---------|---------|
| File recovery (icat/tsk_recover) | The data is still present after rm | Overwrite with shred/sdelete |
| Timeline analysis (plaso) | Anomalous operation times | Timestomping |
| MFT analysis | $FN timestamps not modified | Low-level NTFS operations or never touching the disk |
| USN Journal | File operation records | Delete the USN Journal |
| Prefetch analysis | Tool execution records | Delete the .pf files or avoid a standalone EXE |
| Volume shadow copies | Snapshots of historical files | vssadmin delete shadows |
| Log analysis | Login/operation records | Delete precise log lines (not whole logs) |
