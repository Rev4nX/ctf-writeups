# boroCTF 2026 — Retinal Burn (Forensics, 200pts)

**Author:** Franklin  
**Category:** Forensics  

## Description

> My friend Jonas Wagner sent me a challenge but I can't be bothered to do it. He was always one to be working on his own sorts of projects and stuff. You do it.

## Files

- `burn.png` — 800x800 PNG with text "TOO BRIGHT!!!"

---

## Reading the hints

- **Jonas Wagner** — creator of steganography tools including stegano.js and photo-forensics tools at 29a.ch. His name is a direct pointer to image steganography.
- **"TOO BRIGHT"** — the hidden data is concealed in near-white pixels, invisible to the naked eye.
- **"Retinal Burn"** — the image "burns" your eyes with fake flags to distract from the real one.

## Standard recon (all negative)

```bash
strings burn.png | grep -i "flag|boro|ctf"   # nothing
binwalk burn.png                               # only the PNG itself
exiftool burn.png                             # no flag in metadata
zsteg burn.png                                # nothing in LSB
```

---

## Solution

### Step 1 — Discover the hidden layer

The image has a mean pixel value of 242/255 — extremely bright. Amplifying differences from white (255 - pixel, then ×50–100) reveals two overlapping text layers:
- **Red text**: `FAKE_FLAG` repeated across the entire image
- **Blue text**: the real flag, hidden in near-white pixels with a subtle blue channel anomaly

### Step 2 — Separate the channels

Red text and blue text live in different color channels:
- Red FAKE_FLAG pixels: R channel lower than 255, B channel near 255 → `R < B`
- Blue flag pixels: B channel lower than 255, R channel near 255 → `B < R`

### Step 3 — Extract the flag

Isolate pixels where `R > B` (blue text only), amplify the R−B difference, crop the top ~120px where the flag text sits.

```python
# [SCRIPT TO BE ADDED — extract blue channel anomaly from top 120px]
# Key operation: diff = R_channel - B_channel
# Mask: diff >= 1
# Output: grayscale image where darker = larger R-B difference
```

### Step 4 — Read the flag

The resulting image shows: `BoroCTF{0W_^MY_E7ES!}`

---

## Flag

```
BoroCTF{0W_^MY_E7ES!}
```

---

## Key takeaways

- **Named authors in challenge descriptions are always hints** — Jonas Wagner = steganography tools at 29a.ch
- **"TOO BRIGHT" = hidden data in near-white pixels** — classic technique: data concealed in pixels that differ from the background by only 1-2 per channel
- **Fake flags are a deliberate distraction** — the red FAKE_FLAG layer exists to confuse automated tools and casual visual inspection
- **Channel separation is the key** — when two hidden layers overlap, isolating individual RGB channels separates them cleanly. Red anomaly (R < 255, B ≈ 255) vs blue anomaly (B < 255, R ≈ 255)
- **Amplification reveals subtle differences** — multiplying (255 - pixel) by a large factor (×50-100) makes 1-2 unit differences visible
