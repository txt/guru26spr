<p align="center">
  <a href="https://github.com/txt/guru26spr/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/docs/syllabus.md"><img 
      src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/12Jg_K_E4t8qo0O2uBE-s_t4IAR8f4lXjrdBiItLVs_8/edit?gid=0#gid=0"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8118&bp=s"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591: How to be a SE Guru <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/guru26spr/refs/heads/main/etc/img/banenr.png"> 


# Homework: Refactor the Word Frequency Counter

## Overview

You've learned 5 SE design heuristics:
1. **Separation of Concerns (SoC)** - Don't mix model with I/O
2. **Single Responsibility Principle (SRP)** - One function, one job
3. **Mechanism vs Policy** - Separate rules from code
4. **Small Functions** - Keep functions short and obvious
5. **Streaming Over Loading** - Process incrementally when possible

Now apply them to this messy word counter!

## The Code

**wc0.py** - 43 lines with multiple violations
- Reads text file
- Counts word frequencies
- Removes stopwords
- Shows top N most frequent words

**Sample data:**
- **essay.txt** - Text about software engineering principles

## Current Output

```
==================================================
WORD FREQUENCY ANALYSIS - essay.txt
==================================================

Total words (after removing stopwords): 99
Unique words: 66

Top 10 most frequent words:

 1. software          5 *****
 2. concerns          5 *****
 3. separation        4 ****
 4. very              3 ***
 5. principle         3 ***
```

## The Violations

### 1. Separation of Concerns (SoC)
**Printing mixed throughout the function:**
- Lines 8-10: Header printing
- Lines 24-26: Stats printing
- Lines 27-32: Results printing

**Problem:** Can't test logic without capturing stdout. 
Can't reuse for API or GUI. Can't change output format 
without editing business logic.

### 2. Single Responsibility Principle (SRP)
**The `count_words()` function does EVERYTHING:**
- Reads file
- Cleans words
- Counts frequencies
- Sorts results
- Filters top N
- Formats output
- Prints results

**33 lines doing 7+ responsibilities!**

### 3. Mechanism vs Policy
**Hardcoded policies scattered throughout:**

**Line 14:** 
```python
stopwords = ["the", "a", "an", ...]  # Hardcoded list!
```
- Policy: which words to ignore
- Should be: data in CONFIG

**Line 18:**
```python
word = word.strip('.,!?;:"()')  # Hardcoded punctuation!
```
- Policy: which characters to remove
- Should be: data in CONFIG

**Line 23:**
```python
top_n = 10  # Hardcoded!
```
- Policy: how many results to show
- Should be: parameter or CONFIG

### 4. Small Functions
**The `count_words()` function is 33 lines!**

Should be split into:
- `readText(file)` - 3 lines
- `cleanWord(word, punct)` - 2 lines
- `countWords(text, stopwords, punct)` - 8 lines
- `topN(counts, n)` - 2 lines
- `analyze(file)` - 6 lines (orchestrates)
- `showHeader(file)` - 4 lines
- `showStats(result)` - 3 lines
- `showTop(result, n)` - 6 lines
- `report(file, result)` - 4 lines
- `count_words(file)` - 3 lines (main)

### 5. Streaming Over Loading
**Line 7:** 
```python
text = f.read()  # Loads entire file
```

For this small example, not critical. But shows the pattern.
For large files, could process line by line.

## Your Assignment

Refactor `wc0.py` following the 5 heuristics.

### Required Changes:

**1. Separate model from presentation**
- Extract: `readText()`, `countWords()`, `topN()`, `analyze()`
- Keep all business logic I/O-free
- Create: `showHeader()`, `showStats()`, `showTop()` for printing

**2. Single responsibility per function**
- Main function should be < 5 lines
- Each helper should do ONE thing
- Name functions clearly: verb + noun

**3. Extract policies to data**
```python
CONFIG = {
  'top_n': 10,
  'stopwords': ["the", "a", "an", ...],
  'punctuation': '.,!?;:"()-'
}
```

**4. Keep functions small**
- No function > 10 lines
- Most functions: 2-6 lines
- Extract until obvious

**5. Consider streaming**
- Don't require loading entire file
- For this example, current approach is fine

### Deliverables:

1. **Your refactored code** (~75-85 lines)
2. **Test it runs:** Should produce same results as wc0.py
3. **Brief comments:** Explain which rule you applied where

### Expected Structure:

```python
#--- Policy (data) ---
CONFIG = {
  'top_n': 10,
  'stopwords': [...],
  'punctuation': '...'
}

#--- Model (pure functions, no I/O) ---
def readText(file): ...
def cleanWord(word, punct): ...
def countWords(text, stopwords, punct): ...
def topN(counts, n): ...
def analyze(file): ...

#--- Presentation (I/O only) ---
def showHeader(file): ...
def showStats(result): ...
def showTop(result, n): ...
def report(file, result): ...

#--- Main ---
def count_words(file):
  result = analyze(file)
  report(file, result)
  return result
```

## Grading Rubric:

- **SoC (30%)**: Model/View completely separated
- **SRP (20%)**: Each function has one clear job
- **Mechanism vs Policy (20%)**: Policies in CONFIG
- **Small Functions (20%)**: No function > 10 lines
- **Code Quality (10%)**: Clear names, readable
- **Bonus**: half a mark for each working bonus

## Testing Your Code:

Your refactored code should produce the **exact same output**
as wc0.py:

```bash
python3 wc0.py > before.txt
python3 your_solution.py > after.txt
diff before.txt after.txt  # Should be identical!
```

## Bonus Challenges:

1. **Multiple output formats:**
   ```python
   def toJSON(result): return json.dumps(result)
   def toCSV(result): ...
   ```

2. **Load stopwords from file:**
   ```python
   CONFIG['stopwords'] = loadStopwords('stopwords.txt')
   ```

3. **Add unit tests:**
   ```python
   def test_cleanWord():
     assert cleanWord("hello,", ".,") == "hello"
   
   def test_countWords():
     counts = countWords("the cat and the dog", ["the"], "")
     assert counts == {"cat": 1, "and": 1, "dog": 1}
   ```

4. **Support different languages:**
   ```python
   CONFIG['stopwords_spanish'] = ["el", "la", "los", ...]
   ```

## Hints:

**Start with SoC:**
1. First, extract `showHeader()`, `showStats()`, `showTop()`
2. Move all printing to these functions
3. Make main function return data structure

**Then extract business logic:**
1. Extract `cleanWord()` - just word cleaning
2. Extract `countWords()` - just counting
3. Extract `topN()` - just sorting/filtering

**Then pull out policies:**
1. Create CONFIG dict at top
2. Replace hardcoded values with CONFIG references

**Finally, check sizes:**
1. Is any function > 10 lines? Split it
2. Does each function have a clear single purpose?

## Common Mistakes to Avoid:

❌ **Don't just add functions that still print:**
```python
def countWords(text):
  counts = {}
  # ... counting ...
  print(f"Counted {len(counts)} words")  # BAD!
  return counts
```

✓ **Functions should be pure (I/O-free):**
```python
def countWords(text, stopwords, punct):
  counts = {}
  # ... counting ...
  return counts  # GOOD!
```

❌ **Don't leave policies hardcoded:**
```python
def countWords(text):
  stopwords = ["the", "a", ...]  # Still hardcoded!
```

✓ **Pass policies as parameters:**
```python
def countWords(text, stopwords, punct):
  # Uses parameters!
```

## Expected Results:

**Before (wc0.py):**
- 43 lines
- 1 function doing everything
- Hardcoded policies
- Mixed I/O and logic

**After (your solution):**
- ~75-85 lines
- 10+ small focused functions
- CONFIG for all policies
- Clean separation of concerns

**The trade-off:** Almost double the lines, but:
- Each function is trivial to understand
- Easy to test each piece
- Easy to reuse (API, GUI, batch)
- Easy to change policies
- Easy to maintain

## Final Check:

Before submitting, verify:
- ✓ Same output as wc0.py
- ✓ No function > 10 lines
- ✓ All policies in CONFIG
- ✓ No printing in model functions
- ✓ Each function does ONE thing
- ✓ Clear function names

Good luck! This is much simpler than the grade calculator,
so you should be able to complete it in about 1 hour.

**Remember:** The goal isn't just to make it work, but to
make it *well-structured* following the 5 heuristics.
