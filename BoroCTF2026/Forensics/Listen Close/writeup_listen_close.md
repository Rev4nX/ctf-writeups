# boroCTF 2026 — Listen Close (Forensics, 200pts)

**Author:** Franklin  
**Category:** Forensics  

## Description

> Those who listen closely can read between the lines. It is not always what is being said but the meanings behind it.

## Files

- `chal.wav` — RIFF WAV audio, 16-bit mono, 48000 Hz

---

## Solution

### Step 1 — Standard recon

```bash
file chal.wav
# RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 48000 Hz

binwalk chal.wav
# (no output — no embedded files found)
```

`binwalk` returns nothing, meaning no hidden files with recognizable signatures. The data is in the audio itself.

### Step 2 — Read the hints

- **"Listen closely"** → audio file, pay attention to the signal
- **"Read between the lines"** → the flag is not in the audible content
- **"Not what is being said but the meanings behind it"** → visual representation of the audio

These all point to **spectrogram steganography** — hiding data visually in the frequency spectrum of the audio, where it's invisible to the ear but visible as an image.

### Step 3 — View the spectrogram in Audacity

1. Open `chal.wav` in Audacity
2. Click the dropdown arrow next to the track name
3. Select **Spectrogram**
4. The flag appears as white text written directly in the frequency domain

The spectrogram reveals: `BoroCTF{Sp3c^R0}`

---

## Flag

```
BoroCTF{Sp3c^R0}
```

---

## Key takeaways

- **Spectrogram steganography** — data encoded visually in the frequency spectrum of an audio file. The human ear cannot detect it, but rendering the spectrogram as an image reveals it instantly
- **Audacity** is the standard tool: open file → click track dropdown → Spectrogram
- **binwalk returning nothing** on an audio file is a signal to look at the audio content itself, not at embedded files
- The description "not what is being said but the meanings behind it" is a classic CTF hint for spectrogram — the "meaning" is visual, not audible
- This is a simpler variant of the technique — mono file, flag directly in the spectrum. More complex versions involve stereo channel subtraction (L−R) before viewing the spectrogram, which isolates hidden data from the audible signal
