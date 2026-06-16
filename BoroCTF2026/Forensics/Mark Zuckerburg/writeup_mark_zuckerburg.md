# boroCTF 2026 — Mark Zuckerburg (Forensics, 100pts)

**Author:** Franklin  
**Category:** Forensics  

## Description

> Mark (from Meta) called me the other day and attached this photo. He told me he needed to remember what model camera he took his picture with. Could you help him?

## Files

- `Mark-Zuckerberg.png` — PNG image with embedded metadata

---

## Solution

The challenge asks for the camera model — a direct hint to check **EXIF/image metadata**. Run `exiftool`:

```bash
exiftool Mark-Zuckerberg.png
```

Among the output fields:

```
Camera Model Name  : boroCTF{M3+a_d@ta_1s_M7_Fa40rite}
Make               : Sonya
User Comment       : I LOVE my new job at meta
Date/Time Original : 2190:02:10 12:53:41.947
```

The flag is stored directly in the `Camera Model Name` EXIF field.

---

## Flag

```
boroCTF{M3+a_d@ta_1s_M7_Fa40rite}
```

---

## What is EXIF?

**EXIF** (Exchangeable Image File Format) is a standard for embedding metadata inside image files (JPEG, PNG, TIFF, etc.). It is not a separate file — it is a data chunk stored within the image itself. Originally designed so cameras could record technical shooting information alongside the photo.

Typical EXIF fields: camera make and model, focal length, shutter speed, ISO, GPS coordinates, and timestamp. Any of these can be abused in CTF challenges to hide a flag.

**`exiftool`** takes its name from the EXIF standard, which was designed specifically for image files and is most commonly found there — but the name is somewhat misleading, because the tool reads and writes metadata from dozens of file formats — not just images. PDF, Office documents (docx, xlsx, pptx), MP3, MP4, and more. On Office files it often reveals the author's name, company, edit history, and sometimes full file paths from the author's machine (`C:\Users\name\Documents\...`), making it useful for OSINT as well.

## Key takeaways

- **"What model camera" = check EXIF** — the challenge description is a direct pointer to metadata
- `exiftool <file>` is the first tool to run on any image in a Forensics challenge
- EXIF fields can contain anything the author writes — flags, fake dates (year 2190), custom comments
- `exiftool` works far beyond images: PDF, Office, audio, video — always worth running on any unknown file
