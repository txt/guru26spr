<p align="center">
  <a href="https://github.com/txt/guru26spr/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/docs/lect/syllabus.md"><img 
      src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/1xZfIwkmu6hTJjXico1zIzklt1Tl9-L9j9uHrix9KToU/edit?usp=sharing"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8118&bp=s"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591: How to be a SE Guru <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/guru26spr/refs/heads/main/etc/img/banenr.png"> 


# SE Design Heuristics Tutorial
## From Monolithic to Modular: A Grade Calculator Case Study

---

## Part 1: The Original "Before" Code

Here's working code that calculates student grades, applies
a curve, and prints a report:

```python
#!/usr/bin/env python3 -B
"""grades.csv: student grade calculator with curve"""
from math import sqrt
from types import SimpleNamespace as obj

def Sym(): return obj(it=Sym, n=0, has={})
def Num(): return obj(it=Num, n=0, mu=0, m2=0)
def add(i, v):
  if v != "?":
    i.n += 1
    if Sym is i.it: i.has[v] = 1 + i.has.get(v, 0)
    else: d = v - i.mu; i.mu += d / i.n; i.m2 += d * (v - i.mu)
  return v
def adds(src, i=None): i = i or Num(); [add(i, v) for v in src]; return i
def sd(num): return 0 if num.n < 2 else sqrt(num.m2 / (num.n - 1))
def coerce(s):
  try: return int(s)
  except: 
    try: return float(s)
    except: return s.strip()
def csv(file):
  with open(file) as f:
    for line in f:
      if line := line.strip(): yield [coerce(x) for x in line.split(",")]

def process_grades(file="grades.csv"):
  rows = list(csv(file))  
  header = rows[0]
  students = rows[1:]
  print(f"\n{'='*60}")   
  print(f"GRADE REPORT - {len(students)} students")
  print(f"{'='*60}\n")
  raw_scores = []   
  for student in students:
    name = student[0]
    hw1, hw2, hw3 = student[1], student[2], student[3]
    midterm, final = student[4], student[5]
    hw_avg = (hw1 + hw2 + hw3) / 3 if hw1 != "?" else 0
    raw = 0.3 * hw_avg + 0.3 * midterm + 0.4 * final
    raw_scores.append(raw)
  scores_stat = Num()   
  for score in raw_scores: add(scores_stat, score)
  mean, stdev = scores_stat.mu, sd(scores_stat)
  print(f"Class Statistics (before curve):")  
  print(f"  Mean: {mean:.1f}")
  print(f"  Std Dev: {stdev:.1f}\n")
  target_mean, target_std = 75, 10   
  curved_scores = []
  for raw in raw_scores:
    z_score = (raw - mean) / stdev if stdev > 0 else 0
    curved = target_mean + z_score * target_std
    curved_scores.append(curved)
  print(f"Individual Reports:\n")  
  letter_counts = Sym()
  for i, student in enumerate(students):
    name, curved = student[0], curved_scores[i]
    if curved >= 90: letter = "A"
    elif curved >= 80: letter = "B"
    elif curved >= 70: letter = "C"
    elif curved >= 60: letter = "D"
    else: letter = "F"
    add(letter_counts, letter)
    print(f"  {name:20} Raw: {raw_scores[i]:5.1f}  "   
          f"Curved: {curved:5.1f}  Grade: {letter}")
  print(f"\n{'='*60}")   
  print(f"Grade Distribution:")
  for grade in ["A", "B", "C", "D", "F"]:
    count = letter_counts.has.get(grade, 0)
    pct = 100 * count / len(students) if len(students) > 0 else 0
    bar = "*" * int(pct / 2)
    print(f"  {grade}: {count:2} ({pct:4.1f}%) {bar}")
  print(f"{'='*60}\n")

process_grades("grades.csv")
```

**74 lines total. The problematic function is 45 lines.**

---

### Exercise: Code Review

Before reading further, examine `process_grades` and answer:

1. **What would you change?** List 3-5 issues.
2. **Why change them?** What problems do they cause?
3. **What are the trade-offs?** What might get worse?

Write your answers, then continue.

---

## Part 2: Design Rules and Detailed Examples

### Rule 1: Separation of Concerns (SoC)

**Principle:** Software has layers of responsilities. E.g. database, model, GUII.
Don't pollute (e.g.) model with (e.g.) presentation layer.

**Why?**
- Business logic reusable (CLI, GUI, API, tests)
- Can change output format without touching logic
- Can test logic without capturing stdout
- Pure functions easier to reason about
- **This is THE non-negotiable rule**

**The Violation - Printing Scattered Throughout Logic:**

```python
def process_grades(file="grades.csv"):
  rows = list(csv(file))
  header = rows[0]
  students = rows[1:]
  
  # PRINTING mixed with setup
  print(f"\n{'='*60}")
  print(f"GRADE REPORT - {len(students)} students")
  print(f"{'='*60}\n")
  
  # LOGIC: Compute raw scores
  raw_scores = []
  for student in students:
    name = student[0]
    hw1, hw2, hw3 = student[1], student[2], student[3]
    midterm, final = student[4], student[5]
    hw_avg = (hw1 + hw2 + hw3) / 3 if hw1 != "?" else 0
    raw = 0.3 * hw_avg + 0.3 * midterm + 0.4 * final
    raw_scores.append(raw)
  
  # LOGIC: Compute statistics
  scores_stat = Num()
  for score in raw_scores: add(scores_stat, score)
  mean, stdev = scores_stat.mu, sd(scores_stat)
  
  # PRINTING mixed with processing
  print(f"Class Statistics (before curve):")
  print(f"  Mean: {mean:.1f}")
  print(f"  Std Dev: {stdev:.1f}\n")
  
  # LOGIC: Apply curve
  target_mean, target_std = 75, 10
  curved_scores = []
  for raw in raw_scores:
    z_score = (raw - mean) / stdev if stdev > 0 else 0
    curved = target_mean + z_score * target_std
    curved_scores.append(curved)
  
  # PRINTING mixed with grading
  print(f"Individual Reports:\n")
  letter_counts = Sym()
  for i, student in enumerate(students):
    name, curved = student[0], curved_scores[i]
    if curved >= 90: letter = "A"
    elif curved >= 80: letter = "B"
    elif curved >= 70: letter = "C"
    elif curved >= 60: letter = "D"
    else: letter = "F"
    add(letter_counts, letter)
    print(f"  {name:20} Raw: {raw_scores[i]:5.1f}  "
          f"Curved: {curved:5.1f}  Grade: {letter}")
  
  # PRINTING at the end
  print(f"\n{'='*60}")
  print(f"Grade Distribution:")
  for grade in ["A", "B", "C", "D", "F"]:
    count = letter_counts.has.get(grade, 0)
    pct = 100 * count / len(students)
    bar = "*" * int(pct / 2)
    print(f"  {grade}: {count:2} ({pct:4.1f}%) {bar}")
  print(f"{'='*60}\n")
```

**Problems this causes:**

1. **Can't reuse for API:**
   ```python
   @app.get("/grades")
   def api_grades():
     # Can't use process_grades - it prints!
     # Have to duplicate all the logic
   ```

2. **Can't test without mocking:**
   ```python
   def test_curve():
     # Prints to stdout, have to capture it
     import io, sys
     captured = io.StringIO()
     sys.stdout = captured
     process_grades("test.csv")
     sys.stdout = sys.__stdout__
     # Gross!
   ```

3. **Can't change output format:**
   ```python
   # Want JSON output? Have to edit the 45-line function
   # Want GUI table? Can't use it at all
   # Want email report? Duplicate everything
   ```

**The Fix - Complete Separation:**

```python
#--- MODEL LAYER (Pure business logic, no I/O) ---

def computeRawScore(hw1, hw2, hw3, midterm, final):
  """Pure function: numbers in, number out"""
  hw_avg = (hw1 + hw2 + hw3) / 3 if hw1 != "?" else 0
  return 0.3 * hw_avg + 0.3 * midterm + 0.4 * final

def applyCurve(raw_scores):
  """Pure function: scores in, curved scores out"""
  stats = adds(raw_scores, Num())
  mean, stdev = stats.mu, sd(stats)
  target_mean, target_std = 75, 10
  curved = []
  for raw in raw_scores:
    z = (raw - mean) / stdev if stdev > 0 else 0
    curved.append(target_mean + z * target_std)
  return curved, mean, stdev

def processGrades(file):
  """Returns data structure, no printing"""
  students = []
  raw_scores = []
  for row in csv(file):
    if not students:  # header row
      continue
    name = row[0]
    raw = computeRawScore(row[1], row[2], row[3], row[4], row[5])
    students.append((name, raw))
    raw_scores.append(raw)
  
  curved_scores, mean, stdev = applyCurve(raw_scores)
  
  results = []
  for i, (name, raw) in enumerate(students):
    curved = curved_scores[i]
    letter = letterGrade(curved)
    results.append(obj(name=name, raw=raw, curved=curved, 
                       letter=letter))
  
  return obj(students=results, mean=mean, stdev=stdev)

#--- PRESENTATION LAYER (I/O only, no logic) ---

def showHeader(n):
  """Just prints, no logic"""
  print(f"\n{'='*60}")
  print(f"GRADE REPORT - {n} students")
  print(f"{'='*60}\n")

def showStats(mean, stdev):
  """Just prints, no logic"""
  print(f"Class Statistics (before curve):")
  print(f"  Mean: {mean:.1f}")
  print(f"  Std Dev: {stdev:.1f}\n")

def showStudent(student):
  """Just prints, no logic"""
  print(f"  {student.name:20} Raw: {student.raw:5.1f}  "
        f"Curved: {student.curved:5.1f}  Grade: {student.letter}")

def showDistribution(students):
  """Just prints, no logic"""
  counts = Sym()
  for s in students: add(counts, s.letter)
  print(f"\n{'='*60}")
  print(f"Grade Distribution:")
  for grade in ["A", "B", "C", "D", "F"]:
    count = counts.has.get(grade, 0)
    pct = 100 * count / len(students) if len(students) > 0 else 0
    bar = "*" * int(pct / 2)
    print(f"  {grade}: {count:2} ({pct:4.1f}%) {bar}")
  print(f"{'='*60}\n")

def report(result):
  """Orchestrates presentation, calls pure functions"""
  showHeader(len(result.students))
  showStats(result.mean, result.stdev)
  print(f"Individual Reports:\n")
  for student in result.students:
    showStudent(student)
  showDistribution(result.students)
```

**Now we can:**

1. **Use for API:**
   ```python
   @app.get("/grades")
   def api_grades():
     result = processGrades("grades.csv")
     return [{"name": s.name, "grade": s.letter, 
              "score": s.curved} for s in result.students]
   ```

2. **Test cleanly:**
   ```python
   def test_curve():
     result = processGrades("test.csv")
     assert result.mean > 70
     assert result.students[0].letter == "A"
     # No stdout capturing needed!
   ```

3. **Multiple output formats:**
   ```python
   # CLI (original)
   report(processGrades("grades.csv"))
   
   # JSON
   result = processGrades("grades.csv")
   print(json.dumps([vars(s) for s in result.students]))
   
   # Email
   result = processGrades("grades.csv")
   send_email(format_as_html(result))
   
   # GUI
   result = processGrades("grades.csv")
   table.load_data(result.students)
   ```

---

### Rule 2: Single Responsibility Principle (SRP)

**Principle:** Each function does ONE thing.

**Why?**
- Changes to one concern don't affect others
- Reusable in different contexts
- Function name clearly states what it does
- Testing one thing is easier than testing everything

**The Violation - One Function Does EVERYTHING:**

```python
def process_grades(file="grades.csv"):
  # RESPONSIBILITY 1: Load data
  rows = list(csv(file))
  students = rows[1:]
  
  # RESPONSIBILITY 2: Print header
  print(f"\n{'='*60}")
  print(f"GRADE REPORT - {len(students)} students")
  
  # RESPONSIBILITY 3: Compute raw scores
  raw_scores = []
  for student in students:
    hw_avg = (student[1] + student[2] + student[3]) / 3
    raw = 0.3 * hw_avg + 0.3 * student[4] + 0.4 * student[5]
    raw_scores.append(raw)
  
  # RESPONSIBILITY 4: Compute statistics
  scores_stat = Num()
  for score in raw_scores: add(scores_stat, score)
  
  # RESPONSIBILITY 5: Print statistics
  print(f"Class Statistics...")
  
  # RESPONSIBILITY 6: Apply curve
  curved_scores = []
  for raw in raw_scores:
    z = (raw - mean) / stdev
    curved_scores.append(target_mean + z * target_std)
  
  # RESPONSIBILITY 7: Assign letter grades
  for i, student in enumerate(students):
    if curved >= 90: letter = "A"
    elif curved >= 80: letter = "B"
    # ...
  
  # RESPONSIBILITY 8: Print individual reports
  print(f"  {name:20} Raw: {raw}...")
  
  # RESPONSIBILITY 9: Compute distribution
  letter_counts = Sym()
  for student in students:
    add(letter_counts, letter)
  
  # RESPONSIBILITY 10: Print distribution
  print(f"Grade Distribution:")
```

**45 lines doing TEN different things!**

**The Fix - Each Function Has ONE Job:**

```python
# RESPONSIBILITY 1: Compute one student's raw score
def computeRawScore(hw1, hw2, hw3, midterm, final):
  hw_avg = (hw1 + hw2 + hw3) / 3 if hw1 != "?" else 0
  return 0.3 * hw_avg + 0.3 * midterm + 0.4 * final

# RESPONSIBILITY 2: Apply curve to all scores
def applyCurve(raw_scores):
  stats = adds(raw_scores, Num())
  mean, stdev = stats.mu, sd(stats)
  target_mean, target_std = 75, 10
  curved = []
  for raw in raw_scores:
    z = (raw - mean) / stdev if stdev > 0 else 0
    curved.append(target_mean + z * target_std)
  return curved, mean, stdev

# RESPONSIBILITY 3: Assign letter grade to one score
def letterGrade(score):
  for cutoff, grade in [(90,"A"), (80,"B"), (70,"C"), (60,"D")]:
    if score >= cutoff: return grade
  return "F"

# RESPONSIBILITY 4: Process all grades
def processGrades(file):
  students, raw_scores = [], []
  for row in csv(file):
    if not students: continue  # skip header
    name = row[0]
    raw = computeRawScore(row[1], row[2], row[3], row[4], row[5])
    students.append((name, raw))
    raw_scores.append(raw)
  curved_scores, mean, stdev = applyCurve(raw_scores)
  results = []
  for i, (name, raw) in enumerate(students):
    curved = curved_scores[i]
    results.append(obj(name=name, raw=raw, curved=curved,
                       letter=letterGrade(curved)))
  return obj(students=results, mean=mean, stdev=stdev)

# RESPONSIBILITY 5: Print header
def showHeader(n):
  print(f"\n{'='*60}")
  print(f"GRADE REPORT - {n} students")
  print(f"{'='*60}\n")

# RESPONSIBILITY 6: Print statistics
def showStats(mean, stdev):
  print(f"Class Statistics (before curve):")
  print(f"  Mean: {mean:.1f}")
  print(f"  Std Dev: {stdev:.1f}\n")

# RESPONSIBILITY 7: Print one student
def showStudent(student):
  print(f"  {student.name:20} Raw: {student.raw:5.1f}  "
        f"Curved: {student.curved:5.1f}  Grade: {student.letter}")

# RESPONSIBILITY 8: Print distribution
def showDistribution(students):
  counts = Sym()
  for s in students: add(counts, s.letter)
  print(f"\n{'='*60}")
  print(f"Grade Distribution:")
  for grade in ["A", "B", "C", "D", "F"]:
    count = counts.has.get(grade, 0)
    pct = 100 * count / len(students) if len(students) > 0 else 0
    print(f"  {grade}: {count:2} ({pct:4.1f}%) {bar}")
  print(f"{'='*60}\n")

# RESPONSIBILITY 9: Orchestrate presentation
def report(result):
  showHeader(len(result.students))
  showStats(result.mean, result.stdev)
  print(f"Individual Reports:\n")
  for student in result.students:
    showStudent(student)
  showDistribution(result.students)
```

**Now:** Each function has a clear, single purpose. Want to
change how letter grades are computed? Edit ONE function.
Want to add weighted categories? Edit ONE function. Want a
different report format? Edit presentation layer only.

---

### Rule 3: Mechanism vs Policy

**Principle:** Separate rules (policy) from their 
enforcement (mechanism).

**Eric Raymond (The Art of Unix Programming):**
*"Fold knowledge into data, so program logic can be 
stupid and robust."*

**Why?**
- Change rules without changing code
- Rules can be loaded from config files
- Different contexts can use different rules
- Testing all edge cases becomes trivial
- Business users can modify rules

**The Violation - Policy Hardcoded in Logic:**

```python
def process_grades(file="grades.csv"):
  # ... processing ...
  
  for i, student in enumerate(students):
    name, curved = student[0], curved_scores[i]
    
    # POLICY HARDCODED: Grading thresholds buried in if/elif
    if curved >= 90:      # A threshold
      letter = "A"
    elif curved >= 80:    # B threshold  
      letter = "B"
    elif curved >= 70:    # C threshold
      letter = "C"
    elif curved >= 60:    # D threshold
      letter = "D"
    else:
      letter = "F"
    
    add(letter_counts, letter)
    print(f"  {name:20} ... Grade: {letter}")
```

**Problems:**

1. **Can't change grading scale without editing code:**
   ```python
   # Want more generous grading? Edit if/elif chain
   # Different scale for graduate class? Duplicate function
   # Instructor wants 93+ for A? Edit code
   ```

2. **Can't test all thresholds easily:**
   ```python
   # Have to test: 89.9, 90.0, 79.9, 80.0, etc.
   # Each test needs full context of if/elif chain
   ```

3. **Can't load policy from config:**
   ```python
   # grading_policy.json:
   # {"A": 90, "B": 80, "C": 70}
   # Can't use it! Policy is in code
   ```

**The Fix - Data-Driven Policy:**

```python
# POLICY (data - easy to change, load from file, parameterize)
THRESHOLDS = [
  (90, "A"),
  (80, "B"),
  (70, "C"),
  (60, "D"),
  (0,  "F")
]

# MECHANISM (code - stays the same regardless of policy)
def letterGrade(score, thresholds=THRESHOLDS):
  """Find first threshold where score >= cutoff"""
  for cutoff, grade in thresholds:
    if score >= cutoff:
      return grade
  return "F"  # fallback

# Now in processing:
for i, (name, raw) in enumerate(students):
  curved = curved_scores[i]
  letter = letterGrade(curved)  # Mechanism is simple!
  results.append(obj(name=name, raw=raw, curved=curved, 
                     letter=letter))
```

**Benefits:**

1. **Easy to change policy:**
   ```python
   # More generous grading
   GENEROUS = [(85,"A"), (75,"B"), (65,"C"), (55,"D"), (0,"F")]
   letter = letterGrade(curved, GENEROUS)
   
   # Load from config
   import json
   with open("policy.json") as f:
     policy = json.load(f)
     thresholds = [(p["cutoff"], p["grade"]) for p in policy]
   letter = letterGrade(curved, thresholds)
   ```

2. **Trivial to test:**
   ```python
   def test_letter_grades():
     assert letterGrade(95) == "A"
     assert letterGrade(90) == "A"  # boundary
     assert letterGrade(89.9) == "B"  # boundary
     assert letterGrade(85) == "B"
     assert letterGrade(50) == "F"
     # All boundaries testable with simple data
   ```

3. **Different policies for different contexts:**
   ```python
   # Graduate class (stricter)
   GRAD_POLICY = [(93,"A"), (85,"B"), (77,"C"), (70,"D"), (0,"F")]
   
   # Undergraduate (standard)
   UNDERGRAD_POLICY = [(90,"A"), (80,"B"), (70,"C"), (60,"D"), (0,"F")]
   
   # Plus/minus grading
   PLUSMINUS = [(97,"A+"), (93,"A"), (90,"A-"), (87,"B+"), ...]
   
   def processGrades(file, policy=UNDERGRAD_POLICY):
     # ... same code works with any policy ...
     letter = letterGrade(curved, policy)
   ```

**Raymond's Wisdom Applied:**

The grading *mechanism* (finding first threshold) is now
"stupid and robust" - it's 3 lines and never changes.

The grading *policy* (what the thresholds are) is now
"folded into data" - easily modified, loaded, tested.

This is the power of separating mechanism from policy.

---

### Rule 4: Small Functions (Uncle Bob)

**Principle:** Functions should be 5-10 lines, max 20.

**Why?**
- Easy to understand at a glance
- Easy to test in isolation
- Easy to name descriptively
- Reveals the algorithm structure
- Each small function does ONE obvious thing

**The Violation - 45-Line Monster:**

```python
def process_grades(file="grades.csv"):
  rows = list(csv(file))
  header = rows[0]
  students = rows[1:]
  print(f"\n{'='*60}")
  print(f"GRADE REPORT - {len(students)} students")
  print(f"{'='*60}\n")
  raw_scores = []
  for student in students:
    name = student[0]
    hw1, hw2, hw3 = student[1], student[2], student[3]
    midterm, final = student[4], student[5]
    hw_avg = (hw1 + hw2 + hw3) / 3 if hw1 != "?" else 0
    raw = 0.3 * hw_avg + 0.3 * midterm + 0.4 * final
    raw_scores.append(raw)
  scores_stat = Num()
  for score in raw_scores: add(scores_stat, score)
  mean, stdev = scores_stat.mu, sd(scores_stat)
  print(f"Class Statistics (before curve):")
  print(f"  Mean: {mean:.1f}")
  print(f"  Std Dev: {stdev:.1f}\n")
  target_mean, target_std = 75, 10
  curved_scores = []
  for raw in raw_scores:
    z_score = (raw - mean) / stdev if stdev > 0 else 0
    curved = target_mean + z_score * target_std
    curved_scores.append(curved)
  print(f"Individual Reports:\n")
  letter_counts = Sym()
  for i, student in enumerate(students):
    name, curved = student[0], curved_scores[i]
    if curved >= 90: letter = "A"
    elif curved >= 80: letter = "B"
    elif curved >= 70: letter = "C"
    elif curved >= 60: letter = "D"
    else: letter = "F"
    add(letter_counts, letter)
    print(f"  {name:20} Raw: {raw_scores[i]:5.1f}  "
          f"Curved: {curved:5.1f}  Grade: {letter}")
  print(f"\n{'='*60}")
  print(f"Grade Distribution:")
  for grade in ["A", "B", "C", "D", "F"]:
    count = letter_counts.has.get(grade, 0)
    pct = 100 * count / len(students) if len(students) > 0 else 0
    bar = "*" * int(pct / 2)
    print(f"  {grade}: {count:2} ({pct:4.1f}%) {bar}")
  print(f"{'='*60}\n")
```

**45 lines! To understand this, you have to read and hold
all 45 lines in your head simultaneously.**

**The Fix - Extract Until Each Function Is Obvious:**

```python
# 4 lines - obviously computes one raw score
def computeRawScore(hw1, hw2, hw3, midterm, final):
  hw_avg = (hw1 + hw2 + hw3) / 3 if hw1 != "?" else 0
  return 0.3 * hw_avg + 0.3 * midterm + 0.4 * final

# 11 lines - obviously applies curve to scores
def applyCurve(raw_scores):
  stats = adds(raw_scores, Num())
  mean, stdev = stats.mu, sd(stats)
  target_mean, target_std = 75, 10
  curved = []
  for raw in raw_scores:
    z = (raw - mean) / stdev if stdev > 0 else 0
    curved.append(target_mean + z * target_std)
  return curved, mean, stdev

# 4 lines - obviously assigns letter grade
def letterGrade(score):
  for cutoff, grade in [(90,"A"), (80,"B"), (70,"C"), (60,"D")]:
    if score >= cutoff: return grade
  return "F"

# 16 lines - obviously processes all students
def processGrades(file):
  students, raw_scores = [], []
  for row in csv(file):
    if not students: continue
    name = row[0]
    raw = computeRawScore(row[1], row[2], row[3], row[4], row[5])
    students.append((name, raw))
    raw_scores.append(raw)
  curved_scores, mean, stdev = applyCurve(raw_scores)
  results = []
  for i, (name, raw) in enumerate(students):
    curved = curved_scores[i]
    results.append(obj(name=name, raw=raw, curved=curved,
                       letter=letterGrade(curved)))
  return obj(students=results, mean=mean, stdev=stdev)

# 4 lines - obviously prints header
def showHeader(n):
  print(f"\n{'='*60}")
  print(f"GRADE REPORT - {n} students")
  print(f"{'='*60}\n")

# 4 lines - obviously prints statistics
def showStats(mean, stdev):
  print(f"Class Statistics (before curve):")
  print(f"  Mean: {mean:.1f}")
  print(f"  Std Dev: {stdev:.1f}\n")

# 3 lines - obviously prints one student
def showStudent(student):
  print(f"  {student.name:20} Raw: {student.raw:5.1f}  "
        f"Curved: {student.curved:5.1f}  Grade: {student.letter}")

# 10 lines - obviously prints distribution
def showDistribution(students):
  counts = Sym()
  for s in students: add(counts, s.letter)
  print(f"\n{'='*60}")
  print(f"Grade Distribution:")
  for grade in ["A", "B", "C", "D", "F"]:
    count = counts.has.get(grade, 0)
    pct = 100 * count / len(students) if len(students) > 0 else 0
    bar = "*" * int(pct / 2)
    print(f"  {grade}: {count:2} ({pct:4.1f}%) {bar}")
  print(f"{'='*60}\n")

# 8 lines - obviously orchestrates the report
def report(result):
  showHeader(len(result.students))
  showStats(result.mean, result.stdev)
  print(f"Individual Reports:\n")
  for student in result.students:
    showStudent(student)
  showDistribution(result.students)

# 3 lines - obviously the entry point
def main():
  result = processGrades("grades.csv")
  report(result)
```

**Now:** 
- Longest function: 16 lines (processGrades)
- Most functions: 3-10 lines
- Each function name tells you exactly what it does
- Can understand each function in isolation
- Changes are localized to one small function

**Compare:**
- Before: One 45-line function doing everything
- After: Nine functions, each doing one obvious thing

---

### Rule 5: Streaming Over Loading

**Principle:** Process incrementally when possible, don't
load all data into memory.

**Why?**
- Works with arbitrarily large files
- Constant memory usage
- Can handle infinite streams  
- Faster time-to-first-result
- More scalable

**Note:** For this grade calculator with small classes, 
streaming isn't critical. But it's good practice and shows
the principle.

**The Violation - Load Everything First:**

```python
def process_grades(file="grades.csv"):
  # PROBLEM: Load entire file into memory
  rows = list(csv(file))  # 1000 students = load all 1000
  header = rows[0]
  students = rows[1:]
  
  print(f"GRADE REPORT - {len(students)} students")
  
  # Process the already-loaded data
  raw_scores = []
  for student in students:
    # ... compute scores from loaded rows ...
```

**Problems:**
- 1000 students? Load all 1000 rows first
- 10,000 students? Load all 10,000 rows first
- Memory usage: O(n) where n = number of students
- Can't process as data arrives

**The Fix - Stream and Accumulate:**

```python
def processGrades(file):
  """Process students as we read them, accumulate stats"""
  students = []
  raw_scores = []
  
  # SOLUTION: Process each row as it arrives
  for row in csv(file):  # csv() is already a generator
    if not students:  # first row is header
      continue
    
    # Process this student immediately
    name = row[0]
    raw = computeRawScore(row[1], row[2], row[3], 
                          row[4], row[5])
    students.append((name, raw))
    raw_scores.append(raw)
    
    # Only keep: names and scores, not full rows
  
  # Now curve with accumulated scores
  curved_scores, mean, stdev = applyCurve(raw_scores)
  
  # Build results
  results = []
  for i, (name, raw) in enumerate(students):
    curved = curved_scores[i]
    results.append(obj(name=name, raw=raw, curved=curved,
                       letter=letterGrade(curved)))
  
  return obj(students=results, mean=mean, stdev=stdev)
```

**Benefits:**
- Never hold full CSV rows in memory
- Process each student as we read them
- Only store: (name, score) tuples
- Memory: O(n) but smaller constants
- Could extend to truly stream if we used online stats

**For true streaming (advanced):**

```python
def processGradesStreaming(file):
  """Process and yield students one at a time"""
  raw_scores = []
  students = []
  
  # First pass: accumulate for statistics
  for row in csv(file):
    if not students: continue
    name = row[0]
    raw = computeRawScore(row[1], row[2], row[3], 
                          row[4], row[5])
    students.append((name, raw))
    raw_scores.append(raw)
  
  # Compute curve once
  curved_scores, mean, stdev = applyCurve(raw_scores)
  
  # Stream results
  for i, (name, raw) in enumerate(students):
    curved = curved_scores[i]
    yield obj(name=name, raw=raw, curved=curved,
              letter=letterGrade(curved))

# Usage
for student in processGradesStreaming("grades.csv"):
  showStudent(student)  # Print as they arrive
```

---

## Part 3: Impact Summary

### Before: 74 lines

 
ONE 45-LINE FUNCTION doing everything:

  - Load data (list everything)
  - Compute raw scores (inline loop)
  - Compute statistics (inline loop)
  - Print statistics (mixed with logic)
  - Apply curve (inline loop)
  - Assign grades (hardcoded if/elif)
  - Print students (mixed with logic)
  - Compute distribution (inline loop)
  - Print distribution (mixed with logic)
 

### After: 95 lines

 
CLEAR SECTIONS with focused functions:

  - Model (pure business logic): 35 lines
    computeRawScore (4), applyCurve (11), 
    letterGrade (4), processGrades (16)
  - Presentation (I/O only): 30 lines
    showHeader (4), showStats (4), showStudent (3),
    showDistribution (10), report (8)
  - Infrastructure: 20 lines
    Sym, Num, add, adds, sd, coerce, csv
  - Main: 3 lines
 

### Key Metrics

**Function sizes:**
- Before: 1 function × 45 lines
- After: Longest = 16 lines, most = 3-10 lines

**Responsibilities:**
- Before: 1 function × 10 responsibilities
- After: 9 functions × 1 responsibility each

**Policy flexibility:**
- Before: Grading scale hardcoded in if/elif
- After: THRESHOLDS data structure, easily changed

**Reusability:**
- Before: Can't reuse logic without printing
- After: Logic completely separate from presentation

**Testability:**
- Before: Must capture stdout to test
- After: Pure functions return data structures

**Memory:**
- Before: O(n) rows in memory
- After: O(n) but only (name, score) tuples

---

## Part 4: Was It Worth It?

### The Cost: +21 Lines of Code (28% increase)

**But what did we buy?**

### 1. Testability (HUGE WIN)

**Before (impossible to test cleanly):**
```python
def test_grading():
  # How do I test this without printing?
  import io, sys
  captured = io.StringIO()
  sys.stdout = captured
  process_grades("test.csv")
  output = captured.getvalue()
  sys.stdout = sys.__stdout__
  # Now parse text? Fragile!
  assert "Alice" in output
  assert "Grade: A" in output
```

**After (clean data assertions):**
```python
def test_raw_score():
  assert computeRawScore(90, 90, 90, 90, 90) == 90
  assert computeRawScore(100, 100, 100, 80, 80) == 88

def test_curve():
  raw = [60, 70, 80, 90, 100]
  curved, mean, stdev = applyCurve(raw)
  assert mean == 80
  assert curved[0] < 75  # below mean curves down
  assert curved[4] > 85  # above mean curves up

def test_letter_grades():
  assert letterGrade(95) == "A"
  assert letterGrade(90) == "A"
  assert letterGrade(89.9) == "B"
  assert letterGrade(50) == "F"

def test_full_process():
  result = processGrades("test.csv")
  assert len(result.students) == 10
  assert result.students[0].name == "Alice"
  assert result.students[0].letter == "A"
  assert 70 < result.mean < 85
```

### 2. Reusability (MASSIVE WIN)

**Before (logic locked in printing function):**
```python
# Want JSON API? Can't use process_grades
# Have to copy-paste and modify 45 lines

@app.get("/grades")
def api_grades():
  # ... duplicate all logic without prints ...
```

**After (logic available for any use):**
```python
# CLI
result = processGrades("grades.csv")
report(result)

# JSON API
@app.get("/grades")
def api_grades():
  result = processGrades("grades.csv")
  return [{"name": s.name, "grade": s.letter, 
           "curved": s.curved} for s in result.students]

# Email report
result = processGrades("grades.csv")
html = render_template("grades.html", result=result)
send_email(html)

# GUI
result = processGrades("grades.csv")
table.setData(result.students)
stats_panel.setText(f"Mean: {result.mean:.1f}")

# Batch processing
for class_file in class_files:
  result = processGrades(class_file)
  save_to_database(class_file, result)
```

### 3. Policy Flexibility (UNIQUE WIN)

**Before (grading scale hardcoded):**
```python
# Want different scale? Edit if/elif chain
# Want to load from config? Impossible
# Different scale per class? Duplicate function

if curved >= 90: letter = "A"
elif curved >= 80: letter = "B"
# ... hardcoded ...
```

**After (policy as data):**
```python
# Different policies
STANDARD = [(90,"A"), (80,"B"), (70,"C"), (60,"D"), (0,"F")]
GENEROUS = [(85,"A"), (75,"B"), (65,"C"), (55,"D"), (0,"F")]
STRICT = [(93,"A"), (85,"B"), (77,"C"), (70,"D"), (0,"F")]

# Load from config
with open("grading_policy.json") as f:
  policy = json.load(f)
  thresholds = [(p["min"], p["grade"]) for p in policy]

# Use different policy per class
undergrad_result = processGrades("cs101.csv")
for s in undergrad_result.students:
  s.letter = letterGrade(s.curved, STANDARD)

grad_result = processGrades("cs601.csv")
for s in grad_result.students:
  s.letter = letterGrade(s.curved, STRICT)
```

### 4. Maintainability (BIG WIN)

**Before (change output = edit 45-line function):**
```python
# Want to add class rank to output?
# Find the print statements in the 45-line function
# Hope you don't break the curve calculation

def process_grades(file):
  # ... 20 lines of logic ...
  print(f"  {name:20} ... Grade: {letter}")  # EDIT HERE
  # ... more logic ...
```

**After (change output = edit one small function):**
```python
# Want to add class rank?
def showStudent(student):
  print(f"  {student.name:20} Raw: {student.raw:5.1f}  "
        f"Curved: {student.curved:5.1f}  "
        f"Grade: {student.letter}  "
        f"Rank: {student.rank}")  # ADD ONE FIELD

# Logic functions untouched!
```

### 5. Clarity (WIN)

**Before (what does this do?):**
```python
process_grades("grades.csv")
# Have to read 45 lines to understand
```

**After (self-documenting):**
```python
result = processGrades("grades.csv")
report(result)

# "Process grades from CSV, then report results"
# Crystal clear from function names
```

---

## Part 5: The Verdict

### YES, Absolutely Worth It

**The +21 lines (28%) bought us:**

 
✓ Testable without stdout mocking.  
✓ Reusable for API/GUI/email/batch.     
✓ Flexible grading policies (mechanism vs policy).    
✓ Maintainable presentation layer.   
✓ Self-documenting function names.   
✓ Each function does ONE thing.   
✓ Model/View separation (SoC).   
 

**We gave up:**
 
✗ 21 more lines (28% increase).    
✗ More functions to navigate.     
 

### The Critical Rules

**Non-Negotiable (always apply):**

1. **Separation of Concerns** - Never mix model with I/O
   - Can't be reused otherwise
   - Can't be tested otherwise
   - Can't support multiple UIs otherwise

2. **Mechanism vs Policy** - Separate rules from code
   - Business users can modify policy
   - Different contexts use different policies
   - Rules can be loaded from config
   - Testing becomes trivial

**Highly Recommended (usually apply):**

3. **Single Responsibility** - Each function, one job
4. **Small Functions** - Keep functions short and obvious

**Context-Dependent (sometimes apply):**

5. **Streaming** - Process incrementally
   - Critical at scale
   - Good practice even when not critical

---

## Part 6: When to Apply These Rules

### The Hierarchy

```
┌─────────────────────────────────────┐
│  ALWAYS                             │
│  - Separation of Concerns (SoC)     │
│    (Never mix model with I/O)       │
│  - Mechanism vs Policy              │
│    (Separate rules from code)       │
├─────────────────────────────────────┤
│  USUALLY                            │
│  - Single Responsibility (SRP)      │
│  - Small Functions (<20 lines)      │
├─────────────────────────────────────┤
│  SOMETIMES                          │
│  - Streaming vs Loading             │
│    (matters at scale)               │
└─────────────────────────────────────┘
```

### Apply Rules When:

**1. Code will be reused**
```python
# Library, API, shared module
def processGrades(file):
  # Others will call this
  # MUST separate concerns!
  # MUST make policy flexible!
```

**2. Requirements will change**
 
- Grading scale might change
- Output format might change
- New features will be added
- MUST make it maintainable!
 

**3. Testing matters**
 
- Production code
- Grading affects student outcomes
- Must be correct
- MUST be testable without mocking I/O!

**4. Multiple contexts**

- Different grading scales
- Different output formats (CLI, GUI, API)
- Different use cases
- MUST separate mechanism from policy!


### Skip/Relax When:

**1. Throwaway code**
```python
# One-off grade adjustment script
for line in open("grades.txt"):
  old, new = adjust(line)
  print(f"{old} -> {new}")  # Who cares about SoC?
```

**2. Stable, working code**

- Grade calculator that hasn't changed in 5 years
- Everyone understands it
- No new requirements
- LEAVE IT ALONE (but still separate I/O!)

**3. Very small scale**

- 20-line script for personal use
- Never reused
- Single purpose
- Okay to be simple (but still separate I/O!)


**4. Prototyping**

- Exploring an algorithm
- Will be rewritten
- Just figuring things out
- Okay to mix concerns temporarily

### But SoC and Mechanism vs Policy are ALWAYS Required

**Even for small scripts:**

```python
# BAD - even for one-off
def quick_grade(file):
  for row in csv(file):
    score = compute(row)
    if score >= 90: grade = "A"  # Policy in code
    print(f"{row[0]}: {grade}")  # Mixed with logic
  
# GOOD - even for one-off
POLICY = [(90,"A"), (80,"B"), (70,"C")]

def letterGrade(score):
  for cutoff, g in POLICY:
    if score >= cutoff: return g

def compute(file):
  return [(row[0], compute(row)) for row in csv(file)]

# Let caller choose presentation and policy
for name, score in compute(file):
  print(f"{name}: {letterGrade(score)}")
```

**Why?** Because:

- Scripts become libraries (always!)
- Requirements change (always!)
- Policies evolve (always!)
- You'll thank yourself later (always!)

---

## Part 7: The Final Code

Here's the complete refactored version (95 lines):

```python
#!/usr/bin/env python3 -B
"""grades.csv: student grade calculator with curve"""
from math import sqrt
from types import SimpleNamespace as obj

def Sym(): return obj(it=Sym, n=0, has={})
def Num(): return obj(it=Num, n=0, mu=0, m2=0)

def add(i, v):
  if v != "?":
    i.n += 1
    if Sym is i.it: i.has[v] = 1 + i.has.get(v, 0)
    else: d = v - i.mu; i.mu += d / i.n; i.m2 += d * (v - i.mu)
  return v

def adds(src, i=None): i = i or Num(); [add(i, v) for v in src]; return i

def sd(num): return 0 if num.n < 2 else sqrt(num.m2 / (num.n - 1))

def coerce(s):
  try: return int(s)
  except: 
    try: return float(s)
    except: return s.strip()

def csv(file):
  with open(file) as f:
    for line in f:
      if line := line.strip(): yield [coerce(x) for x in line.split(",")]

#--- Policy (data - easy to change) ---
THRESHOLDS = [(90,"A"), (80,"B"), (70,"C"), (60,"D"), (0,"F")]

#--- Model (pure business logic, no I/O) ---
def computeRawScore(hw1, hw2, hw3, midterm, final):
  hw_avg = (hw1 + hw2 + hw3) / 3 if hw1 != "?" else 0
  return 0.3 * hw_avg + 0.3 * midterm + 0.4 * final

def applyCurve(raw_scores):
  stats = adds(raw_scores, Num())
  mean, stdev = stats.mu, sd(stats)
  target_mean, target_std = 75, 10
  curved = []
  for raw in raw_scores:
    z = (raw - mean) / stdev if stdev > 0 else 0
    curved.append(target_mean + z * target_std)
  return curved, mean, stdev

def letterGrade(score, thresholds=THRESHOLDS):
  for cutoff, grade in thresholds:
    if score >= cutoff: return grade
  return "F"

def processGrades(file):
  students, raw_scores = [], []
  for row in csv(file):
    if not students: continue
    name = row[0]
    raw = computeRawScore(row[1], row[2], row[3], row[4], row[5])
    students.append((name, raw))
    raw_scores.append(raw)
  curved_scores, mean, stdev = applyCurve(raw_scores)
  results = []
  for i, (name, raw) in enumerate(students):
    curved = curved_scores[i]
    results.append(obj(name=name, raw=raw, curved=curved,
                       letter=letterGrade(curved)))
  return obj(students=results, mean=mean, stdev=stdev)

#--- Presentation (I/O only, no logic) ---
def showHeader(n):
  print(f"\n{'='*60}")
  print(f"GRADE REPORT - {n} students")
  print(f"{'='*60}\n")

def showStats(mean, stdev):
  print(f"Class Statistics (before curve):")
  print(f"  Mean: {mean:.1f}")
  print(f"  Std Dev: {stdev:.1f}\n")

def showStudent(student):
  print(f"  {student.name:20} Raw: {student.raw:5.1f}  "
        f"Curved: {student.curved:5.1f}  Grade: {student.letter}")

def showDistribution(students):
  counts = Sym()
  for s in students: add(counts, s.letter)
  print(f"\n{'='*60}")
  print(f"Grade Distribution:")
  for grade in ["A", "B", "C", "D", "F"]:
    count = counts.has.get(grade, 0)
    pct = 100 * count / len(students) if len(students) > 0 else 0
    bar = "*" * int(pct / 2)
    print(f"  {grade}: {count:2} ({pct:4.1f}%) {bar}")
  print(f"{'='*60}\n")

def report(result):
  showHeader(len(result.students))
  showStats(result.mean, result.stdev)
  print(f"Individual Reports:\n")
  for student in result.students:
    showStudent(student)
  showDistribution(result.students)

#--- Main ---
result = processGrades("grades.csv")
report(result)
```

**95 lines. Clean. Testable. Reusable. Flexible. 
Maintainable.**

---

## Summary

**We started with:** 74 lines, 1 monolithic function

**We ended with:** 95 lines, 12 focused functions

**We gained:**

- Testability without stdout mocking
- Reusability for API/GUI/email/batch
- Policy flexibility (change grading scale easily)
- Maintainable presentation layer
- Self-documenting structure
- Clear separation of concerns

**We gave up:** 21 lines (28%)

**The key insights:**

1. **Separation of Concerns** is non-negotiable - model
   must be separate from presentation for reusability

2. **Mechanism vs Policy** enables flexibility - folding
   knowledge into data makes code "stupid and robust"

3. **Small Functions** reveal structure - each function's
   name documents what it does

4. The +28% LOC is worth it for production code that will
   be maintained, tested, and reused

**Eric Raymond's Wisdom Applied:**

*"Fold knowledge into data, so program logic can be 
stupid and robust."*

We folded grading thresholds into data (THRESHOLDS).
Now the grading mechanism is 3 lines and never changes,
while the policy can be modified without touching code.

**"Simple ain't stupid. But simple with SoC and 
Mechanism vs Policy is smarter."**

