
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


# Lecture: Architecture of an Open-Source Software Repository

For a real-world example of the following, see

- Simple example of some of the following: [Lime](https://github.com/marcotcr/lime);
- More complete example: [RouteDash](https://github.com/Ishaan1402/CSC510_G20).


## Summary & Glossary of Key Terms

Before we dive into the anatomy of a production-ready repository, we must 
define the terminology used in modern software engineering (SE). 

* **CI/CD (Continuous Integration / Continuous Deployment):** Automated 
  pipelines that build, test, and deploy code whenever changes are made.
* **SCM (Source Code Management):** Systems like Git that track changes, 
  manage branches, and preserve the history of a codebase.
* **Workflow:** An automated process (often defined in YAML) that runs 
  scripts or tests in response to repository events (e.g., a push).
* **Pull Request (PR):** A proposed set of changes submitted by a developer 
  to be reviewed and merged into the main codebase.
* **Issue Tracker:** A system for logging bugs, feature requests, and tasks.
* **Code Coverage:** A metric representing the percentage of your source 
  code that is executed during automated testing.
* **Linting / Formatting:** Static code analysis tools that flag programming 
  errors, bugs, and stylistic inconsistencies.

**Lecture Summary:** We will condense the 16-point repository checklist into 
four generalized pillars: Discoverability, Documentation, Reproducibility, 
and Automation/Community. We will analyze real-world application using the 
`Ishaan1402/CSC510_G20` (RouteDash) repository as our primary case study.

---

## Pillar 1: Discoverability & Identity 
*(Covers: Software Overview, Identity, Availability, Licensing)*

### What is it?
This pillar encompasses the "Front Door" of your repository. It includes a 
clear, high-level overview of the software, identification of the target 
user base, verifiable licensing, and public availability. 

### Why is it important?
Friction prevents adoption. If a visiting engineer cannot understand what 
your project does, who it is for, or whether they are legally allowed to 
use it within 60 seconds, they will leave. A unique identity and clear 
open-source license (like MIT or Apache 2.0) are legal and social 
prerequisites for software sharing.

### Example in CSC510_G20:
* **Overview:** The `README.md` immediately defines RouteDash as a 
  "travel-aware meal planning experience."
* **Identity:** They distinguish between "Customer flows" and "Merchant 
  flows," explicitly stating who the software is for.
* **Licensing:** The repo contains a dedicated `LICENSE.md` file using the 
  OSI-approved MIT License, granting explicit permission for reuse.

---

## Pillar 2: Documentation & Support 
*(Covers: Documentation, Support, Accessibility, Future Plans)*

### What is it?
Documentation is the user manual of your software. It includes quick-start 
guides, API references, troubleshooting steps, and a published release 
history. Support dictates how users get help (e.g., ticketing systems). 
Future plans outline the 3, 6, and 12-month roadmap.

### Why is it important?
Code without documentation is practically useless to anyone but the original 
author. Good documentation scales your impact by allowing users to self-serve 
instead of demanding direct support. Roadmaps show the project is alive and 
secure for future investment.

### Example in CSC510_G20:
* **Structure:** They provide an `INSTALL.md` separate from the main README 
  to keep the front page clean while providing deep technical steps.
* **Support:** They use GitHub Issues as a public ticketing system and 
  provide an email (`team@routedash.dev`) for direct support.
* **Roadmap:** They maintain a `proj2/docs/governance.md` file that details 
  project governance and roadmap milestones.

---

## Pillar 3: The Engine Room - Architecture & Build
*(Covers: Maintainability, Open Standards, Portability, Building)*

### What is it?
This defines how the code is structured, packaged, and run. It includes 
dependency management, build instructions, architectural modularity, and 
cross-platform portability.

### Why is it important?
"It works on my machine" is an unacceptable excuse in professional software 
engineering. Explicit dependency tracking ensures deterministic builds. 
Modular architecture allows teams to work in parallel without merge 
conflicts. Portability ensures the code runs on Mac, Linux, or Windows.

### Example in CSC510_G20:
* **Portability & Build:** They use Node.js and React Native (Expo), which 
  are inherently cross-platform.
* **Dependency Management:** They use a `package-lock.json` to lock down 
  exact dependency versions, preventing upstream breakages.
* **Architecture:** The repository is cleanly separated into `server` (the 
  API layer) and `routedash` (the client app).

---

## Pillar 4: The Safety Net - SCM, CI/CD & Community 
*(Covers: Source Code Management, Testing, Community, Contributions)*

### What is it?
This is the most critical pillar for scaling a team. It involves storing 
code under revision control, running automated test suites, tracking code 
coverage, and managing contributions from outsiders via PRs and strict 
code-of-conduct policies.

### Why is it important?
Humans make mistakes. As a codebase grows, manual testing becomes 
impossible. Continuous Integration (CI) acts as an automated safety net, 
catching regressions and enforcing style guides before broken code can enter 
the `main` branch. Clear contribution guidelines (`CONTRIBUTING.md`) lower 
the social barrier for new developers.

### Deep Dive: The `/.github/workflows` Directory in CSC510_G20
The RouteDash repository is a masterclass in CI automation. The presence of 
the `/.github/workflows` directory means they are using GitHub Actions to 
automate their SE practices.

* **`backend-ci.yml` & `frontend-ci.yml`:** These scripts automatically 
  spin up virtual machines on GitHub's servers every time code is pushed. 
  They install dependencies and run the Vitest suites. If a developer pushes 
  code that breaks an existing feature, the workflow fails, and the PR 
  is blocked from merging.
* **`lint.yml` & `format.yml`:** These enforce coding standards across the 
  team. Prettier and ESLint check the code for stylistic errors, ensuring 
  the codebase reads like it was written by a single person.
* **`typecheck.yml`:** Validates TypeScript interfaces, catching runtime 
  errors at compile time.
* **Code Coverage (Codecov):** They mandate a 90% test coverage threshold. 
  The CI pipeline reports these metrics automatically.

By leveraging these workflows, the team ensures the `main` branch is 
always stable and deployable. 

### Community Engagement
* **Contributions:** `CONTRIBUTING.md` defines the exact git branching 
  strategy required. `CODE_OF_CONDUCT.md` establishes professional behavior.
* **Course Rubric Compliance:** To satisfy the CSC510 grading rubric, they 
  maintain an active `main` branch with merged PRs tracked under GitHub 
  Insights, proving that all group members are actively contributing.

## Addendum: The Anatomy of a Perfect README.md

While we discussed the repository as a whole, the `README.md` deserves its 
own focus. It is the landing page, the sales pitch, and the entry-level 
manual all rolled into one. A well-structured README generally follows a 
specific hierarchy to minimize developer friction.

Here is the standard structural breakdown:

### 1. Title and Badges
* **What:** The project name followed by dynamic status badges (e.g., CI 
  build status, code coverage percentage, current version, license type).
* **Why:** Badges provide immediate, at-a-glance trust signals. Seeing a 
  green "build: passing" and "coverage: 90%" instantly tells an engineer 
  that the project is actively maintained and rigorously tested.

### 2. The Hook (Short Description)
* **What:** A 1-3 sentence summary of what the software does, the problem 
  it solves, and the target audience.
* **Why:** Time is an engineer's most valuable resource. If they cannot 
  determine if your tool solves their specific problem within the first 
  paragraph, they will close the tab.

### 3. Table of Contents (Optional but Recommended)
* **What:** Hyperlinked list of sections within the document.
* **Why:** For comprehensive tools, users often return to the README just 
  to find the deployment steps. Let them skip the introductory pitch.

### 4. Installation & Quick Start
* **What:** The absolute minimum terminal commands required to clone, 
  build, and run the software locally (e.g., `npm install && npm start`).
* **Why:** The "Time to First 'Hello World'" is a critical metric for 
  adoption. If it takes more than 5 minutes to run, adoption plummets. 
  Keep complex configurations hidden away in a separate `INSTALL.md`.

### 5. Usage & Examples
* **What:** Basic code snippets or CLI examples showing the primary use 
  cases of the software.
* **Why:** Developers learn by example. A concrete code block is infinitely 
  more valuable than a paragraph of abstract explanation.

### 6. Architecture & Directory Structure
* **What:** A brief textual diagram or nested list explaining the repository 
  layout (e.g., separating `/proj2/server` from `/proj2/routedash`).
* **Why:** It helps new contributors build a mental model of the codebase 
  before they even open a source file.

### 7. Contributing & Support
* **What:** A call to action for Pull Requests, linking to the detailed 
  `CONTRIBUTING.md`, issue tracker, and support channels.
* **Why:** It channels community energy into proper workflows, saving 
  maintainers from having to repeatedly explain PR conventions.

### 8. License & Acknowledgments
* **What:** Explicit declaration of the open-source license (e.g., MIT) 
  and credits to authors, funders, or key dependencies.
* **Why:** It clarifies legal usage rights and builds goodwill within the 
  open-source ecosystem.


## Conclusion

A successful software repository is more than a folder of scripts. By 
implementing the four pillars—Discoverability, Documentation, Reproducibility, 
and Automation—you transform a personal project into a robust, collaborative 
software product capable of surviving in the open-source ecosystem.
