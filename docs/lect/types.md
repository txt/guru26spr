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

# Some Javascript Examples

Note:

- not the sort of JS seen in job interview questions
  - no class, prototypes, etc
- pure functional programming in JS is limited by lack of  tail call optimization
- JS has some wonderful funnies. Like `x == y` does first tries type conversion  to same type.
  - `x === y` checks types and values without any conversions.

BTW, this code is all `sync`; i.e. no asynchronous  interlevering of reads threads

```js
// old school JS node example with call back
import fs from "fs"

fs.readFile("data.txt", "utf8",
  (err, s) => err ? die(err) : out(s))

// another eg.
// note the call back function, run when read happens `r ==> r.text()`
const txt = await fetch("data.txt").then(r => r.text())

// chatgpt recommends a slightly different style:
const r   = await fetch("data.txt")
const txt = await r.text()
```
The following code using `readFileSync` i.e. no `async`.


```js
#!/usr/bin/env node
// ez.js: easy AI tools
// (c) 2025 Tim Menzies, MIT license
//
// Options:
//    -b bins=5    Number of bins
//    -B Budget=50 Initial sampling budget
//    -C Check=5   final evaluation budget
//    -l leaf=2    Min examples in leaf of tree
//    -p p=2       Distance coefficient
//    -s seed=1    Random number seed
//    -S Show=30   Tree display width

let fs = require("fs")
let BIG = 1e32, the = {}

//--- random (seedable) -------------------------------------------------------
let _seed = 1
let srand = (n) => { _seed = n }
let rand  = () => { _seed = (16807*_seed) % 2147483647
                     return _seed / 2147483647 }

let shuffle = (a) => {
  for (let i = a.length-1; i > 0; i--) {
    let j = Math.floor(rand() * (i+1));
    [a[i], a[j]] = [a[j], a[i]] }
  return a }

let gauss = (mu,sd1) => mu + 2*sd1*(rand()+rand()+rand() - 1.5)

let pick = (d, n) => {
  n *= rand()
  for (let k in d) if ((n -= d[k]) <= 0) return k }

//--- lib ---------------------------------------------------------------------
let clip   = (v,lo,hi) => Math.max(lo, Math.min(hi, v))
let log2   = (n) => Math.log(n) / Math.log(2)
let sorted = (a, f) => [...a].sort((x,y) => f(x) - f(y))

let cast = (s) => s==="true" ? true : s==="false" ? false
                  : isNaN(Number(s)) ? s : Number(s)

let csv = (f) =>
  fs.readFileSync(f,"utf8").trim().split("\n")
    .map(s => s.split(",").map(cast))

let o = (t) =>
  typeof t === "function"      ? (t.doc || "")
  : Array.isArray(t)           ? "["+t.map(o).join(", ")+"]"
  : typeof t === "number"      ? (t===Math.floor(t) ? ""+t : t.toFixed(2))
  : t && typeof t === "object" ? "{"+Object.keys(t)
                                    .map(k => `:${k} ${o(t[k])}`)
                                    .join(" ")+"}"
  : ""+t

//--- create ------------------------------------------------------------------
let NUM = (d={}) => ({it:"NUM", n:0, mu:0, m2:0, ...d})
let SYM = (d={}) => ({it:"SYM", n:0, has:{},     ...d})

let COL = (at=0, txt=" ") =>
  (txt[0] === txt[0].toUpperCase() ? NUM : SYM)(
    {at, txt, goal: txt.slice(-1) !== "-"})

let DATA = (items=[], s="") =>
  adds(items, {it:"DATA", txt:s, rows:[], cols:null})

let COLS = (names) => {
  let cols = names.map((s,n) => COL(n, s))
  return {it:"COLS", names, all:cols,
          x: cols.filter(c => !"-+!X".includes(c.txt.slice(-1))),
          y: cols.filter(c =>  "-+!".includes(c.txt.slice(-1))) }}

let clone = (data, rows=[]) => DATA([data.cols.names, ...rows])

//--- update ------------------------------------------------------------------
let adds = (items, it=NUM() ) => {
  for (let v of items) add(it, v)
  return it }

let add = (i, v) => {
  if (i.it === "DATA") {
    if (!i.cols) i.cols = COLS(v)
    else i.rows.push(i.cols.all.map(c => add(c, v[c.at])))
  } else if (v !== "?") {
    i.n += 1
    if (i.it === "SYM") i.has[v] = 1 + (i.has[v] || 0)
    if (i.it === "NUM") { let d = v-i.mu; i.mu += d/i.n
                          i.m2 += d*(v - i.mu) }
  }
  return v }
```
Aside: here is the above in standard JS

```js
class NUM {
  constructor(d = {}) {
    this.it = "NUM"
    this.n = 0
    this.mu = 0
    this.m2 = 0
    Object.assign(this, d)
  }
}

class SYM {
  constructor(d = {}) {
    this.it = "SYM"
    this.n = 0
    this.has = {}
    Object.assign(this, d)
  }
}

class COL {
  static create(at = 0, txt = " ") {
    let Cls = txt[0] === txt[0].toUpperCase() ? NUM : SYM
    return new Cls({ at, txt, goal: txt.slice(-1) !== "-" })
  }
}

class COLS {
  constructor(names) {
    this.it = "COLS"
    this.names = names
    this.all = names.map((s, n) => COL.create(n, s))
    this.x = this.all.filter(c => !"-+!X".includes(c.txt.slice(-1)))
    this.y = this.all.filter(c => "-+!".includes(c.txt.slice(-1)))
  }
}

class DATA {
  constructor(items = [], s = "") {
    this.it = "DATA"
    this.txt = s
    this.rows = []
    this.cols = null
    adds(items, this)
  }

  clone(rows = []) {
    return new DATA([this.cols.names, ...rows])
  }
}

//--- update ------------------------------------------------------------------
function adds(items, it) {
  it = it || new NUM()
  for (let v of items) add(it, v)
  return it
}

function add(i, v) {
  if (i instanceof DATA) {
    if (!i.cols) i.cols = new COLS(v)
    else i.rows.push(i.cols.all.map(c => add(c, v[c.at])))
  } else if (v !== "?") {
    i.n += 1
    if (i instanceof SYM) i.has[v] = 1 + (i.has[v] || 0)
    if (i instanceof NUM) {
      let d = v - i.mu
      i.mu += d / i.n
      i.m2 += d * (v - i.mu)
    }
  }
  return v
}
```

Note the tradeoffs:

- instanceof instead of i.it === "NUM" (or keep the .it checks, both work)
- COL is awkward—factory pattern via static method since it returns different types
- More verbose, more ceremony, same behavior

Anyway back to JS, backpacking style (no classes, no prototypes).


```js
//--- query -------------------------------------------------------------------
let score = (num) =>
  num.n < the.leaf ? BIG
                   : num.mu + sd(num)/(Math.sqrt(num.n) + 1/BIG)

let mids = (data) => data.cols.all.map(mid)
let mid  = (col) => col.it === "SYM" ? mode(col) : col.mu
let mode = (sym) => Object.keys(sym.has)
                      .reduce((a,b) => sym.has[a]>=sym.has[b] ? a : b)

let spread = (col) => col.it === "SYM" ? ent(col) : sd(col)
let sd  = (num) => num.n<2 ? 0 : Math.sqrt(num.m2/(num.n-1))

let ent = (sym) => {
  let out = 0
  for (let k in sym.has) {
    let p = sym.has[k]/sym.n; if (p > 0) out -= p*log2(p) }
  return out }

let z      = (num,v) => (v - num.mu) / (sd(num) + 1/BIG)
let norm   = (num,v) => 1 / (1 + Math.exp(-1.7 * v))
let bucket = (num,v) =>
  Math.floor(the.bins * norm(num, clip(z(num,v), -3, 3)))

//--- distance ----------------------------------------------------------------
let minkowski = (items) => {
  let n=0, d=0
  for (let x of items) { n++; d += x ** the.p }
  return n === 0 ? 0 : (d/n) ** (1/the.p) }

let disty = (data, row) =>
  minkowski(data.cols.y.map(y => norm(y, row[y.at]) - y.goal))

let distx = (data, r1, r2) =>
  minkowski(data.cols.x.map(x => aha(x, r1[x.at], r2[x.at])))
```

Digression: This JS does TWO list of the comparison attribute lists but
Python can do it in ONE.

```python
def minkowski(a, p=2):
    n = d = 0
    for x in a:
        d += x**p
        n += 1
    return (d/n) ** (1/p)

def disty(data, row): 
  return minkowski(norm(y, row[y.at]) - y.goal for y in data.cols.y)

def distx(data, r1, r2): 
  return minkowski(aha(x, r1[x.at], r2[x.at]) for x in data.cols.x)
```

```js
let aha = (col, u, v) => {
  if (u === "?" && v === "?") return 1
  if (col.it === "SYM")      return u !== v ? 1 : 0
  u = norm(col,u); v = norm(col,v)
  if (u === "?") u = v > 0.5 ? 0 : 1
  if (v === "?") v = u > 0.5 ? 0 : 1
  return Math.abs(u - v) }

let furthest = (data,row,rows) => around(data,row,rows).slice(-1)[0]
let nearest  = (data,row,rows) => around(data,row,rows)[0]
let around = (data,row,rows) => sorted(rows, r => distx(data,row,r))

//--- cli ---------------------------------------------------------------------
let run = (f, ...a) => {
  srand(the.seed)
  try { f(...a) } catch(e) { console.error(e.stack) } }

let egs = {
  h: {doc:"Show help.", f:() => {
    console.log("ez.js: easy AI tools\n\nOptions:")
    for (let k in the) console.log(`   -${k} ${k}=${the[k]}`)
    console.log("\nActions:")
    for (let k in egs)
      console.log(`   -${k.padEnd(12)} ${egs[k].doc}`) }},

  _the: {doc:"Show config.", f:() => console.log(o(the)) },

  s: {doc:"Set seed.", a:[Number], f:(n) => {
    the.seed = n; srand(n) }},

  _csvs: {doc:"csv reader.", a:["file"], f:(f) =>
    csv(f).filter((_,i) => i%40===0)
           .forEach(r => console.log(o(r))) },

  _syms: {doc:"SYMs summary.", f:() => {
    let syms = adds("aaaabbc", SYM()), x = ent(syms)
    console.log(o(x))
    console.assert(Math.abs(1.379 - x) < 0.05) }},

  _nums: {doc:"NUMs summary.", f:() => {
    let nums = NUM()
    for (let i=0; i<1000; i++) add(nums, gauss(10, 1))
    console.log(o({mu: nums.mu, sd: sd(nums)}))
    console.assert(Math.abs(10 - nums.mu) < 0.05)
    console.assert(Math.abs(1 - sd(nums)) < 0.05) }},

  _ys: {doc:"Show ys.", a:["file"], f:(f) => {
    let data = DATA(csv(f))
    console.log(data.cols.names.join(" "))
    console.log(o(mids(data)))
    sorted(data.rows, r => disty(data,r))
      .filter((_,i) => i%40===0)
      .forEach(row => {
        let bs = data.cols.y.map(c => bucket(c, row[c.at]))
        console.log(...row,...bs,disty(data,row).toFixed(2))
      }) }},

  _tree: {doc:"Show tree.", a:["file"], f:(f) => {
    let data  = DATA(csv(f))
    let data1 = clone(data, shuffle(data.rows).slice(0,50))
    let [tree] = Tree(data1)
    treeShow(tree) }},

  _test: {doc:"Run tests.", a:["file"], f:(f) => {
    let data = DATA(csv(f))
    let half = Math.floor(data.rows.length / 2)
    let Y   = r => disty(data, r)
    let b4  = sorted(data.rows, Y).map(Y)
    let win = r => Math.floor(
      100*(1 - (Y(r)-b4[0]) / (b4[half]-b4[0]+1/BIG)))
    let wins = NUM()
    for (let i=0; i<60; i++) {
      let rows  = shuffle(data.rows)
      let train = rows.slice(0,half).slice(0, the.Budget)
      let test  = rows.slice(half)
      let [tree] = Tree(clone(data, train))
      test.sort((a,b) =>
        treeLeaf(tree,a).y.mu - treeLeaf(tree,b).y.mu)
      add(wins, win(test.slice(0,the.Check)
                        .reduce((a,b) => Y(a)<Y(b)?a:b))) }
    console.log(
      [Math.round(wins.mu),"sd",Math.round(sd(wins)),
       "b4",o(b4[half]),"lo",o(b4[0]),
       "x",data.cols.x.length,"y",data.cols.y.length,
       "r",data.rows.length,
       ...f.split("/").slice(-2)].join(" ,")) }} }

//--- boot --------------------------------------------------------------------
let doc = fs.readFileSync(__filename, "utf8")
for (let m of doc.matchAll(/(\S+)=(\S+)/g))
  if (m.index < 500) the[m[1]] = cast(m[2])
srand(the.seed)

let args = process.argv.slice(2), i = 0
while (i < args.length) {
  let key = args[i].slice(1).replace(/-/g, "_")
  let eg  = egs[key]
  if (eg) {
    let fa = (eg.a||[]).map(t => t==="file" ? args[++i]
                                            : t(args[++i]))
    run(eg.f, ...fa)
  } else if (key in the) { the[key] = cast(args[++i] || "") }
  i++ }
```

## Typescript

What are types? 

- Things we can reason about at load **OR** runtime


e.g. Parse Tree

`2 + pi * r`

```
        +
       / \
      2   *
         / \
       pi   r
       |
     3.14
```

Type Propagation (↑ bottom-up)

```
        +  ← float        float bubbles up
       / \
      2   *  ← float
    int  / \
       pi   r
     float int
```

Type Error (caught at compile time via type propagation)
BTW: compilation can stop here (never generates bad code).

`2 + "hello"`

```
        +  ← ERROR: int + str
       / \
      2  "hello"
     int  str
```


Useful Rewrites

- **Inlining:**       `let pi=3.14 in pi*r`  →  `3.14 * r`
- **Dead code:**      `let pi=3.14 in r*r`   →  `r * r`
- **Desugaring:**     `r ** 2`               →  `r * r`
- **Constant fold:**  `3.14 * 2`             →  `6.28`

Compilation (↑ emit on way up)

```
    *
   / \              →     [PUSH 3.14, LOAD r, MUL]
 3.14  r
```

So types let us reason up,down,over across

| Direction | Name | Flow | Examples |
|-----------|------|------|----------|
| ↑ | synthesized | children → parent | types, code |
| ↓ | inherited | parent → children | env |
| → | rewrite | old tree → new | fold, inline, desugar |
| ✗ | type check | reject bad trees | before codegen |

So, formally, what are "types"?
Two views:

**Interface View:** Types are contracts
- "This value supports these operations"
- Duck typing: discovered at runtime ("if it quacks...")
- Static typing: proven at compile time

**Inference View:** Types are equations
- Compiler solves constraints
- Flows through the parse tree (like our examples!)

Type Inference (constraint propagation):

```
a = 1        →  a is int (known)
b = a + ?    →  ? must be int (forced)
c = b + 0.5  →  c is float (propagates)
```

Compiler fills in what it can prove. Error if contradicts.

In Summary:

| | Dynamic | Static |
|---|---------|--------|
| **Errors** | User finds them | Compiler finds them |
| **Speed** | Boxing, runtime checks | Raw machine code |
| **Proof** | Tests (some cases) | Types (all cases) |
| **Docs** | README | Code is the doc |

Compiler Optimizations (enabled by types)

- **Monomorphization:** `List<int>` → specialized int code, not generic pointers
- **Devirtualization:** known type → inline the function, skip vtable lookup
- **Memory layout:** no boxing, pack structs tight, use stack not heap


> Types let the compiler do at compile time what would otherwise happen at runtime.


```typescript
#!/usr/bin/env ts-node
import fs from "fs"

// -b bins=5 -B budget=50 -C check=5 -l leaf=2 -p p=2 -s seed=1 -S show=30
type V = string | number | boolean
type Row = V[]
interface Col { it:"NUM"|"SYM"; n:number; at:number; txt:string; goal:number;
                mu:number; m2:number; has:Record<string, number> }
interface DATA { rows:Row[]; cols:{all:Col[], x:Col[], y:Col[], names:string[]} }

const the: any = {}, BIG = 1e32, egs: Record<string, any> = {}
let _seed = 1
const srand = (n:number) => _seed = n
const rand = () => (_seed = (16807 * _seed) % 2147483647) / 2147483647
const cast = (s:string): V => s=="true" || (s=="false" ? false : 
             isNaN(Number(s)) ? s : Number(s))

const col = (at:number, txt:string): Col => ({
  n:0, at, txt, it: /^[A-Z]/.test(txt) ? "NUM" : "SYM",
  goal: txt.endsWith("-") ? 0 : 1, mu:0, m2:0, has:{}
})

const add = (c:Col, v:V) => {
  if (v == "?") return v
  c.n++
  if (c.it == "NUM") {
    let d = (v as number) - c.mu
    c.mu += d / c.n
    c.m2 += d * ((v as number) - c.mu)
  } else c.has[v as string] = (c.has[v as string] || 0) + 1
  return v
}

const makeData = (rows: V[][] = []): DATA => {
  let d: DATA = { rows: [], cols: {all:[], x:[], y:[], names:[]} }
  rows.map((row, i) => {
    if (i == 0) {
      d.cols.names = row as string[]
      d.cols.all = d.cols.names.map((n, j) => col(j, n))
      const x = (s:string) => !"-+!X".includes(s.slice(-1))
      d.cols.x = d.cols.all.filter(c => x(c.txt))
      d.cols.y = d.cols.all.filter(c => !x(c.txt))
    } else d.rows.push(d.cols.all.map(c => add(c, row[c.at])))
  })
  return d
}

const sd = (c:Col) => c.n < 2 ? 0 : (c.m2 / (c.n - 1)) ** .5
const mid = (c:Col) => c.it=="SYM" ? 
  Object.keys(c.has).reduce((a,b) => c.has[a] > c.has[b] ? a : b) : c.mu
const norm = (c:Col, v:number) => 1 / (1 + Math.exp(-1.7 * ((v-c.mu)/(sd(c)+1/BIG))))

const csv = (f:string) => fs.readFileSync(f,"utf8").trim().split("\n")
                            .map(s => s.split(",").map(cast))

const o = (t:any): string => typeof t != "object" ? ""+t : 
  Array.isArray(t) ? "["+t.map(o).join(", ")+"]" :
  "{"+Object.keys(t).map(k => `:${k} ${o(t[k])}`).join(" ")+"}"

const dist = (d:DATA, r1:Row, r2:Row) => {
  let ds = d.cols.x.map(c => {
    let u = r1[c.at], v = r2[c.at]
    if (u=="?" && v=="?") return 1
    if (c.it == "SYM") return u != v ? 1 : 0
    let u1 = norm(c, u as number), v1 = norm(c, v as number)
    if (u=="?") u1 = v1 > .5 ? 0 : 1
    if (v=="?") v1 = u1 > .5 ? 0 : 1
    return Math.abs(u1 - v1)
  })
  return (ds.reduce((a,b) => a + b**the.p, 0) / ds.length) ** (1/the.p)
}

// Tests
egs.the = { doc:"Show config", f:() => console.log(o(the)) }
egs.sym = { doc:"SYM summary", f:() => {
  let s = col(0, "a")
  "aaaabbc".split("").map(x => add(s, x))
  console.log(mid(s))
}}
egs.num = { doc:"NUM summary", f:() => {
  let n = col(0, "A")
  for(let i=0; i<100; i++) add(n, i)
  console.log(n.mu, sd(n))
}}

// Boot
const src = fs.readFileSync(__filename, "utf8")
for (let m of src.matchAll(/(\S+)=(\S+)/g)) the[m[1]] = cast(m[2])
let args = process.argv.slice(2)
for (let i=0; i < args.length; i++) {
  let k = args[i].replace(/^-+/, ""), eg = egs[k]
  if (eg) { srand(the.seed); eg.f() }
  else if (the[k] !== undefined) the[k] = cast(args[++i])
}
```

Same code in RUST:

```rust
use std::collections::HashMap;
use std::fs;
use std::env;

const BIG: f64 = 1e32;

static mut SEED: u64 = 1;

fn srand(n: u64) { unsafe { SEED = n; } }
fn rand() -> f64 {
    unsafe {
        SEED = (16807 * SEED) % 2147483647;
        SEED as f64 / 2147483647.0
    }
}

#[derive(Clone, Debug)]
enum V {
    Str(String),
    Num(f64),
    Bool(bool),
}

impl V {
    fn as_num(&self) -> f64 {
        match self { V::Num(n) => *n, _ => 0.0 }
    }
    fn as_str(&self) -> &str {
        match self { V::Str(s) => s, _ => "" }
    }
    fn is_missing(&self) -> bool {
        matches!(self, V::Str(s) if s == "?")
    }
}

fn cast(s: &str) -> V {
    match s {
        "true" => V::Bool(true),
        "false" => V::Bool(false),
        _ => s.parse::<f64>().map(V::Num).unwrap_or_else(|_| V::Str(s.to_string()))
    }
}

#[derive(Clone, Debug)]
enum ColType { NUM, SYM }

#[derive(Clone, Debug)]
struct Col {
    it: ColType,
    n: usize,
    at: usize,
    txt: String,
    goal: f64,
    mu: f64,
    m2: f64,
    has: HashMap<String, usize>,
}

impl Col {
    fn new(at: usize, txt: &str) -> Self {
        Col {
            n: 0, at, txt: txt.to_string(),
            it: if txt.chars().next().map(|c| c.is_uppercase()).unwrap_or(false)
                { ColType::NUM } else { ColType::SYM },
            goal: if txt.ends_with("-") { 0.0 } else { 1.0 },
            mu: 0.0, m2: 0.0, has: HashMap::new(),
        }
    }

    fn add(&mut self, v: &V) -> V {
        if v.is_missing() { return v.clone(); }
        self.n += 1;
        match self.it {
            ColType::NUM => {
                let x = v.as_num();
                let d = x - self.mu;
                self.mu += d / self.n as f64;
                self.m2 += d * (x - self.mu);
            }
            ColType::SYM => {
                let k = v.as_str().to_string();
                *self.has.entry(k).or_insert(0) += 1;
            }
        }
        v.clone()
    }

    fn sd(&self) -> f64 {
        if self.n < 2 { 0.0 } else { (self.m2 / (self.n - 1) as f64).sqrt() }
    }

    fn mid(&self) -> V {
        match self.it {
            ColType::SYM => V::Str(self.has.iter()
                .max_by_key(|(_, v)| *v)
                .map(|(k, _)| k.clone())
                .unwrap_or_default()),
            ColType::NUM => V::Num(self.mu),
        }
    }

    fn norm(&self, v: f64) -> f64 {
        1.0 / (1.0 + (-1.7 * ((v - self.mu) / (self.sd() + 1.0/BIG))).exp())
    }
}

#[derive(Clone, Debug)]
struct Cols {
    all: Vec<Col>,
    x: Vec<usize>,
    y: Vec<usize>,
    names: Vec<String>,
}

#[derive(Clone, Debug)]
struct Data {
    rows: Vec<Vec<V>>,
    cols: Cols,
}

impl Data {
    fn new(rows: Vec<Vec<V>>) -> Self {
        let mut d = Data {
            rows: vec![],
            cols: Cols { all: vec![], x: vec![], y: vec![], names: vec![] },
        };
        for (i, row) in rows.iter().enumerate() {
            if i == 0 {
                d.cols.names = row.iter().map(|v| v.as_str().to_string()).collect();
                d.cols.all = d.cols.names.iter().enumerate()
                    .map(|(j, n)| Col::new(j, n)).collect();
                let is_x = |s: &str| !"-+!X".contains(s.chars().last().unwrap_or(' '));
                d.cols.x = d.cols.all.iter().enumerate()
                    .filter(|(_, c)| is_x(&c.txt)).map(|(i, _)| i).collect();
                d.cols.y = d.cols.all.iter().enumerate()
                    .filter(|(_, c)| !is_x(&c.txt)).map(|(i, _)| i).collect();
            } else {
                let new_row: Vec<V> = d.cols.all.iter_mut()
                    .map(|c| c.add(&row[c.at])).collect();
                d.rows.push(new_row);
            }
        }
        d
    }

    fn dist(&self, r1: &[V], r2: &[V], p: f64) -> f64 {
        let ds: Vec<f64> = self.cols.x.iter().map(|&i| {
            let c = &self.cols.all[i];
            let u = &r1[c.at];
            let v = &r2[c.at];
            if u.is_missing() && v.is_missing() { return 1.0; }
            match c.it {
                ColType::SYM => if u.as_str() != v.as_str() { 1.0 } else { 0.0 },
                ColType::NUM => {
                    let mut u1 = c.norm(u.as_num());
                    let mut v1 = c.norm(v.as_num());
                    if u.is_missing() { u1 = if v1 > 0.5 { 0.0 } else { 1.0 }; }
                    if v.is_missing() { v1 = if u1 > 0.5 { 0.0 } else { 1.0 }; }
                    (u1 - v1).abs()
                }
            }
        }).collect();
        (ds.iter().map(|d| d.powf(p)).sum::<f64>() / ds.len() as f64).powf(1.0/p)
    }
}

fn csv(f: &str) -> Vec<Vec<V>> {
    fs::read_to_string(f).unwrap()
        .trim().lines()
        .map(|s| s.split(',').map(cast).collect())
        .collect()
}

fn o(v: &V) -> String {
    match v {
        V::Str(s) => s.clone(),
        V::Num(n) => n.to_string(),
        V::Bool(b) => b.to_string(),
    }
}

// Config
#[derive(Debug)]
struct Config {
    bins: i32,
    budget: i32,
    check: i32,
    leaf: i32,
    p: f64,
    seed: u64,
    show: i32,
}

impl Default for Config {
    fn default() -> Self {
        Config { bins: 5, budget: 50, check: 5, leaf: 2, p: 2.0, seed: 1, show: 30 }
    }
}

// Tests
fn eg_the(the: &Config) { println!("{:?}", the); }

fn eg_sym() {
    let mut s = Col::new(0, "a");
    for c in "aaaabbc".chars() { s.add(&V::Str(c.to_string())); }
    println!("{}", o(&s.mid()));
}

fn eg_num() {
    let mut n = Col::new(0, "A");
    for i in 0..100 { n.add(&V::Num(i as f64)); }
    println!("{} {}", n.mu, n.sd());
}

fn main() {
    let mut the = Config::default();
    let args: Vec<String> = env::args().skip(1).collect();
    let mut i = 0;
    while i < args.len() {
        let k = args[i].trim_start_matches('-');
        match k {
            "the" => { srand(the.seed); eg_the(&the); }
            "sym" => { srand(the.seed); eg_sym(); }
            "num" => { srand(the.seed); eg_num(); }
            "bins" => { i += 1; the.bins = args[i].parse().unwrap(); }
            "budget" => { i += 1; the.budget = args[i].parse().unwrap(); }
            "check" => { i += 1; the.check = args[i].parse().unwrap(); }
            "leaf" => { i += 1; the.leaf = args[i].parse().unwrap(); }
            "p" => { i += 1; the.p = args[i].parse().unwrap(); }
            "seed" => { i += 1; the.seed = args[i].parse().unwrap(); }
            "show" => { i += 1; the.show = args[i].parse().unwrap(); }
            _ => {}
        }
        i += 1;
    }
}
```
