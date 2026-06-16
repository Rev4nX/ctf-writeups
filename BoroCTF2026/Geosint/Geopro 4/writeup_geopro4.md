# boroCTF 2026 — Geopro 4 (GEOSINT, 100pts)

**Author:** ForeverFlames  
**Category:** GEOSINT  

## Description

> Find the streetname. :D
> Flag format: boroCTF{street_name}

## Files

- `street.png` — Google Street View screenshot of a commercial street in the Philippines

---

## Solution

The image shows a Google Street View screenshot (GSV pin icons and © 2023 copyright watermark visible) of a Filipino commercial street. Tricycles (local transport) confirm the Philippines.

Two unique business names are visible:
- **Medicus Diagnostic Center**
- **Pizza Junction**

Search Google with both names in quotes to force an exact co-location match:

```
"Medicus Diagnostic Center" "Pizza Junction" Philippines street
```

The first result confirms **Pizza Junction** is located on **Rizal Street, Roxas City, Capiz Province, Philippines**.

---

## Flag

```
boroCTF{rizal_street}
```

---

## Key takeaways

- Quoting multiple unique business names in one search (`"Name A" "Name B"`) forces Google to find pages containing both — instantly narrowing results to the exact location
- Medicus has 28+ branches across the Philippines (poor anchor), Pizza Junction in Roxas City is unique (strong anchor) — always prefer the rarer business as your primary signal
- Tricycles/pedicabs visible in a Street View screenshot = Philippines, narrows the country immediately
- GSV pin icons and copyright watermark confirm the image source is Google Street View, not a standalone photo
