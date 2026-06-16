# boroCTF 2026 — Nature's Takeover (OSINT, 100pts)

**Author:** ForeverFlames  
**Category:** OSINT  

## Description

> You can't beat nature. What is this?  
> Example: `boroCTF{not_the_flag}`

## Files

- `nature.png`

---

## Solution

### Step 1 — Analyze the image

The image shows an aerial drone photo of an abandoned ship completely overgrown with trees, sitting in greenish water.

### Step 2 — Reverse image search

Upload `nature.png` to Google Images or Gemini. Results immediately identify the location as **SS Ayrfield** in Homebush Bay, Sydney, Australia — famously known as "The Floating Forest."

Key facts:
- Built in 1911 in the UK as SS Corrimal
- Used to transport supplies to US troops during WWII
- Decommissioned in 1972, left in Homebush Bay ship-breaking yard
- Mangrove trees grew inside the rusting hull over decades

### Step 3 — Submit

```
boroCTF{SS_Ayrfield}
```

Note: `boroCTF{floating_forest}` (the popular nickname) does not work — the challenge requires the official ship name.

---

## Flag

```
boroCTF{SS_Ayrfield}
```

---

## Key takeaways

- Reverse image search (Google Images, Gemini) is the go-to first step for image-based OSINT
- When the flag format is open-ended, try the official name before nicknames
