# boroCTF 2026 — AI Slop (Misc, 100pts)

**Author:** ForeverFlames  
**Category:** Misc  

## Description

> What is this AI slop??? Which AI made this!!!
> Format: boroCTF{ai_in_lowercase}
> WARNING ONLY 5 ATTEMPTS.

## Files

- `slop.jpg` — a boroCTF 2026 promotional banner with glitchy cyberpunk aesthetic

---

## Solution

### Step 1 — Examine the image

The image is a glitchy cyberpunk-style banner for boroCTF 2026. Visual characteristics: skull mascot, neon colors, glitch text artifacts, binary code background. The challenge asks which AI generated it.

### Step 2 — Check metadata

```bash
exiftool slop.jpg
```

No useful EXIF metadata. No C2PA content credentials embedded. The flag is not hidden in the file itself — we need to identify the generator from the image content.

### Step 3 — Use an AI image detector

Upload `slop.jpg` to:

**https://hivemoderation.com/ai-generated-content-detection**

Result:
- AI-Generated: **83.3%**
- Top match: **gemini3: 76.5%**
- Other candidates: imagen4: 12.8%, ernie: 3.1%

Gemini (Google's image generation model) scores highest by a significant margin.

### Step 4 — Submit

Format: `boroCTF{ai_in_lowercase}` → use the model name without version number.

```
boroCTF{gemini}
```

---

## Flag

```
boroCTF{gemini}
```

---

## Key takeaways

- When asked to identify an AI-generated image, skip manual guessing — use a dedicated AI detector tool immediately
- **https://hivemoderation.com/ai-generated-content-detection** identifies not just "AI or not" but the specific generator with confidence percentages
- The format hint `ai_in_lowercase` suggests the model name without version number — `gemini` not `gemini3`
- EXIF/C2PA metadata is the first thing to check, but many AI generators (including Gemini) don't embed identifiable metadata in exported images
- With a low attempt limit (5), always verify with a tool before guessing — don't rely on visual style analysis alone
