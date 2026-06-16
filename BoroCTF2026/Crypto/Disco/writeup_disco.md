# boroCTF 2026 — Disco (Crypto, 200pts)

**Author:** Franklin  
**Category:** Crypto  

## Description

> The hexagonal colors are simply beautiful.

## Files

- `dance.png`

---

## Solution

### Step 1 — Read the hint

"Hexagonal colors" = hex color codes. The image contains blocks of color — each unique color encodes 3 ASCII characters via its RGB values (R=char1, G=char2, B=char3).

### Step 2 — Extract unique colors

Open `dance.png` in an image color picker like https://imagecolorpicker.com/ and extract the hex value of each unique color block in order (left to right, top to bottom):

```
#626f72
#6f4354
#467b6e
#457633
#725f6c
#302465
#5f596f
#55345f
#426540
#747d00
#000000
#000000
```

### Step 3 — Decode

Each hex color `#RRGGBB` maps to three ASCII characters: `chr(RR)`, `chr(GG)`, `chr(BB)`.

```python
colors = [
    "#626f72",
    "#6f4354",
    "#467b6e",
    "#457633",
    "#725f6c",
    "#302465",
    "#5f596f",
    "#55345f",
    "#426540",
    "#747d00",
    "#000000",
    "#000000"
]

result = ''
for hex_color in colors:
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    result += chr(r) + chr(g) + chr(b)

print(result.strip('\x00'))
```

Output: `boroCTF{nEv3r_l0$e_YoU4_Be@t}`

Note: the last `#000000` pixels produce null bytes (`\x00`) — strip them before submitting.

---

## Flag

```
boroCTF{nEv3r_l0$e_YoU4_Be@t}
```

---

## Key takeaways

- "Hexagonal colors" = hex color codes = RGB values encoding ASCII characters
- Each pixel's RGB values (0-255) map directly to ASCII — R=first char, G=second, B=third
- Use https://imagecolorpicker.com/ to extract hex values from color blocks
- Watch out for null bytes from black `#000000` pixels — strip them with `.strip('\x00')`
- Missing commas between strings in a Python list causes silent concatenation — always check your list syntax
