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


# Law and Software Engineering: From the Garage to the Courtroom
### Who Owns Code — and What That Means for You

> *"Modern software is assembled from pre-made parts where 85–97% of code*
> *is reused from external sources."*
> — Martínez & Durán (2021)

> *"Who can afford to do professional work for nothing?"*
> — Bill Gates, Open Letter to Hobbyists (1976)

These two quotes, 45 years apart, define a massive inversion in how we
think about software. This lecture traces that inversion — from the garage
hobbyist who shared everything, through the licence wars, to the supply-
chain liability of today — and asks: **what should you, as a software
engineer in 2026, actually do about it?**

---

## Road Map

1. The Homebrew Era: when code was free
2. The First Enclosure: Gates' manifesto
3. The Moral Rebellion: Stallman and the Four Freedoms
4. The Corporate Civil Wars and the Bazaar
5. Wall Street Validates the Commons
6. Creative Commons: Lessig extends the logic
7. The Backpacking Doctrine: SQLite vs. the Oracle Trap
8. Martínez: The 97% Reality and Supply Chain Risk
9. The AI Legal Frontier: Samuelson (2025)
10. The EU Cyber Resilience Act
11. Licence Choices: A Practical Field Guide
12. Putting It All Together

---

## 1. The Homebrew Era (1975–1976)

### 1.1 What Was the Homebrew Computer Club?

Before Silicon Valley meant billion-dollar exits, it meant a parking lot
in Menlo Park. The **Homebrew Computer Club** (est. January 1975, Stanford
Linear Accelerator Center) was a loose collective of hardware hackers —
engineers, students, radio hobbyists — who met fortnightly to share
schematics, swap chips, and pass around software on **paper tape**.

Famous early members included **Steve Wozniak** ("the Woz"), who debuted
a prototype of what became the Apple I at a club meeting in 1976. The
club's ethos was rooted in the **MIT hacker culture** of the 1960s and
70s, documented by Steven Levy in *Hackers: Heroes of the Computer
Revolution* (1984):

- *All information should be free.*
- *Mistrust authority — promote decentralisation.*
- *Computers can change your life for the better.*
- *You can create art and beauty on a computer.*

In this world, **hardware was the scarce resource**. Software — "programs"
— existed to make hardware useful. Sharing it was rational: the more
people improved a program, the better it got for everyone. The idea that
you could *own* a list of instructions and prevent others from reading it
would have seemed bizarre. Code circulated on paper tape, photocopied
sheets, and early bulletin boards. Nobody charged for it.

This was the world that Bill Gates was about to blow up.

---

## 2. The First Enclosure: Gates' Open Letter (1976)

In January 1976, Gates and Allen had written **Altair BASIC** — an
interpreter for the MITS Altair 8800, the first mass-market personal
computer kit. Hobbyists, including many Homebrew members, were copying
and sharing that BASIC freely.

Gates was furious. In February 1976 he published the
[Open Letter to Hobbyists](https://en.wikipedia.org/wiki/Open_Letter_to_Hobbyists):

> *"As the majority of hobbyists must be aware, most of you steal your*
> *software. Hardware must be paid for, but software is something to*
> *share. Who cares if the people who worked on it get paid?"*

The letter made several arguments that echo to this day:

1. **Labor deserves compensation.** Writing good software takes
   professional time. If it is given away, professionals cannot
   afford to write it.
2. **Sharing is theft.** Using something without paying is morally
   equivalent to stealing hardware.
3. **Quality depends on payment.** Without revenue, you get amateur code.

Gates was not entirely wrong — professional labour does need funding.
But the letter established the **"Software as Property" paradigm** that
would dominate the next two decades:

- Software ships without source code.
- You buy a *licence to use*, not ownership of a copy.
- The EULA (End User Licence Agreement) is born.

The Homebrew community's response was mixed. Many accepted it. Some did
not. One person in particular found it morally intolerable.

---

## 3. The Moral Rebellion: Stallman and the Four Freedoms

### 3.1 The MIT AI Lab and Symbolics

Richard Stallman (universally known as **RMS**) worked as a programmer
at the **MIT AI Lab** in the late 1970s. The lab ran a culture of
complete openness: source code was shared, hardware was hackable, and
the operating system — written in **Lisp** — was a communal artifact
everyone could improve.

In the early 1980s, two companies spun out of the lab: **Lisp Machines
Inc. (LMI)** and **Symbolics**, both selling commercial versions of the
lab's Lisp Machine hardware and OS. Initially both shared improvements
back to the lab. Then Symbolics stopped. They continued taking the lab's
open code, adding commercial features, and refusing to return those
features to the community.

Stallman, refusing to let the community version fall behind, spent
**two years** manually re-implementing every feature Symbolics added —
just to keep the public version competitive. It was exhausting and
demoralising. It radicalised him.

### 3.2 The Xerox Printer

Around the same time, Xerox donated a state-of-the-art laser printer to
the AI Lab. The printer jammed frequently. No problem — the lab had
fixed printer firmware before. But this time, Xerox had not provided
source code. The printer was a black box. When Stallman asked a Xerox
employee for the driver source, the employee refused: he had signed an
NDA.

To Stallman, this was a fundamental **betrayal of the scientific method**:
you cannot build on, fix, or verify something you cannot read. The
printer incident is often cited as the moment Stallman decided the
problem was systemic and required a systemic response.

### 3.3 GNU and the GPL

In 1983 Stallman announced the **GNU Project** (GNU's Not Unix) — an
effort to write a complete free operating system from scratch. In 1985
he published the [GNU Manifesto](https://www.gnu.org/gnu/manifesto.html).
In 1989 he released **GNU General Public Licence v1 (GPL)**.

The GPL is a legal masterstroke. It uses **copyright law** — the very
mechanism Gates used to enclose software — to *guarantee openness*. The
mechanism is called **copyleft**:

> *If you distribute software under the GPL, any derivative work you*
> *distribute must also be under the GPL.*

You cannot take GPL code, add proprietary features, and sell a black
box. The licence forces reciprocity. Stallman called it "jiu-jitsu":
using the enemy's weapon against them.

### 3.4 The Four Essential Freedoms

The Free Software Foundation (FSF, est. 1985) defines free software by
four freedoms users must have:

| # | Freedom |
|---|---------|
| 0 | Run the program for **any purpose** |
| 1 | **Study** how it works (requires source code access) |
| 2 | **Redistribute** copies to help others |
| 3 | Distribute copies of your **modified** versions |

Note that freedom 0 is numbered zero deliberately: it is the most
fundamental. Note also that "free" here means **free as in speech**, not
free as in beer. You can charge money for GPL software; you just cannot
remove the freedoms.

> [!TIP]
> **Developer choice:** If your goal is to prevent the "Symbolics
> enclosure" — someone taking your community project, locking it
> down, and selling it back to you — use the **GPL**. It is legally
> binding copyleft. Anyone who ships a binary derived from your GPL
> code must also ship the corresponding source.

---

## 4. The Corporate Civil Wars and the Bazaar (1991–1998)

### 4.1 The UNIX Copyright Wars

While Stallman was building the moral case, a separate legal crisis
was unfolding around **UNIX**. AT&T's Bell Labs had created UNIX in the
late 1960s, and the University of California, Berkeley had spent years
extending it into **BSD** (Berkeley Software Distribution). By the early
1990s, BSD was arguably better than the original AT&T code.

In 1992, **AT&T's Unix System Laboratories (USL)** sued **BSDi**
(Berkeley Software Design Inc.), claiming BSD contained AT&T trade
secrets and proprietary code. The lawsuit was a fog machine. Nobody
could be sure which parts of BSD were legally clean. Corporate adopters
froze. The suit chilled open-source UNIX development for years — years
during which an alternative quietly took over.

### 4.2 Linus's Accidental Revolution

In August 1991, a Finnish computer science student named **Linus
Torvalds** posted to the comp.os.minix Usenet newsgroup:

> *"I'm doing a (free) operating system (just a hobby, won't be big*
> *and professional like gnu) for 386(486) AT clones."*

Linux was not intended to be a world-historical event. It was a hobby
project. Torvalds chose the **GPLv2** for the kernel — not because he
was an ideological Stallmanite, but because he wanted contributions to
flow back. The GPL solved his engineering problem.

What happened next is described by Eric Raymond in
*The Cathedral and the Bazaar* (1999):

- **The Cathedral**: traditional closed development. A small group
  of wizards labours in secret, releasing polished versions
  infrequently. Think Windows NT.
- **The Bazaar**: Linux's model. Release early. Release often. Treat
  users as co-developers. Every user is a potential debugger.

Raymond's key insight, now called **Linus's Law**:

> *"Given enough eyeballs, all bugs are shallow."*

With thousands of developers reading the source, security holes get
spotted faster than any internal QA team could manage. The Bazaar
out-competes the Cathedral not through ideology but through **parallel
eyeballs**.

### 4.3 The Great Rebranding: "Open Source" (1998)

By the late 1990s, "Free Software" had a marketing problem. "Free"
meant "no money" to most businesspeople. At a strategy session in
February 1998, following Netscape's announcement that it would open-
source its browser, the term **"Open Source"** was coined (credited
to Christine Peterson of the Foresight Institute).

The **Open Source Initiative (OSI)** was founded to certify licences
and promote open source on *pragmatic* grounds — quality, reliability,
flexibility — rather than Stallman's moral grounds. This split the
movement philosophically but accelerated corporate adoption enormously.

> [!TIP]
> **Developer choice:** Understand the difference between "Free
> Software" (FSF/GPL: a moral stance — users must have the four
> freedoms) and "Open Source" (OSI: a pragmatic stance — open
> development produces better software). They overlap heavily but
> diverge at the edges. The FSF will not certify Apache 2.0 as "Free
> Software"; the OSI does. Know which community your project lives in.

---

## 5. Wall Street Validates the Commons (1999)

The sceptics said: you cannot build a business on giving code away.

On **August 11, 1999**, Red Hat went public on the NYSE. The stock
opened at $14 and closed near $52 — a gain of roughly 270% on day one,
one of the largest first-day gains in exchange history at the time.

Red Hat's model was simple: give away the Linux distribution (the code),
sell the support, certification, and integration (the service). The
value is not in the bits; it is in the **trust and expertise** around
the bits.

The IPO sent an unmistakable signal:

1. The "no warranty, no liability" open-source model was not a
   charity; it was a viable, scalable business.
2. You could be a major enterprise software player without a
   proprietary codebase.
3. The GPL was not a threat to business; it was a foundation for it.

Within two years, IBM announced it was investing $1 billion in Linux.
The corporate civil wars were over. Open source had won.

---

## 6. Creative Commons: Lessig Extends the Logic (2001)

If the GPL solved the problem for code, what about everything else —
writing, music, photography, film, academic papers?

**Lawrence Lessig**, a Stanford law professor, observed that the same
dynamics Stallman identified in software were happening across all
digital culture. Copyright terms had been extended repeatedly (the
"Sonny Bono Copyright Term Extension Act" of 1998, nicknamed by critics
the "Mickey Mouse Protection Act," extended terms to life plus 70
years). The default was "all rights reserved," which meant almost
nothing on the internet could be legally remixed.

In 2001 Lessig co-founded **Creative Commons (CC)**, offering a
spectrum of standardised licences from "attribution only" (CC-BY) to
"non-commercial, no derivatives" (CC-BY-NC-ND). The key insight was
the same as Stallman's: use copyright law to *define the terms of
sharing* rather than to prohibit it.

### Why This Matters for AI

Almost every major AI training dataset — Common Crawl, the Pile,
LAION-5B — contains CC-licensed material. Which CC licence is on that
material turns out to matter enormously for whether training constitutes
fair use, and whether the outputs are commercially exploitable. We
return to this in Section 9.

> [!TIP]
> **Developer choice:** When publishing research data, documentation,
> or datasets your lab produces, choose a CC licence explicitly. The
> default ("all rights reserved") creates ambiguity for every
> downstream user. **CC-BY 4.0** is the norm for academic outputs.
> Add **-NC** if you do not want commercial use. Add **-SA**
> (ShareAlike — the copyleft of the content world) if you want
> derivatives to stay open.

---

## 7. The Backpacking Doctrine: SQLite vs. the Oracle Trap

### 7.1 What Is SQLite?

**SQLite** is the most widely deployed database engine in the world.
It runs on every Android device, every iOS device, every Chrome,
Firefox, and Safari browser, most Linux distributions, and — famously
— the Mars rovers. It was written almost entirely by one person:
**D. Richard Hipp**. It ships as a single `.c` file and a single `.h`
file. That is a deliberate philosophical choice.

### 7.2 The Oracle Trap

Early in SQLite's development, Hipp considered using **Berkeley DB**
(BDB) as a storage backend. BDB was open source, mature, and widely
used. Then **Oracle acquired Sleepycat Software** (the BDB vendor) in
2006 and changed the licensing terms: commercial users of BDB now
needed to pay Oracle fees, or ship their entire application as open
source under the AGPL.

Any project that had taken a BDB dependency woke up one morning to
find Oracle standing between them and their production database.
Hipp had already moved away from BDB before the acquisition — he had
written his own B-tree implementation specifically to avoid this kind
of dependency risk. His instinct was right.

### 7.3 Backpacking

Hipp calls his approach **"backpacking"** — cutting the codebase back
to only what is most useful, eliminating external dependencies, and
owning the full stack for anything critical.

> *"If you want to be free, that means doing things yourself."*
> — Richard Hipp

Hipp built his own version control system (Fossil), his own text
editor, his own storage engine, and his own documentation system.
This is not the right approach for every project. But for a component
that will be embedded in billions of devices and must remain free
in perpetuity, it was the only approach that guaranteed freedom from
third-party licence changes.

### 7.4 The Broadcom/VMware Lesson (2023–2024)

The Oracle/BDB story is not ancient history. In 2023, **Broadcom
acquired VMware** and immediately restructured licensing, ending
perpetual licences and forcing customers into expensive subscriptions.
Organisations that had embedded VMware deeply had no escape route.
The lesson of the Oracle Trap was re-learned by an entire generation
of DevOps engineers.

> [!TIP]
> **Developer choice — the Backpacking Audit:**
> Before adding a dependency, ask three questions:
>
> 1. Is this on a **critical path** — would my product break
>    without it?
> 2. Does a **single corporation** control the licence — one that
>    could change terms unilaterally (Oracle, Broadcom, HashiCorp,
>    Redis Labs)?
> 3. Is the dependency **small enough to rewrite** in a week if
>    needed?
>
> If the answer to all three is yes: write it yourself. The short-
> term cost is far lower than a future licensing ransom.

---

## 8. Martínez: The 97% Reality and Supply Chain Risk

### 8.1 The Great Inversion of Development

Martínez & Durán (2021) studied modern software supply chains in the
context of the SolarWinds attack and reached a headline finding:

> *Modern software is assembled from pre-made parts where 85–97% of*
> *code is reused from external sources.*

If you write a Django web app, a React front end, or a PyTorch model,
the overwhelming majority of the code executing in production was
written by strangers. You are not primarily an author; you are a
**curator and integrator**. This is the Great Inversion Gates could
not have imagined in 1976: the "professional work for nothing" he
feared would never get done is now the foundation of every commercial
software product on earth.

### 8.2 The SolarWinds Attack (2020)

Attackers (later attributed to Russian intelligence) compromised the
**build pipeline** of SolarWinds' Orion network monitoring software.
They inserted malicious code into a software update that was then
cryptographically signed and distributed to roughly 18,000
organisations, including the US Treasury, the Pentagon, and Fortune
500 companies.

The victims did nothing wrong. They applied a signed update from a
trusted vendor. The attack surface was the **supply chain** — the 97%.

When you take a dependency, you inherit not just that package's bugs,
but also its dependencies' bugs (transitive dependencies), its build
pipeline's security posture, and its vendor's future licensing
decisions.

### 8.3 The XZ Utils Attack (2024)

More surgically: a threat actor spent **two years** building a
reputation as a contributor to **xz-utils**, a compression library
present in almost every Linux distribution. They then inserted a
backdoor into the build system shortly before a planned stable
release. The attack was caught by accident — a Microsoft engineer
noticed slightly elevated SSH daemon CPU usage on a test machine.

The attacker did not exploit a code bug. They exploited **trust** —
the assumption that a long-standing contributor's commits are safe.
Given enough time and patience, a single motivated attacker can
become a trusted maintainer of a critical open-source project.

> [!TIP]
> **Developer choice — the SBOM:** A **Software Bill of Materials**
> (SBOM) is a machine-readable inventory of every component in your
> software and its provenance. Generate one automatically in CI/CD
> using `syft` or `cyclonedx-bom`. An SBOM lets you answer "am I
> affected by CVE-XXXX-YYYY?" in seconds rather than days. As of
> September 2026, the EU Cyber Resilience Act makes SBOMs a legal
> requirement for commercial products sold in the EU.

> [!TIP]
> **Developer choice — the 30-day rule:** Several organisations now
> block CI/CD deployment of any npm or PyPI package less than 30
> days old. Typosquatting (publishing `requets` instead of
> `requests`) and protestware attacks disproportionately target
> freshly published packages. Make package age a gate in your
> pipeline.

---

## 9. The AI Legal Frontier: Samuelson (2025)

*Based on: Pamela Samuelson, "Does Using In-Copyright Works as*
*Training Data Infringe?", CACM Vol. 68 No. 11, November 2025.*

Pamela Samuelson is a professor at UC Berkeley and one of the
foremost authorities on digital copyright law. Her 2025 CACM article
is the clearest synthesis of the current legal landscape for AI
developers.

### 9.1 The Core Tension

AI companies trained large models on vast corpora that included
copyrighted books, code, articles, and art — often sourced from the
web, sometimes from datasets of dubious provenance (Books3, LibGen,
"shadow libraries"). Authors, artists, and publishers have filed
dozens of lawsuits.

The core allegation: **copying millions of copyrighted works to
create training datasets violates the reproduction right.**

The core defence: **training is transformative use, protected by
fair use.**

### 9.2 The Fair Use Framework

US copyright law (17 U.S.C. § 107) provides a fair use defence
evaluated on four factors:

| Factor | Question | AI Training Implication |
|--------|----------|------------------------|
| **1. Purpose** | Is the use transformative? | Training extracts patterns, not expression. Courts lean yes. |
| **2. Nature** | Factual or creative work? | Mostly creative — weighs against fair use. |
| **3. Amount** | How much was copied? | Entire works — weighs against fair use. |
| **4. Market effect** | Does it harm the original market? | The contested battleground. |

The AI companies' argument on Factor 1: training converts text into
**model weights** — statistical summaries of patterns. The original
expressive purpose (entertainment, information) differs entirely from
the training purpose (statistical generalisation). This echoes
*Authors Guild v. Google* (2015), where Google's digitisation of
entire books to build a search index was held transformative.

### 9.3 The Two Pivotal Cases (2025)

**Bartz v. Anthropic (Judge Alsup, June 2025)**

Training use: potentially fair (transformative). But: Anthropic's
dataset storage — **downloading and archiving** pirated books — was
found to be a separate act of infringement, not covered by the
transformative training defence.

*SE implication:* **architecture matters**. Streaming training data
through a pipeline and discarding it is legally distinct from
building a permanent database of copyrighted works. If you store it,
you own the liability for the storage, regardless of what you do
with it downstream.

**Kadrey v. Meta (Judge Chhabria, June 2025)**

Training defence largely succeeded. But: the judge issued a warning
about **market dilution** — if a system can generate "thousands of
romance novels per day," it may harm the market for human-authored
romance novels even if no individual output copies any specific novel.

*SE implication:* **output volume is a legal variable**. Rate limits
and usage controls are not just product decisions; they are legal
defences against a novel theory of copyright harm.

### 9.4 The Warhol Problem

The Supreme Court's 2023 decision in *Andy Warhol Foundation v.
Goldsmith* complicates the "transformative" argument for AI outputs.
The Court held that Warhol's silkscreen of Lynn Goldsmith's photograph
of Prince was **not** transformative when licensed commercially for
magazine covers, because it served the **same market purpose** as
Goldsmith's original photo licence.

The implication for AI: the test is not "does the output look the
same as training data?" but "does it **substitute for the original
in the same market**?" An AI portrait generator that competes
directly with portrait photographers is riskier than a code
completion tool that competes with no obvious human labour market.

### 9.5 The Shadow Library Problem

Several major training datasets were assembled from pirated sources.
Judge Alsup suggested that using pirated source material does not
automatically destroy a fair use defence if the training use is
transformative — but Judge Chhabria was more sceptical. The legal
picture is not settled.

The practical risk extends beyond litigation: if your training corpus
was sourced from a shadow library, any future licensing deal,
acquisition, or regulatory audit will surface it.

### 9.6 Market Dilution: The Novel Theory

The most significant new legal theory from the 2025 rulings is
**market dilution**. Traditional copyright asks: "does the output
copy the input?" The dilution theory asks: "does the *scale* of AI
output flood the market for human-created work, reducing its economic
value even without copying any specific work?"

This is legally uncharted. If it survives appeal, it has implications
for any AI product designed for high-volume content generation — even
if every individual output would independently pass a copyright test.

> [!TIP]
> **Developer choice — training data provenance:** Treat your
> training corpus like financial records. Document:
> - Where every dataset came from
> - Its licence at time of acquisition
> - Whether it was streamed or stored
> - What filtering was applied
>
> If you cannot answer these questions in a legal deposition, you
> are exposed. Tools like `croissant` metadata format and dataset
> datasheets help. The cost of documentation is orders of magnitude
> less than the cost of discovery in litigation.

> [!TIP]
> **Developer choice — output architecture:**
> Systems that *analyse* have stronger fair use protection than
> systems that *reproduce*. Concretely:
>
> - **Safer:** ephemeral training (process and discard source),
>   output filters detecting verbatim reproduction, rate limits
>   on generation volume
> - **Riskier:** RAG systems that retrieve and display copyrighted
>   originals, persistent databases of copyrighted works, bulk
>   generation APIs with no volume controls
>
> Document your transformative architecture in design docs — it
> is legal evidence, not just engineering record.

---

## 10. The EU Cyber Resilience Act (CRA, 2024–2026)

The legal environment around software liability is not only moving
in courts — it is moving in legislatures. The EU's **Cyber Resilience
Act** (adopted October 2024, enforcement phasing through 2026–2027)
is the most significant regulatory shift for software engineers
since GDPR.

Key provisions:

- **Mandatory security requirements** throughout a product's lifecycle
  for any product with "digital elements" sold in the EU.
- **Vulnerability reporting:** actively exploited vulnerabilities must
  be reported to ENISA (the EU cybersecurity agency) within **24
  hours** of discovery.
- **End of "as-is" disclaimers:** the open-source tradition of
  shipping software with "no warranty" disclaimers does not protect
  commercial distributors. If you make money from it in the EU, you
  are a **"software steward"** with legal obligations.
- **SBOM requirement:** products must ship with a Software Bill of
  Materials documenting every component.

The CRA specifically carves out **non-commercial open-source**
projects from its requirements — but the moment a company packages
and sells that open-source code, the company acquires the obligations.
The "I just glued together some npm packages" defence is gone.

> [!TIP]
> **Developer choice — CRA compliance checklist:**
> 1. Generate and publish an SBOM (`syft`, `cyclonedx-bom`)
> 2. Run automated CVE scanning in CI/CD (`grype`, `trivy`)
> 3. Add a `SECURITY.md` to every public repo — a minimal
>    vulnerability disclosure policy costs ten minutes to write
> 4. Know which jurisdictions your product ships to — CRA covers
>    the EU market; the US NIST SSDF and Australia's SOCI Act
>    have their own requirements
> 5. If you maintain a widely-used OSS library, check whether
>    it qualifies as a CRA "important product" — the bar for
>    obligations is stricter for high-criticality components

---

## 11. Licence Choices: A Practical Field Guide

All of the above history converges on a question every developer
faces at some point: **what licence do I put on this?**

### 11.1 The Main Families

| Family | Canonical Licence | Key Property |
|--------|------------------|--------------|
| Permissive | MIT | Do anything, keep attribution |
| Permissive + Patent | Apache 2.0 | MIT plus explicit patent grant |
| Weak copyleft | LGPL 2.1 | Library stays open; app need not |
| Strong copyleft | GPL v3 | All derivatives must be GPL |
| Network copyleft | AGPL v3 | GPL plus SaaS loophole closed |
| Source-available | BUSL / Commons Clause | Not open source; timed commercial restriction |

### 11.2 Patent Grants and Why They Matter

The MIT licence says nothing about patents. This silence is meaningful.
A company could release code under MIT, let you build a product on it,
wait until your product is profitable, and then sue you for patent
infringement on the algorithms in that code. This is the playbook of
patent assertion entities (PAEs, colloquially "patent trolls").

**Apache 2.0** includes an explicit patent grant: every contributor
grants you a licence to any patents they hold that are necessarily
infringed by the code. If they later sue you for patent infringement,
their Apache 2.0 licence rights are automatically terminated. This
makes Apache 2.0 the **Linux Foundation's preferred licence** for
infrastructure projects: it lowers legal risk for corporate
contributors and blocks the PAE playbook.

> [!TIP]
> **Developer choice — the licence decision tree:**
>
> - Want **maximum adoption** (corporate, startup, academic)?
>   → **Apache 2.0**. Patent grant included. Companies can use
>   it without open-sourcing their product.
>
> - Building a **library** you want widely used but want to
>   prevent proprietary forks of the library itself?
>   → **LGPL v2.1 or v3**. The library must stay open; the
>   application linking to it need not be.
>
> - Want **full copyleft** — all derivatives must give back?
>   → **GPL v3**. Strong reciprocity. Corporates will hesitate
>   to contribute; community projects thrive.
>
> - Building a **server-side tool** and worried about the SaaS
>   loophole (companies running GPL code as a service without
>   ever distributing a binary)?
>   → **AGPL v3**. Network use triggers the copyleft obligation.
>   Note: many companies explicitly ban AGPL in their dependency
>   policies — it will limit corporate adoption.
>
> - Tempted by BUSL, Commons Clause, or "source-available"?
>   → Understand that these are **not open source**. They will
>   generate community backlash (HashiCorp/Terraform 2023,
>   Redis 2024, Elasticsearch 2021) and are not OSI-certified.
>   You will lose contributors and gain a fork.

### 11.3 Licence Compatibility Traps

You cannot combine GPL v2 code and GPL v3 code in one binary — the
licences are incompatible. (The Linux kernel is GPLv2-only; Torvalds
refuses to upgrade, partly due to GPLv3's anti-tivoization clause.)
Before combining dependencies, check compatibility at
[choosealicense.com](https://choosealicense.com) or the
[SPDX licence list](https://spdx.org/licenses/).

> [!TIP]
> **Developer choice — licence auditing in CI:** Tools like
> `liccheck` (Python), `license-checker` (npm), and `pip-licenses`
> will scan your full dependency tree and flag problematic licences
> automatically. Run this check in CI/CD. A single AGPL transitive
> dependency in a commercial product can be a contractual violation.
> Find it before your customer's legal team does.

---

## 12. Putting It All Together

### 12.1 A Summary of the Inversion

| Era | Dominant model | Developer role | Key risk |
|-----|----------------|----------------|----------|
| 1976 (Gates) | Software as property | Author | Piracy |
| 1983 (Stallman) | Software as freedom | Crusader | Enclosure |
| 1991 (Torvalds) | Software as community | Contributor | Fragmentation |
| 1999 (Red Hat) | Software as service | Builder | Commoditisation |
| 2021 (Martínez) | Software as assembly | Integrator | Supply chain attack |
| 2025 (Samuelson) | Software as trained model | Curator | Copyright liability |
| 2026 (CRA) | Software as product liability | Steward | Regulatory violation |

### 12.2 The Vibe Coding Trap

Since 2024, "vibe coding" — accepting AI-generated code with minimal
review — has become a real pattern in production engineering. The
legal and security implications are severe:

- AI-generated code may incorporate patterns from GPL'd training data.
  If your product ships that code, you may be in licence violation
  without knowing it.
- AI agents that `npm install` or `pip install` autonomously may pull
  in packages with incompatible licences or known CVEs.
- The person who commits the code is legally the author. "The AI
  wrote it" is not a defence in a GPL compliance dispute.

> [!TIP]
> **Developer choice — AI-assisted development compliance:**
> 1. Run licence audits on every substantial AI-generated file
>    before commit.
> 2. Treat AI-generated dependency suggestions identically to
>    human ones: check the licence, check the CVE database,
>    check the package age.
> 3. If your team uses an AI coding agent with autonomous tool
>    use, add licence and SBOM gates to its allowed actions.
> 4. Document which parts of your codebase were AI-assisted.
>    This is both a legal record and an engineering hygiene
>    practice.

---

## Summary: Five Things to Do

1. **Audit your dependencies' licences** with `pip-licenses` or
   `license-checker`. Fix any AGPL or GPL violations in commercial
   code before your next release.

2. **Generate an SBOM** for your main project using `syft` or
   `cyclonedx-bom`. Add SBOM generation to your CI pipeline as
   a non-optional step.

3. **Check your training data provenance** if you are building ML
   systems. Document the licence of every dataset. Prefer CC-BY
   or permissively-licensed corpora. If you used a shadow library,
   decide now how you will handle that disclosure.

4. **Add a `SECURITY.md`** to every public repo: a simple
   vulnerability disclosure policy. This is table stakes for CRA
   compliance and costs ten minutes.

5. **Apply the Backpacking Audit** to your three most critical
   external dependencies. For each: who controls the licence?
   Could they change terms unilaterally? What would replacement
   cost? Conclude with a keep / replace / monitor decision.

---

## Key References

- Martínez, J. & Durán, J.M. (2021). Software Supply Chain Attacks,
  a Threat to Global Cybersecurity: SolarWinds' Case Study.
  *International Journal of Safety and Security Engineering*, 11(5),
  537–545. https://doi.org/10.18280/ijsse.110505

- Samuelson, P. (2025). Does Using In-Copyright Works as Training
  Data Infringe? *Communications of the ACM*, 68(11).
  https://cacm.acm.org/opinion/does-using-in-copyright-works-as-training-data-infringe/

- Raymond, E.S. (1999). *The Cathedral and the Bazaar*.
  http://www.catb.org/~esr/writings/cathedral-bazaar/

- Gates, B. (1976). Open Letter to Hobbyists.
  https://en.wikipedia.org/wiki/Open_Letter_to_Hobbyists

- GNU Manifesto (1985). https://www.gnu.org/gnu/manifesto.html

- OSI Approved Licences. https://opensource.org/licenses/

- SPDX Licence List. https://spdx.org/licenses/

- EU Cyber Resilience Act (2024).
  https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act

---

## Review Questions

### Simple Questions

1. What is the difference between "Free Software" (FSF) and "Open
   Source" (OSI)? Give one practical consequence of the distinction.

2. Name Stallman's Four Freedoms. Why is Freedom 0 numbered zero?

3. What is "copyleft"? How does the GPL use copyright law to
   guarantee openness rather than restrict it?

4. What is a Software Bill of Materials (SBOM)? Name one tool that
   generates one and one legal framework that now requires one.

5. In Bartz v. Anthropic (2025), what was the architectural
   distinction the court drew between "training use" and "database
   storage"? What is the SE implication?

### Harder

6. A startup wants to build a commercial product on top of a GPL v3
   library. The CTO says: "It's fine, GPL is just about sharing
   source." Evaluate this claim. What are the actual obligations,
   what are the business risks, and what licence choices would you
   recommend instead?

7. Apply the Backpacking Audit to a real dependency in a project
   you have worked on. Is it on the critical path? Who controls
   the licence? What would replacement cost? Deliver a justified
   keep / replace / monitor verdict.

8. You are designing a data pipeline for a new LLM to be trained
   on publicly available web data and academic papers. Using
   Samuelson's four fair use factors and the architectural lessons
   of Bartz and Kadrey, design the pipeline to maximise your fair
   use defence. Identify two remaining legal risks you cannot
   engineer away.

9. Your company's AI coding agent autonomously runs `pip install`
   and commits generated code to production branches. Using the
   frameworks in this lecture — supply chain security, licence
   compliance, CRA obligations — design a policy and technical
   gate system that reduces risk without eliminating the
   productivity benefit of the agent.

10. "The Great Inversion" describes the shift from software as
    property (Gates, 1976) to software as assembly (Martínez,
    2021). Argue that this inversion makes the Four Freedoms
    *more* important today than in 1983, not less. Ground your
    argument in at least two concrete examples from this lecture.
