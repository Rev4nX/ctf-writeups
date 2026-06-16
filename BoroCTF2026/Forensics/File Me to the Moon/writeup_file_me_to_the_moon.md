# boroCTF 2026 — File Me to the Moon (Forensics, 100pts)

**Author:** ForeverFlames  
**Category:** Forensics  

## Description

> Frank Sinatra accidentally deleted the file extension on one of his files!!!  
> What file extension is it supposed to be???  
> `boroCTF{file_extension}`

## Files

- `superfile`

---

## Solution

### Step 1 — Identify the file type

The file has no extension. Use the `file` command which reads magic bytes (the first bytes of a file that uniquely identify its format):

```bash
file superfile
# superfile: Microsoft PowerPoint 2007+
```

The file is a PowerPoint presentation. The extension is `pptx`.

---

## Flag

```
boroCTF{pptx}
```

---

## Key takeaways

- File extensions are unreliable — always use `file` to identify the actual format
- `file` reads magic bytes: a unique byte signature at the start of every file format
- `.pptx`, `.docx`, `.xlsx` all start with `PK\x03\x04` (ZIP signature) — `file` digs into the ZIP contents to distinguish between them
- "2007+" refers to the OOXML format introduced in Office 2007, not the year the file was created — all modern Office versions use the same format
