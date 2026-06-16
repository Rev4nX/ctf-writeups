# boroCTF 2026 — Grep'n it (Forensics, 100pts)

**Author:** Franklin  
**Category:** Forensics  

## Description

> I lost my flag in a stockpile of fake flags :(. Can you help me find it?

## Files

- `chal`

---

## Solution

### Step 1 — Identify the file

```bash
file chal
```

This tells us what kind of file we're dealing with before opening it blindly.

### Step 2 — Find the flag

The file contains many fake flags mixed with the real one. We need to find the one matching the `boroCTF` format.

**Method 1 — Terminal (recommended):**
```bash
grep "boro" chal
```

Or equivalently:
```bash
cat chal | grep "boro"
```

Both work. The first is cleaner — `grep` can read files directly without needing `cat`. The `cat | grep` pattern is sometimes called "useless use of cat" but is perfectly valid and widely used.

**Method 2 — Text editor:**  
Open `chal` in any text editor (Notepad, VS Code, etc.) and use Ctrl+F to search for `boro`. Same result, no terminal needed.

Both methods are equally valid — use whichever you're more comfortable with.

---

## Flag

```
boroCTF{G63p_G0d}
```

---

## Key takeaways

- `grep "pattern" file` searches for a pattern in a file — the most useful forensics command for finding flags in large files
- `cat file | grep "pattern"` works identically but is slightly redundant — `grep` can read files directly
- Ctrl+F in a text editor is a perfectly valid alternative to `grep` for small files
- When a file contains many fake flags, always search for the unique prefix (`boroCTF`) to find the real one instantly
