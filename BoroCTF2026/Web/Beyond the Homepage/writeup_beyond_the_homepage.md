# boroCTF 2026 — Beyond the Homepage (Web, 100pts)

**Author:** Solarity  
**Category:** Web  

## Description

> There's more to what you see...  
> (Hint: You might want to use a tool that a developer might use)

## URL

`https://6ox3t3alzl51.boroctf.com/`

---

## Solution

### Step 1 — View the page source

The hint says "a tool that a developer might use" — the most basic developer tool for web is viewing the raw HTML source.

Two methods:

**Method 1 — View Page Source (Ctrl+U)**  
Opens a new tab with the raw HTML exactly as the server sent it, before any JavaScript runs or modifies the page. Best for finding hidden comments because you can see everything at once and search with Ctrl+F.

**Method 2 — DevTools (F12 or Ctrl+Shift+I)**  
Opens the browser's developer tools panel. Both shortcuts do the same thing and work across Chrome, Firefox, and Edge. This shows the DOM (Document Object Model) — the page as the browser has processed it. JavaScript may have already added or removed elements, so it doesn't always match the raw source. For static pages like this one, both methods give the same result.

> **Ctrl+U vs F12:** Ctrl+U shows what the server sent. F12 shows what the browser made of it. For CTF challenges, Ctrl+U is often more reliable because it shows the unmodified source.

### Step 2 — Find the flag

In the `<head>` section, right after the `<title>` tag:

```html
<title>boroCTF / Beyond the Webpage</title>
<!--boroCTF{d3v3l0peR_t001s}-->
```

The flag is hidden in an HTML comment — invisible on the rendered page but visible in the source.

---

## Flag

```
boroCTF{d3v3l0peR_t001s}
```

---

## Key takeaways

- HTML comments (`<!-- -->`) are invisible to the user but fully visible in page source — always check source on web challenges
- **Ctrl+U** — View Page Source: raw HTML as sent by the server, new tab, fully searchable. Works in Chrome, Firefox, Edge
- **F12** — DevTools: shows the live DOM after JavaScript processing. Same as Ctrl+Shift+I
- **Ctrl+Shift+I** — alternative shortcut for DevTools, identical to F12
- Ctrl+U and F12/Ctrl+Shift+I are universal across Chrome, Firefox, and Edge. Safari uses Option+Cmd+U for source view
