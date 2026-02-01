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
onst txt = await fetch("data.txt").then(r => r.text())

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
let adds = (items, it) => {
  it = it || NUM()
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
