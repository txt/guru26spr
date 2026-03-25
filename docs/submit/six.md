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


# Howmework: the world's gerates hellow world function

Submit a stranscrtipy cat "cats" your source code, runs the test from part 1., 

Submit screen snaps of:

3. A github actions page of your test actions page; something like this:

 <img width="720" height="504" alt="image" src="https://github.com/user-attachments/assets/4e5b23f2-3e91-4c1d-b108-fd1b26ce5612" />
 

## hello

Write one python file hello.py that returns "hello X" where X is a parameter passed in.

Write another file test.py with a function `test_hello` that  checks that hello returns the right string.

To those files, add doc strings to each fucntion and a doc string to start of file describing what they are all about about.

Run that code with pytest (hint: pip install pytest; pytest test.py).

Document that code with some python 2 html generator (something simple like pycco or [pdoc](https://pdoc.dev/), not something more complex
like mkdocs). Send the output of that code to a sub-directory called `docs` and a file called `docs/index.html`.
To that subdirectory add a file with no content called
`.nojeykll`.

## Agile Dev Ops

Create a Github repo. Go to the settings page, find "pages" git and set "Branch" to Main" and the folder to "docs": 

Create a Github workflow that runs those tests as a side-effect of committing your code. There are many ways to do this
by the following might be useful (consult the web for other ideas). Make file a
.github/workflows/python-test.yml with contents:

```yaml
name: Python application CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: [actions/checkout@v4](https://github.com)
      - name: Set up Python ${{ matrix.python-version }}
        uses: [actions/setup-python@v5](https://github.com)
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Run tests with pytest
        run: |
          pytest
```

Greate a Github workflow to auto run your docunentation tools and send the output to docs, then rename that file docs/index.html

Make your repo "good", Add the follwing files, at least 50 lines each. For examples of good content, see [here](https://github.com/github-samples/copilot-hack/tree/main)

- README.md: The front page of your repository. It includes the project description, installation instructions, and usage examples
- LICENSE: (See https://choosealicense.com/). Crucial for open-source, this file defines how others can use, modify, and distribute your code.
- .gitignore (see https://github.com/github/gitignore): Specifies intentionally untracked files that Git should ignore (e.g., node_modules, .env, compiled binaries).
- CONTRIBUTING.md (see copilot-hack) Guidelines for external contributors, explaining how to submit issues or pull request
- .github/ folder: Contains community health files, such as ISSUE_TEMPLATE.md, PULL_REQUEST_TEMPLATE.md, and default workflows
- CHANGELOG.md: Documents notable changes for each version of the project
- CODE_OF_CONDUCT.md (see copilot_hack): Defines community standards for interaction
see Essential Files for a Professional GitHub Repository on Medium. 
- src/: Contains helper scripts for tasks like setup, building, or testing see Essential Files for a Professional GitHub Repository on LinkedIn.
- docs/: Dedicated folder for detailed project documentation see Creating a default community health file on GitHub Docs. 
- tests/: Your test code, will calls your src/hello.py files.

Write a python package

- Write a pyproject.toml file that enables local install (using `python3 -m pip install -e .`)
- Change directories far away from your code and show you can run your code.


W


