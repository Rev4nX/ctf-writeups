# boroCTF 2026 — 64 is life (Misc, 200pts)

**Author:** ForeverFlames  
**Category:** Misc  

## Description

> Truth, broken into sixty-four.

## Files

- `64.zip`

---

## Solution

### Step 1 — Extract the archive

```bash
unzip 64.zip
```

Output: a folder `ctf_chunks/` containing 64 files.

### Step 2 — Inspect the files

The filenames are base64-encoded integers — the index of each chunk:

```
MQ==  → 1
Mg==  → 2
MTE= → 11
...
```

Each file contains either 3 bytes (a letter followed by `40`) or just `40` with no letter. For example:

```
index 1  → Y40
index 2  → m40
index 36 → =40
index 37 → 40   ← padding, no useful data
```

### Step 3 — Spot the pattern

Files with 3 bytes carry one meaningful character (the first byte), followed by `40` as noise. Files containing only `40` are padding to fill the archive to exactly 64 entries — they carry no data.

Sorting the 3-byte files by index and taking the first byte of each gives:

```
Ym9yb0NURntzMXh0eV9mMHVyX2IzYXV0eX0=
```

This is immediately recognizable as base64.

### Step 4 — Decode

```python
import base64, os

files = os.listdir('ctf_chunks')
pairs = []
for f in files:
    idx = int(base64.b64decode(f, validate=False).decode().strip('\x00'))
    content = open(f'ctf_chunks/{f}', 'rb').read().strip()
    pairs.append((idx, content))

pairs.sort()
# only take files that have an actual letter before '40'
letters = ''.join(chr(c[0]) for _, c in pairs if len(c) == 3)
print(base64.b64decode(letters).decode())
```

Output: `boroCTF{s1xty_f0ur_b3auty}`

---

## Flag

```
boroCTF{s1xty_f0ur_b3auty}
```

---

## Key takeaways

- Filenames encoded as base64 are a common CTF pattern for conveying ordering — always decode them and sort before reading content
- When content looks malformed (`Y40`, `m40`...), look at **all** fragments together before assuming the encoding — the `40` noise only becomes obvious once you see multiple files side by side
- Files containing only `40` (no leading letter) are padding to reach a round count of 64 — filter them out with `if len(c) == 3`
- `base64.b64decode(f, validate=False)` handles filenames with or without `=` padding without throwing errors
- "Truth, broken into sixty-four" = flag split into base64 single characters, each stored in a separately indexed file, padded with empty entries to 64 total
