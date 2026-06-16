# boroCTF 2026 — File File Crocodile (Misc, 200pts)

**Author:** ForeverFlames  
**Category:** Misc  

## Description

> We managed to snap a picture of the infamous File File Crocodile, but right before the flash went off, he swallowed a locked archive containing our flag! He's a master of disguise and his stomach acid has slightly digested the file signatures. Interrogating him didn't work as the only word he seemed to know was "croc".
> Can you cut him open, perform some surgery, and get our archive back?

## Files

- `file_file_crocodile.png` — PNG image with a hidden encrypted ZIP appended

---

## Reading the description as technical hints

Every sentence in the description is a technical clue:
- **"swallowed a locked archive"** → a ZIP file is hidden inside the PNG
- **"stomach acid has slightly digested the file signatures"** → magic bytes of the ZIP are corrupted/replaced
- **"the only word he seemed to know was 'croc'"** → the password to the ZIP is `croc`

In CTF challenges, description text is never decorative. Read it twice before reaching for tools.

---

## Solution

### Step 1 — Initial recon

```bash
file file_file_crocodile.png
# PNG image data, 800 x 1280, 8-bit/color RGBA, non-interlaced

binwalk file_file_crocodile.png
# Only finds the PNG itself — nothing else
```

`binwalk` finds nothing because the ZIP's magic bytes are corrupted. Empty tool output is a clue, not a dead end.

### Step 2 — Look at the raw bytes

```bash
xxd file_file_crocodile.png | tail -50
```

After the PNG end marker `IEND` (hex `49 45 4e 44`) + 4-byte CRC, there is extra data:

```
...flag.txtUT...
...PK...
```

`flag.txt` is a filename inside an archive. `PK` bytes are the ZIP Central Directory signature. A ZIP is appended directly after the PNG ends.

**Why is `flag.txt` visible before `PK`?** ZIP has an inverted structure — the Central Directory (table of contents) lives at the **end** of the file, and actual file data lives at the beginning. `tail` shows the end, so you see the Central Directory first.

### Step 3 — Identify the corrupted magic bytes

```bash
xxd file_file_crocodile.png | grep -i "croc\|FC"
```

The Local File Header at the start of the ZIP shows `46 43` (`FC` in ASCII) instead of `50 4B` (`PK`). The author replaced `PK` with `FC` — **F**ile **C**rocodile. This is why `binwalk` missed it.

The Central Directory at the end was left intact (`PK` = `50 4B`), which is why `flag.txt` was visible in `tail`.

### Step 4 — Extract and repair the ZIP

```python
# Step 1: cut the ZIP out of the PNG
data = open('file_file_crocodile.png', 'rb').read()
iend = data.rfind(b'IEND')
zdata = data[iend + 8:]          # skip IEND (4 bytes) + CRC (4 bytes)
open('extracted.zip', 'wb').write(zdata)

# Step 2: repair FC (0x46 0x43) -> PK (0x50 0x4B) in Local File Headers
fixed = bytearray(zdata)
for i in range(len(fixed) - 3):
    if fixed[i] == 0x46 and fixed[i+1] == 0x43 and fixed[i+2] in (0x03, 0x01, 0x05):
        fixed[i] = 0x50    # P
        fixed[i+1] = 0x4B  # K
open('fixed.zip', 'wb').write(fixed)
```

```bash
file fixed.zip
# Zip archive data
unzip -l fixed.zip
# flag.txt  45 bytes
```

### Step 5 — Extract with the password from the description

```bash
unzip -P croc fixed.zip
cat flag.txt
```

Password `croc` — stated directly in the description: *"the only word he seemed to know was 'croc'"*.

---

## Flag

```
BoroCTF{n3v3r_sm1l3_4t_4_p0lygl0t_cr0c0d1l3}
```

---

## What is a polyglot file?

A **polyglot** is a single file that is simultaneously valid in two different formats. Here:

```
[valid PNG: from start to IEND+CRC          ]
[valid ZIP: from IEND+CRC to end of file    ]
```

- An image viewer opens it → sees PNG magic bytes at offset 0 → reads it as an image → stops at `IEND` → ignores the rest. Fully valid PNG.
- `unzip` opens it → doesn't care what's at the start → finds End of Central Directory at the end → reads the ZIP from the back. Fully valid ZIP.

Both programs are correct. One file, two formats simultaneously.

ZIP is particularly well-suited for polyglots because its Central Directory is at the **end** of the file — you can append a ZIP after any other format and it still works.

The author intentionally corrupted only the Local File Header magic bytes (the very start of the ZIP data) to prevent `binwalk` from auto-detecting it, while leaving the Central Directory intact so the ZIP remained recoverable.

## Key takeaways

- **Read the description as a technical specification** — every sentence was a direct clue: hidden archive, corrupted signatures, password
- **Empty `binwalk` output = corrupted signatures**, not absence of hidden data — look at raw bytes with `xxd`
- **`xxd | tail`** reveals data appended after the end of the nominal file format
- **ZIP structure is inverted** — Central Directory (table of contents) is at the end; data is at the beginning. This is why `flag.txt` appeared before `PK` in `tail` output
- **`FC` = `F`ile `C`rocodile** — the author replaced `PK` with `FC` as a thematic hint hiding in plain sight
- **Try the obvious password first** — before wordlists, re-read the description. `croc` was stated explicitly
- **Polyglot files** are a real attack technique used in malware (file looks like an image to AV, executes as binary) and XSS (server accepts it as image, browser executes it as script)
