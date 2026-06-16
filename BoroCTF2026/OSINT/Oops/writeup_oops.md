# boroCTF 2026 — Oops... (OSINT, 100pts)

**Author:** Solarity  
**Category:** OSINT  

## Description

> My friend (again) was telling me a story about how around two years ago, he may or may not have accidentally pushed a change to a file that disrupted millions of systems at an unprecedented scale.  
> What was the general name of the configuration file that he modified that broke everything?  
> Flag Format: `boroCTF{file_name_67}`

---

## Solution

### The CrowdStrike Incident (July 2024)

"Around two years ago" + "disrupted millions of systems at an unprecedented scale" = the **CrowdStrike global outage of July 19, 2024** — one of the largest IT outages in history.

CrowdStrike is a cybersecurity company providing an EDR (Endpoint Detection and Response) product called **Falcon**. Their agent runs on millions of enterprise Windows machines worldwide and receives automatic content updates called **channel files** — configuration/signature files that tell the agent how to detect threats.

On July 19, 2024, CrowdStrike pushed a faulty update to one of these channel files. The broken file caused the Falcon sensor to crash, which in turn caused Windows to BSOD (Blue Screen of Death) on boot — machines could not start at all.

**Scale of impact:**
- ~8.5 million Windows machines affected globally
- Airlines grounded flights (Delta, United, American)
- Hospitals had to revert to paper records
- Banks and financial systems went offline
- Emergency services disrupted in multiple countries

The specific file responsible was **Channel File 291** (`C-00000291-*.sys`).

The flag format includes the number: `boroCTF{channel_file_291}`.

---

## Flag

```
boroCTF{channel_file_291}
```

---

## Key takeaways

- The CrowdStrike outage is the largest IT outage in history caused by a faulty software update
- Channel files are configuration/signature files pushed automatically to security agents — when they break, they break silently and at scale
- EDR agents run at kernel level with high privileges — a crash there means a system crash
- "Around two years ago" + "unprecedented scale" + "configuration file" = CrowdStrike channel file 291
- Always read the flag format carefully — the example `boroCTF{file_name_67}` shows a number is expected
