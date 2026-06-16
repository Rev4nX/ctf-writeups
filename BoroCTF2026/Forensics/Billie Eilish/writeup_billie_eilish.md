# boroCTF 2026 — Billie Eilish (Forensics, 100pts)

**Author:** ForeverFlames  
**Category:** Forensics  

## Description

> Although she is so beautiful, its whats on the inside that matters.

## Files

- `billie.jpg`

---

## Solution

### Step 1 — Check metadata

```bash
exiftool billie.jpg
```

No flag in metadata. Clean EXIF.

### Step 2 — Check for hidden files

```bash
binwalk billie.jpg
```

Output shows a ZIP archive appended at offset `0x20EBB` (134843 bytes).

### Step 3 — Extract the ZIP

Work in the WSL home directory (not `/mnt/c/`) to avoid NTFS issues:

```bash
cp billie.jpg ~/ctf/billie/
cd ~/ctf/billie/
binwalk -e billie.jpg
ls _billie.jpg.extracted/
# 20EBB.zip
```

### Step 4 — Crack the ZIP password

The ZIP is password-protected. Use `zip2john` + `john`:

```bash
zip2john _billie.jpg.extracted/20EBB.zip > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

Password found: `badguy` — Billie Eilish's most famous song.

### Step 5 — Extract the PNG

```bash
unzip -P badguy _billie.jpg.extracted/20EBB.zip
```

Extracts `eilish.png`.

### Step 6 — Open the image

Open `eilish.png` visually. The flag is printed on Billie Eilish's t-shirt in the photo — a visible watermark added by the challenge author.

Flag on the shirt: `boroCTF{im_a_good_guy}`

---

## Flag

```
boroCTF{im_a_good_guy}
```

---

## Key takeaways

- **Look at the image** before diving into deep stego analysis — sometimes the flag is literally visible
- `binwalk` detects hidden files by magic bytes; `-e` extracts everything found automatically
- `zip2john` + `john` is the reliable combo for cracking ZIP passwords on Kali (use when `fcrackzip` is unavailable)
- ZIP metadata (filenames, sizes) is visible without a password — only file contents are encrypted
- **Always work in WSL home directory** (`~/`) for forensics operations — `/mnt/c/` (NTFS) causes I/O errors with certain file operations like binwalk extraction
- **Theme consistency:** password was `badguy` (her hit song), flag is `im_a_good_guy` (the opposite) — CTF authors often hide hints in thematic wordplay
- `stegseek` + rockyou failing doesn't mean there's no stego — it means the password isn't in rockyou, or steghide wasn't used at all
