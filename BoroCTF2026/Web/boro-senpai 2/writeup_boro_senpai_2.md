# boroCTF 2026 — boro-senpai 2 (Web, 200pts)

**Author:** Solarity  
**Category:** Web  

## Description

> Maine's dead. Lucy's gone dark. David-... you know what happened. There's nothing we can do now. You're the last one standing with a half-finished contract and nothing left to lose. Arasaka's internal data relay is locked behind a blocklist — but their own NetPulse uptime checker is still live on the public net. Plug in. Pull the flag. Get out.

## URL

`https://4imc7nitr7ln.boroctf.com/`

---

## Solution

### Step 1 — Read the page source first

Before attempting any exploit, open DevTools (F12) → **Debugger** tab → find `script.js` in the file list on the left. At the top of the file there is a developer comment:

```javascript
// NOTE FOR DEVS: diagnostic probe routes through the proxy service.
// Internal nodes on mainframe-net (e.g. internal-api) are supposed to be
// shielded by the perimeter blocklist. Double-check filter coverage before prod.
```

This reveals the internal hostname: **`internal-api`**. Developer comments left in production code are a goldmine for attackers — they expose internal architecture that is never meant to be public.

### Step 2 — Understand the vulnerability

The page is an uptime checker ("Pulse Diagnostic") — it takes a URL, the server fetches it server-side, and returns the response. This is a classic **SSRF (Server-Side Request Forgery)** setup.

The Activity Log confirms a blocklist is active:
```
[BOOT] Restricted subnet blocklist active.
```

The blocklist blocks standard localhost representations (`127.0.0.1`, `localhost` etc.) — but it does not block internal hostnames like `internal-api`, which only resolve inside the server's private network.

### Step 3 — Exploit SSRF via internal hostname

Submit the following URL to the Pulse Diagnostic:

```
http://internal-api/flag
```

The server resolves `internal-api` on its internal network (where it is reachable), fetches the endpoint, and returns:

```json
{
  "classification": "TOP SECRET",
  "flag": "boroCTF{w1sh_w3_c0uld_g0_2_th3_m00n_t0g3th3r}",
  "message": "MAINFRAME BREACH CONFIRMED — CLASSIFIED DATA EXFILTRATED"
}
```

---

## Vulnerability: SSRF (Server-Side Request Forgery)

**Conceptually:** In a normal flow, you connect to a server and the server responds. In SSRF, you trick the server into making a request on your behalf:

```
Normal:  You → public server → internet
SSRF:    You → public server → internal network (that you can't reach directly)
```

A real-world analogy: you can't get into a company's warehouse because you don't have a badge. But you can call an employee and ask them to bring something out for you. The employee has access, you don't — but the result is the same.

In cloud environments this is especially dangerous: AWS and GCP servers have a special internal endpoint at `http://169.254.169.254/` that returns access keys to the entire infrastructure. Through SSRF, an attacker can steal those keys without any direct access to the server.

**In this challenge:** SSRF occurs when a server makes HTTP requests to destinations controlled by user input, without properly restricting which destinations are allowed. The attacker never connects to the internal network directly — they trick the server into doing it on their behalf.

The blocklist here only blocked IP-based representations of localhost. Internal DNS hostnames like `internal-api` were not on the blocklist, even though they resolve to internal addresses. This is a common bypass: blocklists that check for `127.0.0.1` and `localhost` but ignore internal service names.

---

## Flag

```
boroCTF{w1sh_w3_c0uld_g0_2_th3_m00n_t0g3th3r}
```

---

## Key takeaways

- **Always read the source before exploiting** — the hostname `internal-api` was in a developer comment in `script.js`. Checking DevTools → Debugger → JS files would have led straight to the flag
- Developer comments in production JavaScript are public — anything written there can be read by anyone
- SSRF blocklists that only block IP addresses often miss internal hostnames — always try service names like `internal-api`, `backend`, `api`, `admin` in addition to `127.0.0.1` bypasses
- The recon order should be: read source → robots.txt → response headers → only then start guessing
