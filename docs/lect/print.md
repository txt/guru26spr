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

DOn;tprint, log

ont mess the model with presentation layer stuff
- speration of concerns

unix t-model sd/in. std/out, std/eror

python has forst class functions

Here is the complete content formatted as a raw Markdown file, wrapped to a maximum of 70 characters width.

```markdown
# Python Logging Variants & Tutorials

## 1. Simplest: Functional Approach
Use this for scripts where you want a global "Volume" knob.

**Logic:**
* `LOUD = 6`: Trace, Debug, Info, Warn, Err, Fatal (Noisy)
* `LOUD = 4`: Info, Warn, Err, Fatal (Standard)
* `LOUD = 1`: Fatal only (Quiet)
* `LOUD = 0`: Mute

```python
import sys

# Global Volume: 6=All, 4=Info+, 1=Fatal, 0=Mute
LOUD = 4

def say(n, *lst, **d):
    if LOUD >= n: print(*lst, **d)

# --- Standard Output ---
def trce(*lst, **d): say(6, "[TRACE]", *lst, **d)
def dbg(*lst, **d):  say(5, "[DEBUG]", *lst, **d)
def info(*lst, **d): say(4, "[INFO] ", *lst, **d)

# --- Standard Error ---
def warn(*lst, **d): say(3, "[WARN] ", *lst, file=sys.stderr, **d)
def err(*lst, **d): say(2, "[ERROR]", *lst, file=sys.stderr, **d)
def fatal(*lst, **d):
    say(1, "[FATAL]", *lst, file=sys.stderr, **d)
    sys.exit(1)

# Usage
# from watcher inport err, fatal,fatal
# o= infor
# o("System ready")
# LOUD = 1
# err("Hidden")
# fatal("Goodbye")

```

---

## 2. Moderate: Class Approach

Use this to encapsulate settings or have different loggers for
different parts of your app.

```python
import sys

class Logger:
    loud = 4  # Class default

    def __init__(self, loudness=None):
        if loudness is not None: Logger.loud = loudness

    def say(self, n, *lst, **d):
        if self.loud >= n: print(*lst, **d)

    # High Verbosity
    def trace(self, *l, **d): self.say(6, "[TRACE]", *l, **d)
    def dbg(self,   *l, **d): self.say(5, "[DEBUG]", *l, **d)
    def info(self,  *l, **d): self.say(4, "[INFO] ", *l, **d)

    # Low Verbosity (Critical)
    def warn(self, *l, **d):
        self.say(3, "[WARN] ", *l, file=sys.stderr, **d)

    def err(self, *l, **d):
        self.say(2, "[ERROR]", *l, file=sys.stderr, **d)

    def fatal(self, *l, **d):
        self.say(1, "[FATAL]", *l, file=sys.stderr, **d)
        sys.exit(1)

    # Shortcut: makes object callable -> log("msg")
    def __call__(self, *lst, **d): self.info(*lst, **d)

# Usage
o = Logger(loudness=4)
o("System Ready")  # Calls info
o.err("Error!")

```
| Feature | Custom "One-Liner" | Standard `logging` Module |
| :--- | :--- | :--- |
| **Setup Time** | Instant | Medium (Requires boilerplate) |
| **Best For** | Scripts, Tools, Prototypes | Production Apps, Servers, Libraries |
| **Log Files** | Manual (You write the code) | Automatic (File rotation, sizing) |
| **Format** | Hard-coded (`[INFO]`) | Configurable (`%(asctime)s - %(name)s`) |
| **Ecosystem** | Isolated | Integrates with Django, Flask, AWS |
```

---

## 3. Tutorial: The "Print Trick" (*l and **d)

How to pass arguments blindly to another function.

* `*l` (List): Packs positional args (e.g., "a", "b").
* `**d` (Dict): Packs keyword args (e.g., end="\n").

```python
def wrapper(*l, **d):
    print("--- START ---")
    # Unpack them to pass to the real print
    print(*l, **d)
    print("--- END ---")

# Usage
# wrapper("Hello", "World", sep="-", end="!!\n")

```

---

## 4. Tutorial: Unpacking Lists

How to grab specific items and ignore the rest using `*`.

```python
data = [1, 2, 3, 4, 5]

# 1. Grab First, Last, ignore middle (_)
first, *_, last = data

# first -> 1
# last  -> 5
# _     -> [2, 3, 4]

# 2. Grab Head vs Tail
head, *tail = data
# head -> 1
# tail -> [2, 3, 4, 5]

```

```

```


## Fun with `*` and `**`

first,*_,last= [1,2,3,4,5]

The Concept
*l (List/Tuple): Collects all "loose" variables (positional arguments) into a tuple.

**d (Dictionary): Collects all "named" variables (keyword arguments) into a dictionary.

The Power Move: When you use * and ** in a function call, they dump those collections back out as individual items.

Example 1: The Print Trick
This is the logic used in the logger we built. You want a middleman function that accepts anything and passes it blindly to the real print function.

. Capture everything into 'l' (list) and 'd' (dict)
```
def wrapper(*l, **d):
    print("--- LOG START ---")
    
    # 2. Unpack them back out to pass to the real print
    #    If you didn't use * and **, it would print the tuple and dict objects directly.
    print(*l, **d) 
    
    print("--- LOG END ---")

# Usage
wrapper("Hello", "World", sep="-", end="!!\n")
```  

What happens internally:
- l = ("Hello", "World")
- d = {'sep': '-', 'end': '!!\n'}
- print calls -> print("Hello", "World", sep="-", end="!!\n")

"""
|Log Level|	Importance|
|---------|---------|
|Fatal	|One or more key business functionalities are not working and the whole system doesn’t fulfill the business functionalities. |
|Error|	One or more functionalities are not working, preventing some functionalities from working correctly.|
|Warn|	Unexpected behavior happened inside the application, but it is continuing its work and the key business features are operating as expected.|
|Info|	An event happened, the event is purely informative and can be ignored during normal operations.|
|Debug|	A log level used for events considered to be useful during software debugging when more granular information is needed.|
|Trace|	A log level describing events showing step by step execution of your code that can be ignored during the standard operation, but may be useful during extended debugging sessions.|
"""
LOUD=5

You are right. In standard logging, "loudness" is usually treated as Verbosity.

High Loudness (e.g., 6) = Very verbose. You hear everything (Trace, Debug, Info...).

Low Loudness (e.g., 1) = Very quiet. You only hear the most critical things (Fatal).

0: Mute (Nothing prints)

1: Fatal only

2: Errors + Fatal

3: Warnings + Errors + Fatal

4: Info + Warnings... (Standard)

5: Debug + Info...

6: Trace + Debug... (All)

```
import sys

class Logger:
    loud = 4  # Default to Standard (Info and above)

    def __init__(self, loudness=None):
        if loudness is not None: Logger.loud = loudness

    def say(self, n, *lst, **d):
        if self.loud >= n: print(*lst, **d)

    # 6=Trace, 5=Debug, 4=Info, 3=Warn, 2=Error, 1=Fatal
    def trace(self, *lst, **d): self.say(6, "[TRACE]", *lst, **d)
    def dbg(self,   *lst, **d): self.say(5, "[DEBUG]", *lst, **d)
    def info(self,  *lst, **d): self.say(4, "[INFO] ", *lst, **d)
    
    def warn(self,  *lst, **d): self.say(3, "[WARN] ", *lst, file=sys.stderr, **d)
    def err(self,   *lst, **d): self.say(2, "[ERROR]", *lst, file=sys.stderr, **d)
    def fatal(self, *lst, **d): self.say(1, "[FATAL]", *lst, file=sys.stderr, **d); sys.exit(1)

    # Shortcut: Makes o("msg") equivalent to o.info("msg")
    def __call__(self, *lst, **d): self.info(*lst, **d)
```
Lesson: a;; pythong ucntions ahve 2 arguments: list of positions and a list of names vars **d
```
o = Logger(loudness=3) 
o.trace("Variable x = 10")  # Hidden (3 < 6)
o.dbg("Connecting...")      # Hidden (3 < 5)
o.info("System Ready")      # Hidden (3 < 4)
o.warn("Disk full")         # PRINTED (3 >= 3)
o.err("Database down")      # PRINTED (3 >= 2)
o.fatal("Bye")              # PRINTED (3 >= 1) -> Exits
```

But do I need a class? Place this code inn a file called watcher


```
import sys

# Global Volume Control
# 6=All, 4=Standard, 1=Fatal Only, 0=Mute
LOUD = 4

def say(n, *lst, **d):
    # Reads the global LOUD variable
    if LOUD >= n: print(*lst, **d)

# --- Standard Output (High Verbosity) ---
def trce(*lst, **d): say(6, "[TRACE]", *lst, **d)
def dbg(*lst, **d):  say(5, "[DEBUG]", *lst, **d)
def info(*lst, **d): say(4, "[INFO] ", *lst, **d)

# --- Standard Error (Low Verbosity / Critical) ---
def warn(*lst, **d):  say(3, "[WARN] ", *lst, file=sys.stderr, **d)
def err(*lst, **d):   say(2, "[ERROR]", *lst, file=sys.stderr, **d)
def fatal(*lst, **d): say(1, "[FATAL]", *lst, file=sys.stderr, **d); sys.exit(1)

# --- Shortcut ---
o = info
```
Then import
```
from watcher import info,warn,err,o
o("badness")
```            
Lesson: polymopshims is nt just an object conceot.

Not everyhting must/should be a class


Bything has a much better logging class. hNaldes smultiple out file stamps, rotating logs etc etc


