.

# Roll your own IDE

Handl in stapled sheets showing your code and and input outpits. For large
data files, jsut show first 4 lines.

For support files, go to https://github.com/txt/guru26spr/tree/main/docs/submit/three

## BASE

1. Show this works:

```
make sh
🔆 parent/dir main* ▶
```
(note that parent/dir will show your dir and aprent dir names)

2. Add a banner that is printed before running the sh.


```
make sh
 ______   ______   _____   ______
/\  ___\ /\  __ \ /\  __-. /\  ___\
\ \ \____\ \ \/\ \\ \ \/\ \\ \  __\
 \ \_____\\ \_____\\ \____- \ \_____\
  \/_____/ \/_____/ \/____/  \/_____/

🔆 parent/dir main* ▶
```

3. Add make rules to  show date, list mae. Add them to the Makefile hep system:

```
🔆 parent/dir main* ▶ make

make

Usage:
  make <target>

targets:
  date             show date
  files            show files
  help             show help.
  push             save to cloud
  sh               run my shell
```


4. Document some Python code using the Pyhton pycco  package

You will have to install it first.  `pipx  install pycco`
or `pip install pycco`).

Try it on the [match.py](match.py) file included here.

```
🔆 parent/dir main* ▶ pycco -d ~/tmp match.py
pycco: match.py -> /Users/timm/tmp/match.html
```
make ~/tmp/match.html 
```


4. Data Quality 

## Background

The file `page_blocks_dirty.csv` describes 5491 page layout blocks extracted
from document images. Each row is one block; the class label says what kind
of block it is (text, horizontal line, picture, vertical line, graphic).

The dataset has been *deliberately seeded* with data-quality problems.
Your job is to find them.

## The Features

| Feature | Meaning |
|---------|---------|
| HEIGHT | block height in pixels |
| LENGHT | block length (width) in pixels |
| WIDTH | block width in pixels |
| AREA | block area in pixels |
| ECCEN | eccentricity (length / height) |
| P_BLACK | proportion of black pixels = BLACKPIX / AREA |
| P_AND | proportion of black-and-white pixels = BLACKAND / AREA |
| MEAN_TR | mean number of white-to-black transitions |
| BLACKPIX | total black pixels |
| BLACKAND | total black-and-white pixels |
| WB_TRANS | total white-to-black transitions |
| DATASET_ID | dataset identifier |
| class! | block type: 1=text, 2=horiz line, 3=picture, 4=vert line, 5=graphic |

## Domain Knowledge

Some checks are purely mechanical. Others require **domain knowledge** —
facts about what the data *should* look like that cannot be deduced from
the data alone. Here is the domain knowledge for this dataset.

### Derived-feature relationships (referential integrity)
- `AREA = HEIGHT × LENGHT`
- `ECCEN = LENGHT / HEIGHT` (rounding tolerance: 0.01)
- `P_BLACK = BLACKPIX / AREA` (tolerance: 0.001)
- `P_AND = BLACKAND / AREA` (tolerance: 0.001)

### Plausibility constraints
- HEIGHT, LENGHT, WIDTH, AREA, BLACKPIX, BLACKAND, WB_TRANS, MEAN_TR must all be **> 0**
- P_BLACK and P_AND are proportions so must be in **[0, 1]**
- ECCEN must be **> 0**
- `class!` must be one of **{1, 2, 3, 4, 5}**
- BLACKPIX ≤ BLACKAND (black pixels are a subset)

### What counts as missing
- In this file, missing values are encoded as **`?`**

---

## The Checks

### Part 1: gawk checks (no domain knowledge needed)

These are purely mechanical — one pass, no floating-point math, no
cross-column formulas. Each should be ≤ 5 lines of gawk.

| Target | What to count |
|--------|--------------|
| **S1** | **Ragged rows** — rows with a different number of fields than the header |
| **S2** | **Missing values** — report (a) which *columns* contain at least one `?` and (b) which *rows* contain at least one `?` |
| **S3** | **Constant columns** — columns where every row has the same value |
| **S4** | **Bad class labels** — rows where `class!` does not match `/^[1-5]$/` |
| **S5** | **Duplicate rows** — rows appearing more than once (count every copy) |

### Part 2: Python checks (domain knowledge required)

These need the referential integrity constraints and plausibility rules.
They involve floating-point tolerances, cross-column formulas, and
set-union aggregation.

#### Feature-level (report column names)

| Target | What to count |
|--------|--------------|
| **A** | **Identical features** — columns with the same values for every row. Report all columns in each identical group. |
| **B** | **Constant features** — same as S3 (reuse the result) |
| **C** | **Features with missing values** — same as S2 column list (reuse) |
| **D** | **Features with conflicting values** — columns involved in ≥1 violated referential integrity constraint |
| **E** | **Features with implausible values** — columns with ≥1 value violating a plausibility constraint |
| **F** | **Total problem features** — distinct columns hit by any of A–E. Note: F ≤ A+B+C+D+E since a column can have multiple problems. |

#### Case-level (report row numbers)

| Target | What to count |
|--------|--------------|
| **G** | **Identical cases** — same as S5 (reuse) |
| **H** | **Inconsistent cases** — rows identical on all features but with a different `class!` |
| **I** | **Cases with missing values** — same as S2 row list (reuse) |
| **J** | **Cases with conflicting values** — rows violating ≥1 referential integrity constraint (skip rows with `?` in involved fields) |
| **K** | **Cases with implausible values** — rows with ≥1 plausibility violation |
| **L** | **Total data-quality problem cases** — distinct rows hit by any of I–K. Note: L ≤ I+J+K. |
| **M** | **Total problem cases** — distinct rows hit by any of G–K. Note: M ≤ G+H+I+J+K. |

Note that B=S3, C=S2(columns), G=S5, I=S2(rows). Your Makefile should
reuse the gawk outputs rather than recompute them.

---

## Makefile Structure

```makefile
DATA = page_blocks_dirty.csv

all: out/S1 out/S2 out/S3 out/S4 out/S5 \
     out/A out/B out/C out/D out/E out/F \
     out/G out/H out/I out/J out/K out/L out/M

# ── Part 1: gawk ─────────────────────────────────
out/S1: $(DATA); mkdir -p out; gawk -f S1.awk $< > $@
out/S2: $(DATA); mkdir -p out; gawk -f S2.awk $< > $@
out/S3: $(DATA); mkdir -p out; gawk -f S3.awk $< > $@
out/S4: $(DATA); mkdir -p out; gawk -f S4.awk $< > $@
out/S5: $(DATA); mkdir -p out; gawk -f S5.awk $< > $@

# ── Part 2: python ───────────────────────────────
out/A: $(DATA);         mkdir -p out; python3 checks.py A $< > $@
out/B: out/S3;          cp $< $@
out/C: out/S2;          grep '^COL:' $< | sed 's/^COL://' > $@
out/D: $(DATA);         mkdir -p out; python3 checks.py D $< > $@
out/E: $(DATA);         mkdir -p out; python3 checks.py E $< > $@
out/F: out/A out/B out/C out/D out/E
	tail -n+2 $^ | grep -vE '^$$|^==>' | sort -u > $@

out/G: out/S5;          cp $< $@
out/H: $(DATA);         mkdir -p out; python3 checks.py H $< > $@
out/I: out/S2;          grep '^ROW:' $< | sed 's/^ROW://' > $@
out/J: $(DATA);         mkdir -p out; python3 checks.py J $< > $@
out/K: $(DATA);         mkdir -p out; python3 checks.py K $< > $@
out/L: out/I out/J out/K
	tail -n+2 $^ | grep -vE '^$$|^==>' | sort -un > $@
out/M: out/G out/H out/I out/J out/K
	tail -n+2 $^ | grep -vE '^$$|^==>' | sort -un > $@
```

**Output format convention**: line 1 is the count; remaining lines are
the identities (column names for feature checks, row numbers for case checks).
F, L, and M union these identity lines from their dependencies.

---

## Worked Example: gawk (S4 — bad class labels)

The class label is the last field (`$NF`). A legal label matches `/^[1-5]$/`.
Anything else — a `0`, a `7`, a `-1`, a blank — is a problem.

**S4.awk**:
```awk
BEGIN { FS = "," }
NR == 1 { next }
$NF !~ /^[1-5]$/ { n++; print NR }
END { print n + 0 > "/dev/stderr" }
```

That's it: skip the header, test the last field against a regex, print the
offending row number. The count goes to stderr so you can capture it separately
if you want, but the row numbers in stdout are what targets F/L/M need.

Running it:

```
$ gawk -f S4.awk page_blocks_dirty.csv > out/S4 2>&1
$ head out/S4
140
326
821
987
```

---

## Worked Example: Python (J — cases with conflicting feature values)

A row has conflicting values when a derived feature disagrees with its
formula. We check four constraints, each with its own tolerance. Rows
containing `?` in any relevant field are skipped (missing-ness is handled
by check I, not here).

**checks.py** (just the J function — your full script will dispatch on `sys.argv[1]`):

```python
import csv, sys

MISSING = '?'

def check_J(path):
    """Rows violating at least one referential integrity constraint."""
    with open(path) as f:
        rows = list(csv.DictReader(f))

    bad_rows = []
    for i, r in enumerate(rows):
        # skip if any field we need is missing
        needed = ['HEIGHT','LENGHT','AREA','ECCEN',
                  'P_BLACK','P_AND','BLACKPIX','BLACKAND']
        if any(r[c] == MISSING for c in needed):
            continue

        h   = float(r['HEIGHT']);  l  = float(r['LENGHT'])
        a   = float(r['AREA']);    e  = float(r['ECCEN'])
        pb  = float(r['P_BLACK']); pa = float(r['P_AND'])
        bpx = float(r['BLACKPIX']); ba = float(r['BLACKAND'])

        # four constraints
        if (a != h * l
            or (h > 0 and abs(e - l/h) > 0.01)
            or (a > 0 and abs(pb - bpx/a) > 0.001)
            or (a > 0 and abs(pa - ba/a)  > 0.001)):
            bad_rows.append(i + 2)          # +2: 1-indexed, skip header

    print(len(bad_rows))
    for r in bad_rows:
        print(r)
```

Key decisions visible in the code:

- **Tolerances**: exact integer match for AREA (no rounding), 0.01 for ECCEN,
  0.001 for the two proportions.
- **`i + 2`**: csv.DictReader is 0-indexed and skips the header, so row `i`
  is line `i + 2` in the file. This matters because the Makefile unions
  row numbers across targets.
- **Guard clauses**: `h > 0` and `a > 0` prevent division by zero.
  Rows with negative heights are caught by check K, not here.

---

## What to Submit

1. Your `Makefile`
2. Your `.awk` scripts (S1–S5)
3. Your `checks.py`
4. All output files (`out/S1`–`out/S5`, `out/A`–`out/M`)
5. A short `REPORT.md` (≤ 1 page) summarizing what you found
