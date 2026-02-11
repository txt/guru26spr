# Data Quality Exercise: page_blocks_dirty.csv

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

## Domain Knowledge You Will Need

Some quality checks are purely mechanical (find duplicates, find blanks).
Others require **domain knowledge** — facts about what the data *should*
look like that cannot be deduced from the data alone.

Here is the domain knowledge for this dataset:

### Derived-feature relationships (referential integrity)
- `AREA = HEIGHT × LENGHT`
- `ECCEN = LENGHT / HEIGHT` (to within rounding tolerance of 0.01)
- `P_BLACK = BLACKPIX / AREA` (tolerance 0.001)
- `P_AND = BLACKAND / AREA` (tolerance 0.001)

### Plausibility constraints
- HEIGHT, LENGHT, WIDTH, AREA, BLACKPIX, BLACKAND, WB_TRANS, MEAN_TR must all be **> 0**
- P_BLACK and P_AND are proportions so must be in **[0, 1]**
- ECCEN must be **> 0**
- `class!` must be one of **{1, 2, 3, 4, 5}**
- BLACKPIX ≤ BLACKAND (black pixels are a subset)

### What counts as missing
- In this file, missing values are encoded as **`?`**

## Quality Checks A–M

Write a Makefile that detects the following problems. Each check should be
a separate Make target that writes its result to a file (e.g. `out/A`,
`out/B`, ..., `out/M`). Each output file should contain the **count** of
the relevant problem.

Use whatever scripting language you like (awk, python, etc.) inside
the Make rules.

| Target | What to count | Notes |
|--------|--------------|-------|
| **A** | Number of **identical features** — columns that contain the same values for every row | Count the *number of redundant columns* (if 3 columns are identical, 2 are redundant) |
| **B** | Number of **constant features** — columns where every row has the same value | |
| **C** | Number of **features with missing values** — columns that contain at least one `?` | |
| **D** | Number of **features with conflicting values** — columns involved in at least one violated referential-integrity constraint | See domain knowledge above for the constraints |
| **E** | Number of **features with implausible values** — columns that contain at least one value violating a plausibility constraint | See domain knowledge above |
| **F** | **Total problem features** — number of distinct columns affected by one or more of A–E | `F ≤ A+B+C+D+E` because a column may have multiple problems |
| **G** | Number of **identical cases** — rows that are exact duplicates of another row (count each duplicated row) | |
| **H** | Number of **inconsistent cases** — rows that are identical on all features *except* `class!` | |
| **I** | Number of **cases with missing values** — rows containing at least one `?` | |
| **J** | Number of **cases with conflicting feature values** — rows where at least one referential-integrity constraint is violated | |
| **K** | Number of **cases with implausible values** — rows containing at least one value that violates a plausibility constraint | |
| **L** | **Total data-quality problem cases** — distinct rows affected by one or more of I–K | `L ≤ I+J+K` |
| **M** | **Total problem cases** — distinct rows affected by one or more of G–K | `M ≤ G+H+I+J+K` |

## Makefile Structure

Your Makefile should look roughly like this:

```makefile
DATA = page_blocks_dirty.csv

all: out/A out/B out/C out/D out/E out/F \
     out/G out/H out/I out/J out/K out/L out/M

out/A: $(DATA)
	mkdir -p out
	python check_A.py $(DATA) > out/A    # or inline script

# F, L, M are aggregates:
out/F: out/A out/B out/C out/D out/E
	# combine the problem-feature sets from A–E, count distinct

out/L: out/I out/J out/K
	# combine the problem-case sets from I–K, count distinct

out/M: out/G out/H out/I out/J out/K
	# combine the problem-case sets from G–K, count distinct
```

**Important**: For targets F, L, and M you need to know *which* features
or cases are affected, not just the counts. So your intermediate targets
(A–E, G–K) should also write out the *identities* of the problem
features/cases (e.g. column names for A–E, row numbers for G–K) in
addition to the count.

## What to Submit

1. Your `Makefile`
2. Any scripts it calls
3. The 13 output files (`out/A` through `out/M`)
4. A short `REPORT.md` (≤ 1 page) summarizing what you found

## Hints

- `awk -F,` is your friend for quick column checks.
- For floating-point comparisons, use a tolerance (e.g. `abs(actual - expected) > 0.01`).
- For check A, compare every pair of columns — there are only 13 choose 2 = 78 pairs.
- For check G, sorting the file makes duplicates adjacent.
- For check H, sort by everything *except* `class!` and look for adjacent rows that match.
