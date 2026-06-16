# boroCTF 2026 — The Shattered Needle (Forensics, 100pts)

**Author:** ForeverFlames  
**Category:** Forensics  

## Description

> Man I hate haystacks. Where is my needle!!!

## Files

- `the_haystack.zip`

---

## Solution

### Step 1 — Inspect the archive without extracting

```bash
unzip -l the_haystack.zip | head -20
unzip -l the_haystack.zip | wc -l
```

Output: ~110,000 lines — meaning tens of thousands of files across hundreds of directories. Do not extract blindly on `/mnt/c/` (NTFS).

### Step 2 — Check if flag is in filenames

```bash
unzip -l the_haystack.zip | grep -i "boro\|needle\|flag"
```

Nothing. Flag is inside file contents, not filenames.

### Step 3 — Extract to WSL home directory

```bash
mkdir ~/ctf/haystack
cp the_haystack.zip ~/ctf/haystack/
cd ~/ctf/haystack
unzip the_haystack.zip
```

### Step 4 — Search all file contents recursively

```bash
grep -r "boro" .
```

Finds first fragment:
```
./dir_33/sub_65/data_8.txt:Anomaly: [FLAG_FRAGMENT_1/5]: boroCTF{gr3p_
```

### Step 5 — Find all fragments

The author labeled each fragment with `FLAG_FRAGMENT` — use it as the search pattern:

```bash
grep -r "FLAG_FRAGMENT" .
```

Output:
```
FLAG_FRAGMENT_1/5: boroCTF{gr3p_
FLAG_FRAGMENT_2/5: 1s_y0ur_b3st_
FLAG_FRAGMENT_3/5: fr13nd_f0r_
FLAG_FRAGMENT_4/5: 1nc1d3nt_
FLAG_FRAGMENT_5/5: r3sp0ns3}
```

Assemble in order: `boroCTF{gr3p_1s_y0ur_b3st_fr13nd_f0r_1nc1d3nt_r3sp0ns3}`

---

## Flag

```
boroCTF{gr3p_1s_y0ur_b3st_fr13nd_f0r_1nc1d3nt_r3sp0ns3}
```

---

## Key takeaways

- `unzip -l` lists archive contents without extracting — always check first before extracting 100k files
- `grep -r "pattern" .` searches recursively through all files in the current directory — essential for haystack challenges
- `.` = current directory (same as `pwd` output) — use it as a shorthand in grep and other commands
- `FLAG_FRAGMENT` labels in files are put there by the challenge author, not by any tool — once you spot one, use it as your search pattern to find the rest
- Always assemble split flags yourself rather than asking an LLM — previous experience showed LLMs can misread similar characters (`1`/`l`/`i`)
- **Always work in `~/` (WSL home) for large extractions** — NTFS (`/mnt/c/`) causes slowdowns and I/O errors
