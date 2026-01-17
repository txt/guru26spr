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

# Regular expressions

 > "Regular expressions are the duct tape of text processing."

Imagine regular expressions as a navigational map for a
vast railway network hidden inside your text.

- Every character in a string is a ticket. That ticket lets
you travel from one station to the next — but only if the
tracks exist. Those tracks are the rules defined by your
regular expression.
- A letter may allow forward movement. A digit, whitespace,
or symbol might be the only valid connection at a given
point. If the required track is missing, the train stops.
- As the engine moves through the text, it tries each
character as a potential starting station. From there,
it follows the rails you defined, step by step.
- If every transition is valid, the train keeps moving.
If a rule fails, the engine backs up and tries another
route.
- Your goal is to design a route that reaches a final
station — the end of the pattern.
- When the engine arrives there without derailment, the
match succeeds. The journey ends. The search stops

As a simple example, here is a machine recognizing the set of strings matched by the regular expression `a(bb)+a`:

![](https://swtch.com/~rsc/regexp/fig0.png)

A finite automaton is always in one of its states, represented in the diagram by circles. (The numbers inside the circles are labels to make this discussion easier; they are not part of the machine's operation.) As it reads the string, it switches from state to state.
This machine has two special states: the start state s0 and the matching state s4.

The machine reads an input string one character at a time, following arrows corresponding to the input to move from state to state. Suppose the input string is abbbba. When the machine reads the first letter of the string, the a, it is in the start state s0. It follows the a arrow to state s1. This process repeats as the machine reads the rest of the string: b to s2, b to s3, b to s2, b to s3, and finally a to s4.

![](https://swtch.com/~rsc/regexp/fig1.png)

The machine is not deterministic because if it reads a b in state s2, it has multiple choices for the next state: it can go back to s1 in hopes of seeing another bb, or it can go on to s3 in hopes of seeing the final a. Since the machine cannot peek ahead to see the rest of the string, it has no way to know which is the correct decision. In Thompson NFA (nondeterministic finite satat automata), the
match push down all outputs. In other ([much slower](https://swtch.com/~rsc/regexp/regexp1.html)
approaches), it pushes down
one all the way it can, and only tries the others if that match fails.

The fun thing about regualr expressions is that they can be 
[coded very simply](https://www.cs.princeton.edu/courses/archive/spr09/cos333/beautiful.html). They are very, very effecient.

- "Rob's implementation itself is a superb example of beautiful code: compact, elegant, efficient, and useful. It's one of the best examples of recursion that I have ever seen, and it shows the power of C pointers. Although at the time we were most interested in conveying the important role of a good notation in making a program easier to use and perhaps easier to write as well, the regular expression code has also been an excellent way to illustrate algorithms, data structures, testing, performance enhancement, and other important topics." - Brian Kernighan

## PART 1 — Lua Pattern Meta-characters

Here is the reference table for Lua's specific regex flavor (patterns).

```text
^       Start of string (anchor)
$       End of string (anchor)
.       Any single character
%       Escape or class prefix
* 0+ repeats (greedy)
+       1+ repeats (greedy)
-       0+ repeats (non-greedy)
?       Optional (0 or 1)
[]      Character set/class
()      Capture group
%s      Whitespace
%S      Non-whitespace
%d      Digit
%D      Non-digit
%w      Alphanumeric
%W      Non-alphanumeric
%bxy    Balanced x...y
%f[]    Frontier (boundary)

```

---

## PART 2 — Lua Examples (The Lesson)

*Study these 10 standard editing tasks using Lua patterns.*

**1. Find & Replace**
*Replace literal text.*

* **Code:** `s = s:gsub("foo", "bar")`
* **Before:** `"foo = foo + 1"`
* **After:** `"bar = bar + 1"`

**2. Whitespace Cleanup**
*Trim ends and collapse internal spaces.*

* **Code:** `s = s:gsub("^%s+", ""):gsub("%s+$", ""):gsub("%s+", " ")`
* **Before:** `"   a   b    c   "`
* **After:** `"a b c"`

*# Regualr expersions*3. Remove Blank Lines**
*Remove lines that contain only whitespace.*

* **Code:** `s = s:gsub("\n%s*\n", "\n")`
* **Before:** `"a\n\n\nb\n\nc"`
* **After:** `"a\nb\nc"`

**4. Extract Substring (Email)**
*Capture non-whitespace surrounding an @ symbol.*

* **Code:** `e = s:match("(%S+@%S+)")`
* **Before:** `"mail me at tim@example.com asap"`
* **After:** `"tim@example.com"`

**5. Reformat Text (Swap Names)**
*Swap "Last, First" to "First Last".*

* **Code:** `s = s:gsub("(%w+),%s*(%w+)", "%2 %1")`
* **Before:** `"menzies, tim"`
* **After:** `"tim menzies"`

**6. Bulk Rename with Boundaries**
*Replace a word only if it is a whole word (using frontier pattern).*

* **Code:** `s = s:gsub("%f[%w]old%f[%W]", "new")`
* **Before:** `"old older fold old."`
* **After:** `"new older fold new."`

**7. Validate Structure (Date)**
*Check if string matches YYYY-MM-DD exactly.*

* **Code:** `ok = s:match("^%d%d%d%d%-%d%d%-%d%d$") ~= nil`
* **Before:** `"2026-01-15"`
* **After:** `true`

**8. Join Wrapped Lines**
*Join lines where a sentence was split, preserving the space.*

* **Code:** `s = s:gsub("([^\n])\n(%S)", "%1 %2")`
* **Before:** `"this is a\nwrapped line"`
* **After:** `"this is a wrapped line"`

**9. Comment / Uncomment Code**
*Add or remove comment markers at the start of the line.*

* **Code (Comment):** `s = s:gsub("^(%s*)", "%1-- ")`
* **Code (Uncomment):** `s = s:gsub("^(%s*)%-%-%s?", "%1")`
* **Before:** `"print(x)"`  `"-- print(x)"`

**10. Find Balanced Structures**
*Match text between nested parentheses.*

* **Code:** `for x in s:gmatch("%b()") do print(x) end`
* **Before:** `"f(a, g(b,c), d)"`
* **After:** `"(a, g(b,c), d)"`

---

## PART 3 — Python Answer Sheet (For Tutors)

*These are the Python equivalents students should produce for the homework.*

**1. Find & Replace**

```python
import re
s = "foo = foo + 1"
 Solution
s = s.replace("foo", "bar")
 OR regex: s = re.sub("foo", "bar", s)

```

**2. Whitespace Cleanup**

```python
s = "   a   b    c   "
 Solution
s = re.sub(r"\s+", " ", s.strip())

```

**3. Remove Blank Lines**

```python
s = "a\n\n\nb\n\nc"
 Solution
s = re.sub(r"\n\s*\n", "\n", s)

```

**4. Extract Substring (Email)**

```python
s = "mail me at tim@example.com asap"
 Solution
match = re.search(r"(\S+@\S+)", s)
e = match.group(1) if match else None

```

**5. Reformat Text (Swap Names)**

```python
s = "menzies, tim"
 Solution
s = re.sub(r"(\w+), \s*(\w+)", r"\2 \1", s)
 Note: Python uses \1, \2 for backreferences, Lua uses %1, %2

```

**6. Bulk Rename with Boundaries**

```python
s = "old older fold old."
 Solution
s = re.sub(r"\bold\b", "new", s)
 Note: Python uses \b for boundaries, Lua uses %f

```

**7. Validate Structure (Date)**

```python
s = "2026-01-15"
 Solution
ok = bool(re.match(r"^\d{4}-\d{2}-\d{2}$", s))
 Note: Python uses {} for counts, Lua repeats %d%d...

```

**8. Join Wrapped Lines**

```python
s = "this is a\nwrapped line"
 Solution
s = re.sub(r"([^\n])\n(\S)", r"\1 \2", s)

```

**9. Comment / Uncomment Code**

```python
s = "print(x)"
 Solution (Comment)
s = re.sub(r"^", "# ", s) 

s = "# print(x)"
 Solution (Uncomment)
s = re.sub(r"^#\s?", "", s)

```

**10. Find Balanced Structures**

```python
s = "f(a, g(b,c), d)"
 Solution
 Python 're' cannot handle recursive nesting like Lua's %b(). 
 Students must install the 'regex' module or write a parser.
 A close approximation for one level depth is:
matches = re.findall(r"\([^)]*\)", s)

