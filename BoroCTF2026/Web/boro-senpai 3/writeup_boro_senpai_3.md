# boroCTF 2026 — boro-senpai 3 (Web, 200pts)

**Author:** Solarity  
**Category:** Web  

## Description

> ———— was an actress. A public figure. Then one day, she wasn't. Her AobaNet account — gone. Her name — scrubbed. The internet forgot she existed. But the internet doesn't actually delete things. Prove she existed.

## URL

`https://5l24ruh9miuo.boroctf.com/`

---

## Solution

### Step 1 — Identify the deleted account

The challenge is set in the Seishun Buta Yarou (Rascal Does Not Dream of Bunny Girl Senpai) universe. The site is a fictional social network called AobaNet. "Actress, scrubbed from the internet" is a description of **Mai Sakurajima**, the main character of the series.

Navigate to her profile:

```
https://5l24ruh9miuo.boroctf.com/profile/mai-sakurajima
```

The page returns HTTP 404 — "This account has been suspended or does not exist."

### Step 2 — Read the JavaScript source

Every page on the site loads `/static/main.js` via a `<script>` tag at the bottom of the HTML. Open it:

```
https://5l24ruh9miuo.boroctf.com/static/main.js
```

Inside, there is a moderator panel function that constructs a URL to fetch deleted profiles:

```javascript
var API_BASE = '/api/user/';

var url = API_BASE + encodeURIComponent(username) + '?' + window._modFlags.k + '=' + window._modFlags.v;
```

`API_BASE` is just a variable holding the base path — the full endpoint is `/api/user/<username>?<key>=<value>`. The key and value come from `window._modFlags`, which is a moderator-only object set by the page. We need to find out what those values are.

### Step 3 — Read `_modFlags` from the browser console

`window._modFlags` is only defined on certain pages — specifically the suspended account page. Navigate to:

```
https://5l24ruh9miuo.boroctf.com/profile/mai-sakurajima
```

Open DevTools (F12) → **Console** tab. The console is an interactive JavaScript interpreter running in the context of the current page — any variables the page has loaded into memory are accessible here.

Type:

```javascript
window._modFlags
```

Output:

```javascript
Object { k: "include_deleted", v: "true" }
```

Typing `window._modFlags` (without `.k` or `.v`) returns the whole object at once, giving us both the key and the value in one step.

### Step 4 — Build the URL and fetch the deleted profile

We now have everything needed to construct the full API URL:

```
/api/user/mai-sakurajima?include_deleted=true
```

Navigate to:

```
https://5l24ruh9miuo.boroctf.com/api/user/mai-sakurajima?include_deleted=true
```

The server returns the deleted profile as JSON. The flag is in the `mod_notes` field:

```
boroCTF{th@nk_y0u_y0u_d!d_w3ll_!_l0v3_y0U<3}
```

---

## Vulnerability: Broken Access Control + Information Disclosure

The application uses "soft delete" — accounts are never truly removed, only marked as `status: "deleted"` and hidden from regular users. A special API endpoint with `include_deleted=true` is meant to be accessible only to moderators.

The problem: the moderator credentials (`_modFlags`) are embedded in client-side JavaScript and set on the suspended account page itself — visible to anyone who opens the browser console. There is no server-side check that the person calling `/api/user/?include_deleted=true` is actually a moderator.

The description hint "the internet doesn't actually delete things" referred to this exact mechanism.

---

## Flag

```
boroCTF{th@nk_y0u_y0u_d!d_w3ll_!_l0v3_y0U<3}
```

---

## Key takeaways

- **Read the JS source before anything else** — DevTools → Debugger (or just open `/static/main.js` directly) reveals hidden endpoints and logic
- The browser **Console** tab is an interactive JS interpreter with full access to everything the page has loaded into memory — variables, functions, objects
- `window._modFlags` was only defined on the suspended account page, not on the homepage — context matters when reading variables from the console
- Soft-delete patterns (hiding data instead of deleting it) are only safe if the API enforces authorization server-side — client-side "moderator flags" are not a security control
