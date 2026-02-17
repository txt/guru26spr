<p align="center">
  <a href="https://github.com/txt/guru26spr/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/docs/lect/syllabus.md"><img 
      src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/1xZfIwkmu6hTJjXico1zIzklt1Tl9-L9j9uHrix9KToU/edit?usp=sharing"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8119"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591: How to be a SE Guru <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/guru26spr/refs/heads/main/etc/img/banenr.png"> 

# Roll your own IDE

Hand in stapled sheets showing your code and input/outputs. For large
data files, just show first 4 lines.

For support files, go to https://github.com/txt/guru26spr/tree/main/docs/submit/three

 
## What to Submit

1. Your `Makefile`
2. Your `.awk` scripts (S1–S5)
3. Your `checks.py`
4. All output files (`out/S1`–`out/S5`, `out/A`–`out/M`)
5. A short `REPORT.md` (≤ 1 page) summarizing what you found


Everyone:
- do the gawk questions this week (see S1,S2,S3,S4,S5, below)
- hand in A,B,C,D,E,G, in 2 weeks (see below)

Grad students
- hand in A...M in 2 weeks ( see below)

## 1. Show this works:

```
make sh
🔆 parent/dir main* ▶
```
Note that parent/dir will show your dir and parent dir names.

Also, for windows users, tput may not run. If so then inside `etc/ell`
change lines with tput to...

```
bold="\033[1m"
col0="\033[0m"       # reset
col1="\033[36m"      # cyan
col2="\033[33m"      # yellow
```

## 2. Add a banner that is printed before running the sh. Change the banner to "think + do".


```
make sh
 ______   ______   _____   ______
/\  ___\ /\  __ \ /\  __-. /\  ___\
\ \ \____\ \ \/\ \\ \ \/\ \\ \  __\
 \ \_____\\ \_____\\ \____- \ \_____\
  \/_____/ \/_____/ \/____/  \/_____/

🔆 parent/dir main* ▶
```

## 3. Add make rules to  show date, list files. Add them to the Makefile help system:

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


## 4. Document some Python code using the Python pycco  package

You will have to install it first.  `pipx  install pycco`
or `pip install pycco`).

Try it on the [match.py](match.py) file included here.

```
🔆 parent/dir main* ▶ pycco -d ~/tmp match.py
pycco: match.py -> /Users/timm/tmp/match.html
```

```
🔆 parent/dir main* ▶ make ~/tmp/match.html 
pycco: match.py -> /Users/timm/tmp/match.html
```

Modify the rule so that `"echo 'p {text-align: right}"` is always appended to ~/tmp/pycco.css
(so explanation text moves closer to the code it explains).

<img width="968" height="344" alt="image" src="https://github.com/user-attachments/assets/07d208e1-e670-4a32-b117-05a93b5dddac" />


## 5. Data Quality  (Big Task)

For HW3, implement S1...S5 (the gawk stuff) and A--M (the python stuff).


**Background**

The file [page_blocks_dirty.csv](page_blocks_dirty.csv) describes 5491 page layout blocks extracted
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

**Domain Knowledge**

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

### Part 2: Python checks (domain knowledge & statistics)

These checks require floating-point math, statistics, and cross-column
reasoning that goes beyond what gawk does well.

**Important**: no external packages! Use only `csv`, `sys`, `math`.
Computing mean, standard deviation, and correlation from scratch is part
of the exercise.

#### Mini Python tutorials

Before you start, here are the building blocks you'll need. Each is just
a few lines of plain Python — no imports beyond `math.sqrt`.

**Mean** — the average value of a list:

```python
def mean(xs):
    return sum(xs) / len(xs)
```

**Standard deviation** — how spread out the values are.  We use the
*population* formula (divide by n, not n−1) since we're describing
this dataset, not estimating a population parameter:

```python
from math import sqrt

def sd(xs):
    mu = mean(xs)
    return sqrt(sum((x - mu)**2 for x in xs) / len(xs))
```

**Pearson correlation** — measures how linearly related two columns are.
Returns a value between −1 and +1.  When |r| is close to 1 the columns
move in lockstep; when it's 0 they're unrelated:

```python
def pearson(xs, ys):
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx  = sum((x - mx)**2 for x in xs)
    dy  = sum((y - my)**2 for y in ys)
    if dx == 0 or dy == 0:
        return 0
    return num / sqrt(dx * dy)
```

These three functions are all you need for checks B, C, G, and I below.

---

#### Feature-level (report column names)

| Target | What to count |
|--------|--------------|
| **A** | **Identical features** — columns with the same values for every row. Report all columns in each identical group. |
| **B** | **Correlated features** — pairs of numeric features with Pearson \|r\| > 0.95. Report both column names in each pair. |
| **C** | **Outlier features** — columns that contain at least one value more than 3 standard deviations from the column mean (μ ± 3σ). |
| **D** | **Features with conflicting values** — columns involved in ≥1 violated referential integrity constraint |
| **E** | **Features with implausible values** — columns with ≥1 value violating a plausibility constraint |
| **F** | **Total problem features** — distinct columns hit by any of A–E. Note: F ≤ A+B+C+D+E since a column can have multiple problems. |

#### Case-level (report row numbers)

| Target | What to count |
|--------|--------------|
| **G** | **Outlier cases** — rows containing at least one value more than 3σ from the column mean. (The row-level dual of check C.) |
| **H** | **Inconsistent cases** — rows identical on all features but with a different `class!` |
| **I** | **Class-conditional outlier cases** — *within each class*, rows containing at least one value more than 3σ from the *class-specific* mean. A row can look normal globally but be a freak for its class. |
| **J** | **Cases with conflicting values** — rows violating ≥1 referential integrity constraint (skip rows with `?` in involved fields) |
| **K** | **Cases with implausible values** — rows with ≥1 plausibility violation |
| **L** | **Total data-quality problem cases** — distinct rows hit by any of G–K. |
| **M** | **Total problem cases** — same as L here (since all case checks are G–K). Kept for symmetry with F. |

Every Python target in Part 2 is distinct from every gawk target in
Part 1.  There is no overlap and no reuse between the two parts.

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

# ── Part 2: python ────────────────────────────────
out/A: $(DATA);         mkdir -p out; python3 checks.py A $< > $@
out/B: $(DATA);         mkdir -p out; python3 checks.py B $< > $@
out/C: $(DATA);         mkdir -p out; python3 checks.py C $< > $@
out/D: $(DATA);         mkdir -p out; python3 checks.py D $< > $@
out/E: $(DATA);         mkdir -p out; python3 checks.py E $< > $@
out/F: out/A out/B out/C out/D out/E
	tail -n+2 $^ | grep -vE '^$$|^==>' | sort -u > $@

out/G: $(DATA);         mkdir -p out; python3 checks.py G $< > $@
out/H: $(DATA);         mkdir -p out; python3 checks.py H $< > $@
out/I: $(DATA);         mkdir -p out; python3 checks.py I $< > $@
out/J: $(DATA);         mkdir -p out; python3 checks.py J $< > $@
out/K: $(DATA);         mkdir -p out; python3 checks.py K $< > $@
out/L: out/G out/H out/I out/J out/K
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
by check S2, not here).

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
