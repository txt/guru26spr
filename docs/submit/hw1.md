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


# Homework: Refactor the Word Frequency Counter

YOu will need these files:

- sample data: [essay.txt](essay.txt)
- sample code: [wc0.py](wc0.py)

## Overview

You've learned 5 SE design heuristics:
1. **Separation of Concerns (SoC)** - Don't mix model with I/O
2. **Single Responsibility Principle (SRP)** - One function, one job
3. **Mechanism vs Policy** - Separate rules from code
4. **Small Functions** - Keep functions short and obvious

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

Can you find and fix these:

Q1. What Separation of Concerns (SoC) issues? What problems do they cause?

Q2. Single Responsibility Principle (SRP) issues? Can you list functions containing multiple other candidate functions?

Q3. Mechanism vs Policy issues? Can you find them?

Q4. Any small Function problems (Hint: yes). How to fix?

## Your Assignment

Refactor `wc0.py` following the 4 heuristics.
Hand in a version of wc0.py with comments on what parts of the code fix what heuristcs. Make sure you have lots
of comments. Make sure your comments include symbols like Q1, AQ1, Q2, AQ2, etc. Name the file wc0_fixed.py

### Required Changes:

- Separate model from presentation**
- Single responsibility per function**
- Extract policies to data
- Keep functions small**
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
   (Hint: Common english stopwords at [https://github.com/timm/ezr/blob/main/etc/stop_words.txt](https://github.com/timm/ezr/blob/main/etc/stop_words.txt)

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
## Expected Results:

**Before (wc0.py):**
- 43 lines
- 1 function doing everything
- Hardcoded policies
- Mixed I/O and logic

**After (wc0_fixed.py):**
- ~75-85 lines
- 10+ small focused functions
- CONFIG for all policies
- Clean separation of concerns

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
make it *well-structured* following the 4 heuristics.
