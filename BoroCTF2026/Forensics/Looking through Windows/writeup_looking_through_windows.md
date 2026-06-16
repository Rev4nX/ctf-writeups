# boroCTF 2026 — Looking through Windows (Forensics, 200pts)

**Author:** Solarity  
**Category:** Forensics  

## Description

> My friend thinks he can hide his secrets from me by deleting them...  
> Who's gonna tell him?

## Files

- `challenge.zip` → `challenge.vhd` — Virtual Hard Disk image (Windows NTFS)

---

## Solution

### Step 1 — Identify the file

```bash
unzip challenge.zip
file challenge.vhd
# challenge.vhd: Microsoft Disk Image, Virtual Server or Virtual PC
```

A `.vhd` is a **Virtual Hard Disk** — a binary image of a Windows virtual disk used by Hyper-V and similar tools. The challenge title "Looking through Windows" is a double hint: Windows OS + looking *through* (into) the disk image.

### Step 2 — Examine the partition table

```bash
mmls challenge.vhd
```

Output shows an NTFS partition starting at sector 128:
```
002:  000:000   0000000128   0000096383   0000096256   NTFS / exFAT (0x07)
```

- `mmls` (The Sleuth Kit) — lists the partition table of a disk image
- Offset 128 is needed for all subsequent commands

### Step 3 — List files including deleted ones

```bash
fls -r -o 128 challenge.vhd
```

- `fls` — file listing tool from The Sleuth Kit
- `-r` — recursive (all subdirectories)
- `-o 128` — partition offset in sectors

Deleted files are marked with `*`:

```
$RECYCLE.BIN/S-1-5-21-.../
  -/r * 39-128-1:    $RIFYI8L.zip    ← deleted file DATA
  -/r * 43-128-1:    $IIFYI8L.zip    ← deleted file METADATA
```

Two entries in the Recycle Bin. Windows Recycle Bin stores every deleted file as two entries:
- `$R` prefix = actual file data
- `$I` prefix = metadata (original path, deletion date, size)

The interesting one is `$RIFYI8L.zip` (inode 39).

### Step 4 — Recover the deleted file

```bash
icat -o 128 challenge.vhd 39 > recovered1.zip
file recovered1.zip
# recovered1.zip: Zip archive data
```

- `icat` — extracts a file by inode number from a disk image
- The file is extracted to the local filesystem, not back into the VHD

### Step 5 — Crack the ZIP password

```bash
zip2john recovered1.zip > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

John the Ripper finds the password: **`forget92936281`**

### Step 6 — Extract the flag

```bash
unzip -P forget92936281 recovered1.zip
cat flag.txt
```

---

## Flag

```
boroCTF{f!l3_f0r3nsics_FTW!!}
```

---

## Key takeaways

- **Deleting ≠ erasing** — on NTFS (and most filesystems), deletion only removes the directory entry. The actual data stays on disk until overwritten. This is the core concept of file recovery forensics
- **Windows Recycle Bin structure**: every deleted file creates two entries — `$R` (data) and `$I` (metadata). Always look for `$R` files for the actual content
- **The Sleuth Kit workflow**: `mmls` (partition table) → `fls` (file listing with deletions) → `icat` (extract by inode). This is the standard forensic trifecta for disk images
- **VHD files** are Windows virtual disk images — treat them like any other disk image, no need to mount
- **`zip2john` + `john`** is the standard pipeline for cracking ZIP passwords. Rockyou covers most CTF passwords
- The hint "Looking through Windows" = analyzing a Windows disk image; "he thinks he can hide by deleting" = file recovery from NTFS
