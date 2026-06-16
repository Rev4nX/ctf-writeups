# boroCTF 2026 — Perfectly Destructive File (REV, 200pts)

**Author:** Franklin  
**Category:** Reverse Engineering  
**Points:** 200  
**Solves:** (at time of solve)

## Description

> Subject: Urgent - John's computer is acting up again  
> John said that he downloaded a financial report for this quarter, yet now his computer has a "virus". He says that all of his files suddenly have a weird double extension. Like they all have ".boroCTF" appended onto them.  
> Can you help figure out what happened? Probably pirating video games again if you ask me.  
> Note - This challenge does NOT contain any functional malware.

## Files

- `financial_report` (no extension)

---

## Solution

### Step 1 — Identify the file type

```bash
file financial_report
# financial_report: PDF document, version 1.5
```

The file has no extension but `file` identifies it as a PDF. Rename it:

```bash
mv financial_report financial_report.pdf
```

### Step 2 — Check for hidden files

```bash
binwalk financial_report.pdf
```

Only one signature found (the PDF itself). No embedded files.

### Step 3 — Try strings

```bash
strings financial_report.pdf | grep -i "boro\|flag\|javascript"
```

The PDF uses `/Filter /FlateDecode` — its streams are zlib-compressed. `strings` returns mostly garbage because it cannot decompress them. We need a proper PDF parser.

### Step 4 — Extract JavaScript with pymupdf

PDF stores all its contents (pages, buttons, scripts) as numbered objects in a cross-reference table (xref). We iterate over every object and look for ones containing JavaScript:

```bash
pip install pymupdf --break-system-packages
```

```python
import fitz

doc = fitz.open('financial_report.pdf')
for i in range(doc.xref_length()):
    try:
        obj = doc.xref_object(i)
        if 'JS' in obj or 'JavaScript' in obj:
            print(f'xref {i}:', obj)
    except:
        pass
```

### Step 5 — Analyze the output

Two relevant objects are found:

**xref 6** — a button widget with an `AA/U/JS` action (fires on click):
```javascript
app.alert({cMsg:"Ya, I'm not making it that easy.", nIcon:3, cTitle:"boroCTF 2026"});
```
This is a decoy. Clicking the "Click me for free flag!" button just shows an alert.

**xref 4** — a JavaScript action that runs on document open:
```javascript
var a = 7;
var b = 13;
// ... lots of noise variables ...
var encoded = "Ym9yb0NURnswbjFfRiFsZV9JNV9AMTFfaXRfdEFrZSR9";
var decoded = util.printd("yyyy", new Date());
```

All the variables (`a`, `b`, `c`, `d`...) are noise. The flag is in `encoded`.

### Step 6 — Decode base64

The string `Ym9yb0NURnsw...` is recognizable as base64 by its character set and structure.

```bash
echo "Ym9yb0NURnswbjFfRiFsZV9JNV9AMTFfaXRfdEFrZSR9" | base64 -d
```

Or in CyberChef: paste → "From Base64" recipe.

---

## Flag

```
boroCTF{0n1_F!le_I5_@11_it_tAke$}
```

---

## Key takeaways

- PDFs are not just documents — they can contain JavaScript, forms, and actions
- `/Filter /FlateDecode` means zlib compression; `strings` alone won't work
- PDF objects are stored in a cross-reference table (xref); iterate over it to find hidden content
- The decoy (button + alert) is there to waste your time — always look at all JS, not just the obvious one
- Base64 is recognizable on sight: alphanumeric + `/` + `+`, length divisible by 4, often ends with `=`
