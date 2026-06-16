# boroCTF 2026 — Franklin (Rev, 200pts)

**Author:** Franklin  
**Category:** Rev  

## Description

> A customized idea by me, about me, with me, for you.

## Files

- `Franklin` (no extension)

---

## Solution

### Step 1 — Identify the file

```bash
file Franklin
# Franklin: TrueType Font data, 18 tables, 1st "FFTM"
```

It's a font file. The description says "customized" — something has been modified inside this font.

### Step 2 — Basic recon

```bash
strings Franklin | grep -i "boro\|flag\|ctf"
binwalk Franklin
```

Nothing useful. The flag is not stored as a plaintext string. We need to look inside the font's internal structure.

### Step 3 — Inspect the font with fonttools

Install fonttools — a Python library for reading and modifying font files:

```bash
pip install fonttools --break-system-packages
```

First, see what tables the font contains:

```python
from fontTools.ttLib import TTFont

font = TTFont('Franklin')
print(list(font.keys()))
```

Output includes: `GSUB`, `GDEF`, `MATH`, `cmap`, `glyf`, `name`, and others.

**`GSUB`** stands for Glyph SUBstitution — this table defines rules for replacing one glyph or sequence of glyphs with another. This is where fonts define things like ligatures. It's worth investigating.

### Step 4 — Inspect the GSUB table

```python
from fontTools.ttLib import TTFont

font = TTFont('Franklin')
gsub = font['GSUB'].table

for i, lookup in enumerate(gsub.LookupList.Lookup):
    print(f'Lookup {i}: Type {lookup.LookupType}')
```

Output:
```
Lookup 0: Type 4
```

**Type 4** is a ligature substitution — it maps a sequence of glyphs to a single output glyph. Normal ligatures are short: `f + i → fi`, `f + l → fl`. Let's see what's in this one.

### Step 5 — Dump the ligatures

```bash
cat > solve.py << 'EOF'
from fontTools.ttLib import TTFont

font = TTFont('Franklin')
gsub = font['GSUB'].table

for lookup in gsub.LookupList.Lookup:
    for subtable in lookup.SubTable:
        if hasattr(subtable, 'ligatures'):
            for first_glyph, ligs in subtable.ligatures.items():
                for lig in ligs:
                    components = [first_glyph] + lig.Component
                    print(' + '.join(components), '->', lig.LigGlyph)
EOF
python3 solve.py
```

Output:
```
b + o + r + o + C + T + F + braceleft + f + R + four + n + k + l + one + n + underscore + f + zero + n + seven + braceright -> asterisk
```

This is immediately anomalous — a 22-glyph ligature. No real font uses ligatures this long for typographic purposes. Something is hidden here.

### Step 6 — Read the flag from the ligature

The glyph names map directly to characters:
- `b`, `o`, `r`, `o`, `C`, `T`, `F` → `boroCTF`
- `braceleft` → `{`
- `f`, `R` → `fR`
- `four` → `4`
- `n`, `k`, `l` → `nkl`
- `one` → `1`
- `n` → `n`
- `underscore` → `_`
- `f` → `f`
- `zero` → `0`
- `n` → `n`
- `seven` → `7`
- `braceright` → `}`

Result: **`boroCTF{fR4nkl1n_f0n7}`**

The flag was hidden as a ligature rule in the font's GSUB table. If you actually typed the flag using this font, the renderer would collapse all 22 characters into a single `*` glyph — making the flag invisible in rendered text.

---

## Flag

```
boroCTF{fR4nkl1n_f0n7}
```

---

## Key takeaways

- When given a font file, don't just look for plaintext strings — inspect the internal tables with fonttools
- **GSUB** (Glyph SUBstitution) is the table to check first: it contains ligature rules and glyph substitutions that can hide arbitrary data
- **Type 4 GSUB lookup = ligature substitution**: maps a sequence of glyphs to one output glyph. Normal ligatures have 2-3 components. A 22-component ligature is an immediate red flag
- Glyph names like `four`, `one`, `zero`, `seven`, `braceleft`, `braceright`, `underscore` are standard PostScript names for digits and punctuation — read them as characters to reconstruct the flag
- The font itself (`DejaVu Sans`) renders completely normally — the flag is invisible without directly inspecting the GSUB table
