# boroCTF 2026 — Nature's Delight (Misc, 100pts)

**Author:** ForeverFlames  
**Category:** Misc  

## Description

> I found this tag stuck on the back of my shirt! My friend must have put it... but who even makes these?
> Flag format: boroCTF{tag_maker}

## Files

- `weirdtag.jpg` — a photo of a barcode label

---

## Solution

### Step 1 — Read the barcode number

The image shows a barcode with the number clearly printed below it:

```
075720481279
```

There is also text at the bottom: **"NOT FOR SALE IN BOTTLE DEPOSIT STATES"** — this is a standard label found on beverage containers in the US, not a clothing tag. The "tag stuck on my shirt" is a joke — it's a label peeled off a bottle.

### Step 2 — Look up the barcode

Go to **https://www.barcodelookup.com** and enter the UPC number `075720481279`.

Result:
- **Product:** Poland Spring 16.9 FL OZ (500 ml) Bottle Water
- **Manufacturer:** Poland Spring
- **Category:** Beverages > Water > Spring Water

### Step 3 — Connect the dots

"Nature's Delight" = spring water = a natural product. Poland Spring is a brand of 100% natural spring water — the title was a direct hint at the product category.

---

## Flag

```
boroCTF{poland_spring}
```

---

## Key takeaways

- UPC barcodes can be looked up at **https://www.barcodelookup.com** — just enter the number printed below the barcode
- "NOT FOR SALE IN BOTTLE DEPOSIT STATES" is a standard US beverage label — immediately identifies this as a drink container, not a clothing tag
- The challenge description was misdirection ("tag on my shirt") — the actual answer comes from reading the barcode number and looking it up
- Challenge title "Nature's Delight" + barcode lookup = Poland Spring (natural spring water) — the title is always a hint
