# boroCTF 2026 — Geopro 5 (GEOSINT, 100pts)

**Author:** ForeverFlames  
**Category:** GEOSINT  

## Description

> What country am I in?
> Note: ONLY 5 GUESSES
> Flag format: boroCTF{country}

## Files

- `Country.png` — Google Street View screenshot of a commercial street with auto repair shops

---

## Solution

### Step 1 — Read the visible text

The image shows Arabic-language signage on auto repair and car wash shops:
- **"إصلاح الإطارات والعجلات الحديثة"** — "Repair of Tires and Modern Wheels"
- **"NEW AUTO SPARE PARTS SALE"**
- **"CAR CLEANING & POLISHING"**
- Phone number: **95967008** (8 digits)

### Step 2 — Identify the country from the phone number

The phone number has **8 digits** starting with **95**. Searching for Oman's telephone numbering plan confirms:
- Oman uses 8-digit numbers with country code **+968**
- Prefix **94xx–95xx** belongs to operator **Ooredoo Oman**

### Step 3 — Confirm with visual clues

- Arid mountainous landscape in the background → consistent with Oman's Al Hajar Mountains
- Beige/sandstone low-rise buildings → typical Gulf architecture
- Interlocking brick paving → common in Oman
- © 2026 Google watermark → Google Street View

All clues converge on **Oman**.

---

## Flag

```
boroCTF{oman}
```

---

## Key takeaways

- Phone numbers on shop signs are powerful GEOSINT anchors — format and prefix uniquely identify the country and operator
- Oman: 8-digit numbers, country code +968, prefix 95xx = Ooredoo
- Visual environment (mountains, architecture, paving style) serves as confirmation, not primary identification
- With a limited guess count, verify before submitting — phone number lookup takes 30 seconds and eliminates uncertainty
