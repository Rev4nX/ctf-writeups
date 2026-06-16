# boroCTF 2026 — NERV (Web, 200pts)

**Author:** Solarity  
**Category:** Web  

## Description

> NERV HQ internal systems remain online following the Third Impact preliminary event. You have been assigned clearance level 2. This is sufficient. Do not look for what you have not been given access to. Credentials have been issued. ikari : eva01

## URL

`https://xqpmkotuq78s.boroctf.com/`

---

## Solution

### Step 1 — Log in

Use the provided credentials: `ikari` / `eva01`. This gives access to the NERV Personnel Portal dashboard with Clearance LVL-2.

### Step 2 — Check robots.txt

`robots.txt` is a file at the root of every web server that tells search engine crawlers which paths they should not index. It is a polite request, not a technical restriction — any visitor (or attacker) can freely access the listed paths. In CTF challenges, `robots.txt` often reveals hidden admin panels or sensitive endpoints.

Navigate to:

```
https://xqpmkotuq78s.boroctf.com/robots.txt
```

Contents:

```
User-agent: *
Disallow: /admin/reports
```

### Step 3 — Access the hidden admin panel

Navigate directly to the disallowed path:

```
https://xqpmkotuq78s.boroctf.com/admin/reports
```

This reveals a "MAGI SYSTEM — MELCHIOR-1" report query terminal. The system status panel at the bottom confirms:

- **TEMPLATE ENGINE: ACTIVE**
- **AUTH LAYER: DISABLED**
- **CLEARANCE CHECK: BYPASSED**

The description also says: "QUERIES ARE EVALUATED AGAINST NERV PERSONNEL ARCHIVE" — the word *evaluated* means user input is executed, not just displayed.

### Step 4 — Confirm SSTI

Server-Side Template Injection (SSTI) occurs when user input is embedded directly into a template and executed by the template engine. The classic test is `{{7*7}}` — Jinja2 template syntax for an expression. If the server executes it and returns `49` instead of the literal string `{{7*7}}`, SSTI is confirmed.

Enter `{{7*7}}` in the query field and click Execute Query.

Output: **49** ✓ — Jinja2 is running on the backend and executing our input.

### Step 5 — Exploit SSTI to read the flag

In Jinja2 (Python/Flask), you can chain object attributes to climb through Python's internals and reach the `os` module, which allows executing arbitrary system commands.

Payload:

```
{{request.application.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read()}}
```

Breaking it down step by step:

- **`request.application`** — In Flask, `request` is always available in Jinja2 templates. `.application` is the Flask application object — our entry point into Python internals.
- **`.__globals__`** — Every Python function has a `__globals__` dict containing all global variables in the module where that function lives. This is how we escape the sandboxed template context.
- **`.__builtins__`** — Python's built-in functions (`print`, `len`, `__import__`...). Normally inaccessible from a Jinja2 template, but reachable via `__globals__`.
- **`.__import__('os')`** — Imports the `os` module — Python's standard library for OS operations. Equivalent to `import os` in a normal Python script, but reached through the back door.
- **`.popen('cat /flag.txt')`** — Opens a subprocess running `cat /flag.txt`, exactly as if typed in a terminal. `popen` = "process open".
- **`.read()`** — Reads the output of that subprocess and returns it as a string, which Jinja2 renders into the page output.

Output: `boroCTF{c0ngr@tulat!0nS*}`

---

## Why SSTI is dangerous

The attack starts from "display a variable in a template" and ends at "execute arbitrary commands on the server." Once you can run `os.popen()`, you can read any file, list directories, or in a real attack — establish a reverse shell. The vulnerability exists because the application passes untrusted user input directly to the template engine without sanitization.

---

## Flag

```
boroCTF{c0ngr@tulat!0nS*}
```

---

## Key takeaways

- **Always check `robots.txt`** — it often lists paths the site owner doesn't want indexed, which are exactly the paths worth visiting in a CTF
- `robots.txt` is a convention, not a security control — listing a path there does not prevent access
- **SSTI test:** `{{7*7}}` → if output is `49`, Jinja2 is evaluating your input
- The full exploit chain: Flask `request` object → `__globals__` → `__builtins__` → `__import__('os')` → `popen()` → arbitrary command execution
- SSTI on Jinja2/Flask is one of the most critical web vulnerabilities — it gives direct OS-level access to the server
