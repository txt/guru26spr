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

# Package Management: From Chaos to `pip install`


## Part 1: The Problem 

### Why Should You Care?

You wrote a brilliant Python script. It works on your
laptop. Your colleague wants to use it. What do you send them?

**Attempt 1: Email the file.**

```
Hey, here's ezr.py. Just run it.
```

Your colleague replies:

> It says `ModuleNotFoundError: No module named 'ezr'`.
> Also, I'm on Python 3.9. Also, what's a "CSV"?
> Also, I put it in my Downloads folder and now
> `import ezr` doesn't work.

**Attempt 2: Write a README.**

```
1. Download ezr.py and ezeg.py
2. Put them in the same directory
3. Make sure you have Python 3.12+
4. Run: python ezeg.py --h
```

Better. But what happens when:

- You release version 0.9.2 and they're still on 0.9.1?
- They have another project that also has an `ezr.py`?
- They want `ezr` to be a command they can type anywhere,
  not just from that one directory?
- Twenty people are using your code and you need to push
  a bugfix to all of them?

These are the problems that package managers solve.

### The Five Headaches

Every software distribution system eventually has to deal with
the same five headaches:

1. **Discovery** — How do I find software that does X?
2. **Installation** — How do I get it onto my machine?
3. **Dependency Resolution** — What else do I need?
4. **Versioning** — Which version works with my stuff?
5. **Removal** — How do I cleanly uninstall it?

Before package managers, the answer to all five was:
"Read the README and pray."

---

## Part 2: A Brief History of Not Losing Your Mind 

### The Dark Ages: Tarballs and Makefiles (1970s–1990s)

Unix software was distributed as compressed archives (`.tar.gz`).
To install something:

```bash
tar xzf cool-tool-1.3.tar.gz
cd cool-tool-1.3
./configure
make
make install
```

The `configure` script would probe your system — do you have
the right C compiler? The right version of `libpng`? The right
kernel headers? If anything was missing, you got a cryptic error
and had to go find *that* dependency, compile *it* from source,
and try again.

This was called **dependency hell**, and it was real. Installing
one program could take hours of recursive tarball unpacking.

### The Revolution: apt and dpkg (1998)

Debian Linux introduced `apt` (Advanced Package Tool), which
solved dependency hell by maintaining a central registry of
every package and what it depends on.

```bash
apt install python3    # Installs Python AND everything it needs
```

The key insight: **a package isn't just code — it's code plus
metadata**. A `.deb` package contains:

- The actual files to install
- A list of dependencies (other packages required)
- Version constraints (`requires libfoo >= 2.1`)
- Pre/post install scripts
- Where to put files on the filesystem

This was transformative. For the first time, you could install
complex software with a single command.

### The Ecosystem Explodes (2000s)

Every language community independently reinvented package
management:

| Year | System | Language | Registry |
|------|--------|----------|----------|
| 1998 | apt/dpkg | System (Debian) | debian.org |
| 2003 | CPAN | Perl | cpan.org |
| 2003 | RubyGems | Ruby | rubygems.org |
| 2004 | PyPI/pip | Python | pypi.org |
| 2010 | npm | JavaScript | npmjs.com |
| 2013 | Cargo | Rust | crates.io |
| 2014 | Homebrew | macOS system | brew.sh |

Each one learned from the last. Each one made new mistakes.

### The Left-Pad Incident (2016)

A JavaScript developer named Azer Koçulu unpublished a tiny
11-line npm package called `left-pad`. It did one thing: pad
a string with spaces on the left.

Thousands of packages depended on it. When it vanished,
builds broke worldwide — including at Facebook, Spotify,
and Netflix. The entire Node.js ecosystem briefly collapsed
because of an 11-line function.

**Lesson:** Package managers create a web of trust and
dependency. That web is only as strong as its weakest node.

---

## Part 3: What Makes a Good Package Manager? 

### The Desired Features

A good package manager provides:

**For users:**

- One-command install: `pip install ezr`
- One-command remove: `pip uninstall ezr`
- Version pinning: `pip install ezr==0.9.1`
- Isolation: installing package A doesn't break package B

**For developers:**

- Simple packaging: describe your project in one config file
- A registry: upload once, anyone can install
- Reproducibility: same install today and next year
- CLI entry points: `pip install ezr` creates the `ezr` command

**For the ecosystem:**

- Dependency resolution: if A needs B≥2.0 and C needs B<3.0,
  figure out which B satisfies both
- Security: verify packages haven't been tampered with
- Namespacing: two developers can't accidentally overwrite
  each other's package

### The Tradeoffs

No package manager gets everything right. Here's where the
major ones sit:

| Feature | apt | pip | npm | cargo |
|---------|-----|-----|-----|-------|
| System-wide install | ✓ | ✓* | ✗ | ✗ |
| Per-project isolation | ✗ | venv | ✓ | ✓ |
| Lock files | ✗ | ✗** | ✓ | ✓ |
| Compiled code | ✓ | sometimes | ✗ | ✓ |
| Dependency resolution | good | improving | complex | excellent |
| Security audit | ✓ | basic | `npm audit` | `cargo audit` |

*\* pip installs user-wide by default, system-wide with sudo*
*\*\* pip has `pip freeze > requirements.txt` but no true lock file yet*

---

## Part 4: The Linux Package Flow 

How does a piece of software travel from a developer's laptop
to millions of machines? Here's the standard flow for a
Linux distribution:

```
Developer writes code
        │
        ▼
┌───────────────┐
│  Source Code  │  (GitHub, GitLab, etc.)
│  + Makefile   │
└───────┬───────┘
        │  maintainer packages it
        ▼
┌───────────────┐
│  .deb / .rpm  │  (compiled binary + metadata)
│  package file │
└───────┬───────┘
        │  uploaded to
        ▼
┌───────────────┐
│   Repository  │  (archive.ubuntu.com, etc.)
│   Server      │  mirrors worldwide
└───────┬───────┘
        │  apt update / yum update
        ▼
┌───────────────┐
│  Local Index  │  (your machine knows what's available)
└───────┬───────┘
        │  apt install python3
        ▼
┌───────────────┐
│  Dependency   │  "python3 needs libpython3.12,
│  Resolver     │   libssl3, zlib1g..."
└───────┬───────┘
        │  downloads + installs all of them
        ▼
┌───────────────┐
│  /usr/bin/    │  (binaries)
│  /usr/lib/    │  (libraries)
│  /etc/        │  (config)
└───────────────┘
```

**Python's pip follows a similar but simpler flow:**

```
Developer writes code
        │
        ▼
┌───────────────┐
│  Source Code  │  ezr.py, ezeg.py
│  + pyproject. │  pyproject.toml
│    toml       │
└───────┬───────┘
        │  python -m build
        ▼
┌───────────────┐
│  .whl / .tar  │  (wheel or sdist archive)
│  distribution │
└───────┬───────┘
        │  twine upload
        ▼
┌───────────────┐
│    PyPI       │  (pypi.org — the Python Package Index)
└───────┬───────┘
        │  pip install ezr
        ▼
┌───────────────┐
│ Site-packages │  (~/.local/lib/python3.12/site-packages/)
│  + bin/ezr    │  (console script entry point)
└───────────────┘
```

---

## Part 5: Python's pip — A Deep Dive 

### pyproject.toml: The One File That Rules Them All

Modern Python uses a single file — `pyproject.toml` — to
describe everything about a package. Let's read ours line
by line:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

This says: "To build this package, you need setuptools version
61 or higher." The build system is separate from the package
itself — this is a lesson learned from years of Python packaging
chaos where `setup.py` was both the installer and the thing
being installed (a chicken-and-egg problem).

```toml
[project]
name = "ezr"
version = "0.9.1"
readme = "README.md"
description = "Explainable multi-objective optimization"
authors = [{name = "Tim Menzies", email = "timm@ieee.org"}]
license = {text = "MIT"}
requires-python = ">=3.12"
dependencies = []
```

This is the metadata that PyPI displays. Note:

- **`name`** must be unique on PyPI. Once you claim `ezr`,
  nobody else can use it.
- **`requires-python = ">=3.12"`** means pip will refuse to
  install this on Python 3.11. We need 3.12 for the `type`
  statement syntax.
- **`dependencies = []`** — zero dependencies. This is
  unusual and deliberate. `ezr` uses only the standard
  library.

```toml
[project.optional-dependencies]
test = ["pytest"]
```

Optional extras. `pip install ezr` doesn't install pytest.
But `pip install ezr[test]` does. This keeps the core install
lightweight while letting developers get the test tools.

```toml
[project.scripts]
ezr = "ezeg:cli"
```

**This is the magic line.** It says: "When someone installs
this package, create a command called `ezr` that calls the
`cli()` function in `ezeg.py`."

After `pip install -e .`, you can type `ezr --h` from
anywhere on your system. pip generated a tiny wrapper script
in your PATH that does the equivalent of:

```python
from ezeg import cli
cli()
```

```toml
[tool.setuptools]
py-modules = ["ezr", "ezeg"]
```

Because our package is two flat `.py` files (not a
directory with `__init__.py`), we explicitly list the modules.
Setuptools would normally look for a folder named `ezr/`.

### The Three Modes of Installation

**Mode 1: Editable install (development)**

```bash
pip install -e .
```

The `-e` flag creates a symlink. Changes to `ezr.py` and
`ezeg.py` take effect immediately — no reinstall needed.
This is what you use while actively developing.

**Mode 2: Regular install (users)**

```bash
pip install ezr
```

Copies files into `site-packages`. Changes to the source
don't affect the installed version. This is what end users do.

**Mode 3: No install (quick and dirty)**

```bash
python ezeg.py --h
```

Works if you're in the directory. No pip involved. But the
`ezr` command doesn't exist system-wide.

### What Actually Happens During `pip install`

When you run `pip install ezr`, pip:

1. **Queries PyPI** for the package named `ezr`
2. **Downloads** the latest compatible wheel (`.whl`)
3. **Checks `requires-python`** — refuses if your Python
   is too old
4. **Resolves dependencies** — for each package in
   `dependencies`, recursively installs them first
5. **Copies files** into `site-packages/`
6. **Creates console scripts** — the `ezr` command
7. **Records metadata** — so `pip uninstall ezr` knows
   exactly which files to remove

### Virtual Environments: Don't Pollute the Global

What if Project A needs `numpy==1.24` and Project B needs
`numpy==2.0`? They can't both be installed system-wide.

```bash
python -m venv myenv        # create isolated environment
source myenv/bin/activate   # enter it
pip install ezr             # installs ONLY in myenv/
deactivate                  # leave it
```

Each virtual environment has its own `site-packages`. This
is Python's answer to the isolation problem that npm solves
with `node_modules/` and Rust solves with `target/`.

### Building and Publishing

To share your package with the world:

```bash
pip install build twine     # one-time setup
python -m build             # creates dist/ezr-0.9.1.tar.gz
                            #     and dist/ezr-0.9.1-py3-none-any.whl
twine upload dist/*         # pushes to PyPI
```

The `.whl` (wheel) file is just a ZIP archive:

```
ezr-0.9.1-py3-none-any.whl
├── ezr.py
├── ezeg.py
└── ezr-0.9.1.dist-info/
    ├── METADATA        (from pyproject.toml)
    ├── WHEEL           (format version)
    ├── RECORD          (checksums of every file)
    └── entry_points.txt (the ezr = ezeg:cli mapping)
```

The filename `py3-none-any` means: Python 3, no C
extensions, any platform. A package with compiled C code
would say something like `cp312-cp312-manylinux_x86_64`.

### The `from ezr import *` Question

When `ezeg.py` does `from ezr import *`, Python looks for
`ezr` in this order:

1. `ezr/` directory with `__init__.py` (a package)
2. `ezr.py` file (a module)

**This bit us earlier in class.** There was an old `ezr/`
directory sitting around, and Python loaded it instead of
the flat `ezr.py`. The fix was `rm -rf ezr/`. Lesson:
a package directory always shadows a module file of the
same name.

Related: `__all__` controls what `import *` exports.
Names starting with `_` are excluded by default. We had
to add:

```python
__all__ = ([k for k in globals() if not k.startswith('_')]
           + ['_nest', '_cluster', '_treeCuts', '_treeSplit'])
```

to export our private helpers.

### requirements.txt vs pyproject.toml

You'll see older projects with a `requirements.txt`:

```
numpy==1.24.3
pandas>=2.0,<3.0
scikit-learn~=1.3
```

This is a *consumer-side* lock: "here are the exact versions
I tested with." It's generated by `pip freeze > requirements.txt`
and installed with `pip install -r requirements.txt`.

`pyproject.toml`'s `dependencies` is a *producer-side*
specification: "here's what my package needs, loosely."
Both serve a purpose. For a library like `ezr`, the toml
is sufficient. For a deployed application, you want both.

---

## Part 6: Package Managers Compared 

### System-Level: apt, yum, brew

These manage your *operating system*. They install binaries,
libraries, and system services.

```bash
apt install python3          # Debian/Ubuntu
yum install python3          # Red Hat/CentOS
brew install python@3.12     # macOS
```

You don't use these for Python libraries. They're too
coarse-grained and update too slowly.

### Language-Level: pip, npm, cargo

These manage libraries *within* a language ecosystem.

```bash
pip install numpy            # Python
npm install express          # JavaScript
cargo add serde              # Rust
```

They're fast, fine-grained, and understand language-specific
conventions (like Python's `site-packages` or npm's
`node_modules`).

### The Layering

In practice, you use both:

```
┌──────────────────────────────┐
│  Your Python Application     │
│  (ezr, numpy, pandas...)     │
│  Managed by: pip             │
├──────────────────────────────┤
│  Python Runtime              │
│  Managed by: apt/brew        │
├──────────────────────────────┤
│  Operating System            │
│  Managed by: apt/brew        │
└──────────────────────────────┘
```

A common beginner mistake is installing Python packages
with `apt` (`apt install python3-numpy`). This works but
gives you old versions and can't be easily isolated per
project.

---

## Part 7: Practical Exercise — Our Package 

### The ezr Package Structure

```
ezr/
├── ezr.py           474 lines — the library
├── ezeg.py          261 lines — the driver + tests
├── pyproject.toml    21 lines — the packaging config
├── README.md                  — the man page
├── LICENSE.md                 — MIT license
└── Makefile                   — developer shortcuts
```

Two Python files. One config file. That's the whole package.

### Try It Yourself

```bash
# Clone and install
git clone http://github.com/timm/ezr
cd ezr
pip install -e .

# Use the CLI
ezr --h
ezr --see ~/gits/moot/optimize/misc/auto93.csv
ezr --seed=42 --test ~/gits/moot/optimize/misc/auto93.csv

# Run tests
pip install pytest
pytest ezeg.py -v
pytest ezeg.py -k test_num

# Use as a library
python3 -c "from ezr import *; print(the.seed)"
```

### What Didn't We Need?

Notice what's *absent* from our package:

- No `setup.py` (the old way — replaced by `pyproject.toml`)
- No `setup.cfg` (another old way)
- No `MANIFEST.in` (setuptools auto-detects our files)
- No `__init__.py` (we're flat modules, not a package dir)
- No C extensions (pure Python, so `py3-none-any`)
- No dependencies (stdlib only)

This is the minimal viable package. Two `.py` files and
a `.toml`. Everything else is optional.

## Part 8. Some Usecases


Real packaging problems you'll hit, and the `pyproject.toml`
fields that save you.

### 8a. "Your package broke my old Python"

You used `match` statements (3.10+) and a user on 3.9 gets
a syntax error at import time. No helpful message — just a
traceback.

```toml
[project]
requires-python = ">=3.12"
```

Now pip refuses to install on older Pythons with a clear
message *before* downloading anything. For `ezr`, we need
3.12 because of `type Row = list[Atom]` syntax.

### 8b. "I installed it but there's no command"

The user does `pip install ezr`, then types `ezr` and gets
`command not found`. They expected a CLI tool but got a
library.

```toml
[project.scripts]
ezr = "ezeg:cli"
```

This creates a console entry point. pip generates a wrapper
script in the user's PATH. You can define multiple commands
from one package:

```toml
[project.scripts]
ezr = "ezeg:cli"
ezr-bench = "ezeg:benchmark_cli"
```

### 8c. "I need pandas but only sometimes"

Your core library is dependency-free, but the plotting
module needs matplotlib, and the test suite needs pytest.
You don't want every user installing all of that.

```toml
[project]
dependencies = []                    # core: zero deps

[project.optional-dependencies]
plot = ["matplotlib>=3.7"]           # pip install ezr[plot]
test = ["pytest>=7.0"]               # pip install ezr[test]
all  = ["matplotlib>=3.7", "pytest"] # pip install ezr[all]
```

Users pick what they need. CI pipelines do
`pip install ezr[test]`. Data scientists do
`pip install ezr[plot]`. Minimalists get the bare library.

### 8d. "Which files are part of the package?"

You have a `scratch/` folder, some `.ipynb` notebooks, a
`docs/` directory, and random test data CSVs. Setuptools
tries to include everything. Your wheel balloons to 50MB.

```toml
[tool.setuptools]
py-modules = ["ezr", "ezeg"]        # ONLY these two files
```

For directory-based packages, you can be explicit:

```toml
[tool.setuptools.packages.find]
include = ["ezr*"]                   # only ezr/ and subpackages
exclude = ["tests*", "scratch*"]     # never ship these
```

Or use a `MANIFEST.in` for source distributions, but the
toml approach is cleaner and covers most cases.

### 8e. "My package name was taken on PyPI"

You called it `stats` but that name is already claimed by
a package uploaded in 2011 that has 12 downloads total. PyPI
names are globally unique and first-come-first-served.

```toml
[project]
name = "ezr-stats"                   # PyPI name (hyphens ok)
```

```toml
[tool.setuptools]
py-modules = ["ezr_stats"]           # Python import name (underscores)
```

The *install* name and the *import* name can differ. Users
do `pip install ezr-stats` but `import ezr_stats`. This is
confusing and you should avoid it when possible, but
sometimes the namespace is crowded.

### 8f. "Works on my machine but not on Windows"

Your package shells out to `grep` or uses `/tmp/` paths.
You can warn Windows users away, or provide platform-specific
dependencies:

```toml
[project]
requires-python = ">=3.12"

# Platform-specific deps using environment markers
dependencies = [
    "pyreadline3; sys_platform == 'win32'",
    "gnureadline; sys_platform == 'darwin'",
]
```

Environment markers are a mini-language for conditional
dependencies. Common markers: `sys_platform`, `python_version`,
`os_name`, `platform_machine`. This is how packages ship
one toml that works everywhere.

### 8g. "Nobody can find my package on PyPI"

Your package page on pypi.org shows a bare name and one-line
description. No README, no links, no way to report bugs.

```toml
[project]
name = "ezr"
description = "Explainable multi-objective optimization"
readme = "README.md"
license = {text = "MIT"}
keywords = ["optimization", "explainable-ai", "decision-trees"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "http://github.com/timm/ezr"
Issues   = "http://github.com/timm/ezr/issues"
Docs     = "http://github.com/timm/ezr#readme"
```

The `readme` field renders your entire README.md on the PyPI
page. Classifiers are a controlled vocabulary — PyPI uses them
for search and filtering. The `urls` section puts clickable
links on the sidebar.

### 8h. "pytest keeps picking up random files"

You run `pytest` and it discovers test functions inside
your library code, or crawls into `node_modules`, or runs
files you didn't intend. The test suite takes forever and
half the tests fail because they're from a different project.

```toml
[tool.pytest.ini_options]
testpaths = ["ezeg.py"]             # ONLY look here
addopts = "-v --tb=short"           # always verbose, short tracebacks
markers = [
    "slow: marks tests as slow (deselect with '-m not slow')",
]
```

This lives in the same `pyproject.toml`. No separate
`pytest.ini` or `setup.cfg` needed. The `testpaths` field
is the leash — pytest only sniffs where you point it.

### 8i. "I reformatted and now git blame is useless"

You ran `black` or changed your tab width and every line
changed. Or worse, different contributors use different
formatters and every PR is a style war.

```toml
[tool.black]
line-length = 90
target-version = ["py312"]

[tool.ruff]
line-length = 90
select = ["E", "F", "W"]            # pyflakes + pycodestyle
ignore = ["E501"]                    # we handle line length ourselves

[tool.ruff.per-file-ignores]
"ezeg.py" = ["F811"]                # allow redefined test fixtures
```

Tools like `black`, `ruff`, `mypy`, and `isort` all read
their config from `pyproject.toml`. One file governs
formatting, linting, type checking, testing, *and* packaging.
Before `pyproject.toml`, you'd have `setup.py`, `setup.cfg`,
`.flake8`, `mypy.ini`, `pytest.ini`, and `tox.ini` — six
config files doing what one now does.

### 8j. "I released 0.9.1 with a bug and can't take it back"

You pushed to PyPI and immediately realized you shipped
a broken version. PyPI doesn't let you re-upload the same
version number (even if you delete it). You need 0.9.2.
But how do you manage version numbers sanely?

```toml
[project]
dynamic = ["version"]               # don't hardcode it here

[tool.setuptools.dynamic]
version = {attr = "ezr.__version__"}  # read from ezr.py
```

Then in `ezr.py`:

```python
__version__ = "0.9.2"
```

Single source of truth. Or go further — derive the version
from git tags:

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm>=8.0"]

[tool.setuptools_scm]
# version auto-derived from git tags: git tag v0.9.2
```

Now `git tag v0.9.3 && python -m build` automatically stamps
the right version. No file to edit, no chance of forgetting.

### 8k. "I need to ship data files with my package"

Your code loads CSV files, templates, or config defaults at
runtime. They're in the repo but `pip install` doesn't copy
them because setuptools only ships `.py` files by default.
```toml
[tool.setuptools.package-data]
ezr = ["data/*.csv", "templates/*.html", "defaults.json"]
```

For flat-module packages like ours (no `ezr/` directory),
use a data directory explicitly:
```toml
[tool.setuptools.data-files]
"share/ezr/data" = ["data/*.csv"]
```

The hard part is *finding* those files at runtime. Paths
break when code moves from a git checkout to `site-packages`.
Never use `__file__` with relative paths. Use the standard
library instead:
```python
from importlib.resources import files

# Python 3.12+
data_dir = files("ezr").joinpath("data")
csv_path = data_dir.joinpath("auto93.csv")
text = csv_path.read_text()
```

`importlib.resources` works whether the package is installed
normally, installed editable, or even running from a ZIP.
It's the one correct way to reference package data.

### 8l. "I want to ship multiple commands"

Your package has a main tool, a benchmarking script, a
data converter, and an admin utility. You want each to be
its own command.
```toml
[project.scripts]
ezr       = "ezeg:cli"              # the main driver
ezr-bench = "ezeg:bench_cli"        # benchmarking entry point
ezr-conv  = "ezconv:main"           # data format converter
```

Each entry maps a command name to a `module:function` pair.
After `pip install -e .`, all three commands appear in PATH.
They can live in the same file or different files — pip
doesn't care.

For commands that should only be available inside Python
(not the shell), use `gui-scripts` or `entry-points`:
```toml
[project.gui-scripts]
ezr-viz = "ezviz:launch"            # no console window on Windows

[project.entry-points."ezr.plugins"]
trees    = "ezr:treeGrow"           # plugin discovery system
clusters = "ezr:kmeans"
```

The `entry-points` section is how plugin architectures work.
A host application calls `importlib.metadata.entry_points()`
to discover what's registered, without importing anything
until needed. Pytest, tox, and setuptools itself all use
this mechanism.

### 8m. "I want to build docs as part of the package"

Your project has Sphinx or MkDocs documentation that should
be buildable by anyone who clones the repo. The doc toolchain
has its own dependencies that users don't need.
```toml
[project.optional-dependencies]
test = ["pytest>=7.0"]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
    "mkdocstrings[python]>=0.24",
]
dev = ["ezr[test,docs]"]            # one group to rule them all
```

Contributors do `pip install -e .[dev]` and get everything.
Users get nothing extra. The `dev` group is a convention —
it combines test and docs deps into a single install target.

Configure the doc builder in the same toml:
```toml
[tool.mkdocs]
# mkdocs doesn't read pyproject.toml yet, but many tools do.
# For mkdocs, you still need mkdocs.yml. But Sphinx can:

[tool.sphinx]
project = "ezr"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
```

For tools that don't read `pyproject.toml` yet (like mkdocs),
you can at least automate the build in your Makefile:
```makefile
docs:
	pip install -e .[docs]
	mkdocs build
```

The key insight: documentation dependencies are just another
optional group. 

```markdown
### 8n. "Where do I put my tests — inside or outside the package?"

This is a genuine debate. There are three options, each with
real tradeoffs.

**Option A: Tests outside the package (the common convention)**

```
myproject/
├── ezr.py
├── pyproject.toml
└── tests/
    ├── test_columns.py
    └── test_trees.py
```

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

Pros: tests never ship to users. `pip install ezr` is lean.
Tests are forced to use public imports (`from ezr import Num`),
which proves the installed package actually works.

Cons: tests are invisible to users who might want to verify
their install. Tests live far from the code they test. If
you rename a function in `ezr.py` and forget to update
`tests/`, nothing warns you until you run pytest.

This is what setuptools documentation recommends, and what
most PyPI libraries do.

**Option B: Tests inside the package**

```
ezr/
├── __init__.py
├── columns.py
├── tests/
│   ├── test_columns.py
│   └── test_trees.py
└── ...
```

```toml
[tool.pytest.ini_options]
testpaths = ["ezr/tests"]
```

Pros: tests ship with the code, so users can run
`python -m pytest --pyargs ezr` to verify their install
works. Tests live next to the code they test. Django, NumPy,
SciPy, and requests all do this.

Cons: every `pip install` includes test code the user
probably doesn't need. Adds a few KB (or MB if you have
test fixtures and data files).

**Option C: Tests in a flat peer file (what we did)**

```
myproject/
├── ezr.py          # library
├── ezeg.py         # tests + CLI driver
└── pyproject.toml
```

```toml
[tool.setuptools]
py-modules = ["ezr", "ezeg"]

[tool.pytest.ini_options]
testpaths = ["ezeg.py"]
```

Pros: absolute minimum structure — two files, no directories.
Tests and demos are the same thing, which works perfectly for
teaching. `pytest ezeg.py` and `ezr --num` run the same
functions. Students see everything without navigating folders.

Cons: `pip install ezr` also installs `ezeg.py` into
site-packages. Test code ships with the library. Doesn't
scale past a few hundred lines of tests.

### 8o. "My tests are also my tutorials — how do I serve both?"

In a teaching codebase, your tests *are* the documentation.
`test_num()` isn't just checking that the mean equals 30 —
it's showing a student how `Num` works. Hiding tests in a
`tests/` folder nobody opens defeats the purpose.

The tension: pytest wants functions named `test_*`. Students
want runnable examples. The CLI wants dispatchable commands.
Can one function be all three?

**Yes. Here's the pattern we use:**

```python
# ezeg.py

def test_num():
  """Test numeric incremental updates."""
  c = adds([10, 20, 30, 40, 50], Num())
  assert c.mu == 30 and 15.8 < spread(c) < 15.9
```

This single function serves three masters:

- **pytest** finds it by name and runs the asserts
- **`ezr --num`** dispatches it via `globals().get(f"test_{k}")`
- **a student** reads it as a five-line tutorial on `Num`

The trick that makes this work is the `autouse` fixture
for pytest and the `random.seed(the.seed)` reset in the
CLI loop — both ensure reproducibility regardless of which
entry point runs the function:

```python
# pytest gets this fixture automatically
@pytest.fixture(autouse=True)
def _seed():
  random.seed(the.seed)
```

```python
# CLI reseeds before each dispatch
def cli():
  args = sys.argv[1:]
  while args:
    random.seed(the.seed)      # same reset, different entry point
    k = re.sub(r"^-+", "", args.pop(0))
    if fn := globals().get(f"test_{k}"):
      fn(...)
```

**When does this pattern break?** When your test suite grows
beyond what one person can read in a sitting. If `ezeg.py`
hits 1000 lines, split it into `ezeg_columns.py`,
`ezeg_trees.py`, etc. — still flat files, still peers of
`ezr.py`, still following the same three-masters pattern.
Update the toml:

```toml
[tool.setuptools]
py-modules = ["ezr", "ezeg_columns", "ezeg_trees", "ezeg_cluster"]

[tool.pytest.ini_options]
testpaths = ["ezeg_columns.py", "ezeg_trees.py", "ezeg_cluster.py"]
```

The flat-file approach scales further than you'd expect.
You only need directories when you have dozens of modules
or deep internal structure. For a 500-line library with
24 test functions, two files is the right answer.
```


## Summary

| Concept | One-Liner |
|---------|-----------|
| Package manager | Automates finding, installing, updating, and removing software |
| Dependency hell | When installing A requires B requires C requires a different A |
| `pyproject.toml` | The single config file for modern Python packages |
| `pip install -e .` | Editable install — symlinks to your source for development |
| `pip install ezr` | Regular install from PyPI for end users |
| `[project.scripts]` | Maps a CLI command name to a Python function |
| Virtual environment | Isolated Python + packages per project |
| Wheel (`.whl`) | The distribution format — a ZIP with code + metadata |
| PyPI | The Python Package Index — the central registry |
| `__all__` | Controls what `from X import *` exports |

---

## Review Questions

### Quick 

1. What problem does `requires-python = ">=3.12"` solve?

2. In our `pyproject.toml`, what does `ezr = "ezeg:cli"` under
   `[project.scripts]` actually do when someone runs `pip install`?

3. Why does `pip install -e .` use a dot? What does the dot
   refer to?

4. If `ezr/` (a directory) and `ezr.py` (a file) both exist,
   which does `import ezr` load? Why?

5. Why is `dependencies = []` unusual, and why is it a feature
   of this particular codebase?

### Deeper 

6. The Left-Pad incident broke thousands of builds because of
   an 11-line package. What package management feature could
   prevent this? What are the tradeoffs of that feature?

7. Our `pyproject.toml` lists `pytest` under
   `[project.optional-dependencies]` instead of `dependencies`.
   Explain why this design choice matters for a user who just
   wants to run `ezr --see data.csv`.

8. Compare how `apt`, `pip`, and `cargo` handle the isolation
   problem (two projects needing different versions of the
   same library). Which approach do you think is best and why?

9. The `__all__` list in `ezr.py` explicitly includes names
   like `_nest` and `_cluster`. Why were these excluded by
   default, and what would break in `ezeg.py` without this fix?

10. A developer puts `numpy==1.24.3` in both `pyproject.toml`
    dependencies and `requirements.txt`. A colleague argues
    you should only pin the exact version in `requirements.txt`
    and use `numpy>=1.24` in `pyproject.toml`. Who is right,
    and why does the distinction matter?
