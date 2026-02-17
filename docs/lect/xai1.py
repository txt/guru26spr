#!/usr/bin/env python3 -B
"""
xai.py: explainable multi-objective optimzation   
(c) 2025 Tim Menzies, MIT license   
   
Input is CSV. Header (row 1) defines column roles as follows:   

    [A-Z]* : Numeric (e.g. "Age").     [a-z]* : Symbolic (e.g. "job").   
    *+     : Mximize (e.g. "Pay+").    *-     : Minimize (e.g. "Cost-").   
    *X     : Ignored (e.g. "idX").     ?      : Missing value (not in header)   
   
For help on command line options:
	⁃	
    ./xai.py -h

To install and test, got to http://tiny.cc/xaipy and download file. Then:   

    chmod +x xai.py   
    mkdir -p $HOME/gits   # download sample data    
    git clone http://github.com/timm/moot $HOME/gits/moot   
    ./xai.py --tree ~/gits/moot/optimize/misc/auto93.csv   
   
Options:   

    -h                help   
    -b bins=7         set number of bins for discretization   
    -B Budget=30      set number of rows to evaluate   
    -C Check=5        set number of guesses to check   
    -d data=data.csv  set data to load   
    -l leaf=2         set examples per leaves in a tree   
    -s seed=1         set random number seed   
"""
import ast, sys, random, re
from math import sqrt, exp, floor
from types import SimpleNamespace as obj
from typing import Any, Iterable, Iterator, Callable

# --- Intermediate Types ---
Qty = int | float
Row = list[Qty | str]
Rows = list[Row]
Obj = obj  # Alias for SimpleNamespace to simplify pseudo-class return hints

BIG: float = 1e32

### Constructors -----------------------------------------------------------
def Sym() -> Obj:
    """Constructs a Symbolic column tracker to count occurrences of distinct values."""
    return obj(it=Sym, n=0, has={})

def Num() -> Obj:
    """Constructs a Numeric column tracker to maintain count, mean, and variance."""
    return obj(it=Num, n=0, mu=0.0, m2=0.0)

def Col(at: int = 0, txt: str = " ") -> Obj:
    """
    Constructs a column representation. 
    Upper case names indicate Numeric, lower case indicate Symbolic.
    """
    col = (Num if txt[0].isupper() else Sym)()
    col.at, col.txt, col.target = at, txt, 0 if txt[-1] == "-" else 1
    return col

def Cols(names: list[str]) -> Obj:
    """Parses a list of column names, separating them into independent (x) and dependent (y) columns."""
    cols = [Col(n, s) for n, s in enumerate(names)]
    return obj(it=Cols, names=names, all=cols,
               x=[col for col in cols if col.txt[-1] not in "+-X"],
               y=[col for col in cols if col.txt[-1] in "+-"])

def Data(rows: Iterable[Row] | None = None) -> Obj:
    """Initializes a Data object to hold rows and their corresponding column structures."""
    return adds(rows, obj(it=Data, rows=[], n=0, cols=None, _centroid=None))

def clone(data: Obj, rows: Iterable[Row] | None = None) -> Obj:
    """Creates a new Data object with the same column structure as the original, optionally populated with rows."""
    return adds(rows, Data([data.cols.names]))


### Update ----------------------------------------------------------------
def adds(src: Iterable[Any] | None, i: Obj | None = None) -> Obj:
    """Pushes a collection of items (e.g., rows or numbers) into the target object `i`."""
    i = i or Num()
    [add(i, v) for v in src or []]
    return i

def add(i: Obj, v: Any, inc: int = 1) -> Any:
    """
    Adds a single value `v` into an object `i`. 
    Handles updates for Sym (counts), Num (Welford's algorithm for variance), and Data (rows).
    """
    if v != "?":
        if Data is i.it and not i.cols: 
            i.cols = Cols(v) # init, not adding
        else:
            i.n += inc # adding
            if Sym is i.it: 
                i.has[v] = inc + i.has.get(v, 0)
            elif Num is i.it: 
                if inc < 0 and i.n < 2:
                    i.mu = i.m2 = i.n = 0
                else:
                    d = v - i.mu
                    i.mu += inc * d / i.n
                    i.m2 += inc * d * (v - i.mu)
            else: # Data is i.it
                i._centroid = None # old centroid now out of date
                [add(col, v[col.at], inc) for col in i.cols.all] # recursive add 
                (i.rows.append if inc > 0 else i.rows.remove)(v)   # row storage
    return v # convention: always return the thing being added


### Queries ----------------------------------------------------------------
def norm(num: Obj, n: Qty | str) -> float:
    """Normalizes a number using a logistic function to handle outliers."""
    if n == "?": return 0.0
    z = (float(n) - num.mu) / sd(num)
    z = max(-3, min(3, z))
    return 1 / (1 + exp(-1.7 * z))

def sd(num: Obj) -> float:
    """Calculates the standard deviation of a Numeric column."""
    return 1/BIG + (0 if num.n < 2 else sqrt(max(0, num.m2) / (num.n - 1)))

def mid(col: Obj) -> Qty | str:
    """Calculates the central tendency of a column (mean for Num, mode for Sym)."""
    return col.mu if Num is col.it else max(col.has, key=col.has.get)

def mids(data: Obj) -> Row:
    """Calculates and caches the central tendencies of all columns in a Data object."""
    data._centroid = data._centroid or [mid(col) for col in data.cols.all]
    return data._centroid

def disty(data: Obj, row: Row) -> float:
    """Calculates the Euclidean distance of a row's dependent (y) variables to the target ideal."""
    ys = data.cols.y
    return sqrt(sum(abs(norm(y, row[y.at]) - y.target)**2 for y in ys) / len(ys))

def distx(data: Obj, row1: Row, row2: Row) -> float:
    """Calculates the Euclidean distance between two rows based on their independent (x) variables."""
    xs = data.cols.x
    return sqrt(sum(_aha(x, row1[x.at], row2[x.at])**2 for x in xs) / len(xs))

def _aha(col: Obj, u: Qty | str, v: Qty | str) -> float:
    """Helper calculating the absolute distance between two specific cell values."""
    if u == v == "?": return 1.0
    if Sym is col.it: return float(u != v)
    u_norm, v_norm = norm(col, u), norm(col, v)
    u_val = u_norm if u != "?" else (0.0 if v_norm > 0.5 else 1.0)
    v_val = v_norm if v != "?" else (0.0 if u_norm > 0.5 else 1.0)
    return abs(u_val - v_val)


## Cutting -------------------------------------------------------------------
def Cut(at: int, txt: str, lo: float, hi: float) -> Obj: 
    """Constructs a Cut range representing a discretization bin for a column."""
    return obj(it=Cut, at=at, txt=txt, xlo=lo, xhi=hi, y=Num())

def cutShow(cut: Obj, accept: bool = True) -> str:
    """Returns a string representation of a Cut range."""
    s, lo, hi = cut.txt, cut.xlo, cut.xhi
    if lo == hi: return f"{s} {'==' if accept else '!='} {lo}"
    if hi == BIG: return f"{s} {'>=' if accept else '<'} {lo}"
    if lo == -BIG: return f"{s} {'<' if accept else '>='} {hi}"
    return f"{lo} <= {s} < {hi}" if accept else f"{s} < {lo} or {s} >= {hi}"

def cutSelects(cut: Obj, row: Row) -> bool:
    """Checks if a given row falls within the specified Cut range."""
    if (x := row[cut.at]) == "?": return True
    if cut.xlo == cut.xhi: return x == cut.xhi
    return cut.xlo <= float(x) < cut.xhi

def cutScore(cut: Obj) -> float: 
    """Scores a cut based on variance and count; lower is better."""
    if cut.y.n < the.leaf: return BIG
    return cut.y.mu + sd(cut.y) / (sqrt(cut.y.n) + 1/BIG)

def cutBest(data: Obj, rows: Rows) -> Obj | None:
    """Evaluates all possible cuts across all columns to find the single best split."""
    all_bins = (b for col in data.cols.x for b in cutsAll(col, rows, data))
    return min(all_bins, key=lambda b: cutScore(b), default=None)

def cutsAll(col: Obj, rows: Rows, data: Obj) -> list[Obj]:
    """Generates all possible bins for a specific column given a subset of rows."""
    d, xys = {}, [(r[col.at], disty(data, r)) for r in rows if r[col.at] != "?"]
    for x, y in sorted(xys):
        k = x if Sym is col.it else floor(the.bins * norm(col, x))
        if k not in d: 
            d[k] = Cut(col.at, col.txt, float(x), float(x))
        add(d[k].y, y)
        d[k].xhi = float(x)
    return cutsComplete(col, sorted(d.values(), key=lambda b: b.xlo))

def cutsComplete(col: Obj, cuts: list[Obj]) -> list[Obj]:
    """Expands bounds on a sorted list of cuts so they cover the entire number line."""
    if Num is col.it:
        for n, b in enumerate(cuts):
            b.xlo = cuts[n-1].xhi if n > 0 else -BIG
            b.xhi = cuts[n+1].xlo if n < len(cuts)-1 else BIG
    return cuts


## Trees -------------------------------------------------------------------
def Tree(data: Obj, rows: Rows, cut: Obj | None) -> Obj:
    """Constructs a Tree node holding splitting criteria and branch paths."""
    centroid = mids(clone(data, rows))
    return obj(it=Tree, n=len(rows), mu=disty(data, centroid), cut=cut, 
               kids={},
               mids=[centroid[col.at] for col in data.cols.y],
               goals=[col.txt for col in data.cols.y])

def treeGrow(data: Obj, rows: Rows | None = None, cut: Obj | None = None, uses: set[str] | None = None) -> Obj:
    """Recursively splits data using the best cuts to grow a decision tree."""
    rows = rows or data.rows
    uses = uses if uses is not None else set()
    tree = Tree(data, rows, cut)
    if len(rows) > the.leaf * 2:
        if cut1 := cutBest(data, rows):
            ok, no = [], []
            for row in rows: 
                (ok if cutSelects(cut1, row) else no).append(row)
            if ok and no:
                uses.add(cut1.txt)
                tree.kids[True]  = treeGrow(data, ok, cut1, uses)
                tree.kids[False] = treeGrow(data, no, cut1, uses)
    return tree

def treeShow(tree: Obj, lvl: int = 0, accept: bool = True, width: int = 60, dec: int = 1) -> None:
    """Recursively prints the decision tree structure to standard output."""
    if lvl == 0:
        print(" ")
        print((' ' * width) + f"  score     N   ", ', '.join(tree.goals))
        print((' ' * width) + f"  -----    ---   -------------------")
    here = f"{cutShow(tree.cut, accept)} " if lvl > 0 else "."
    report = f"{'| ' * (lvl-1)}{here}"
    print(f"{report:{width}}: {o(tree.mu):6}: {tree.n:>4} : ",
          ', '.join([f"{o(n, DEC=dec)}" for n in tree.mids]))
    for k, kid in tree.kids.items():
        treeShow(kid, lvl + 1, k, width, dec)

def treeLeaf(tree: Obj, row: Row) -> Obj:
    """Traverses the tree to find the terminal leaf node corresponding to a given row."""
    if tree.kids:
        rule = tree.kids[True].cut 
        return treeLeaf(tree.kids[cutSelects(rule, row)], row)
    return tree

   
## Lib -----------------------------------------------------------------------
def gauss(mid: float, div: float) -> float:
    """Generates a pseudo-Gaussian random number given a mean and standard deviation."""
    return mid + 2 * div * (sum(random.random() for _ in range(3)) - 1.5)

def o(v: Any = None, DEC: int = 2, **D: Any) -> str:
    """Utility for pretty-printing numbers, dictionaries, and classes."""
    if D: return o(D, DEC=DEC)
    isa = isinstance
    if isa(v, (int, float)): return f"{round(v, DEC):_}"
    if isa(v, list):  return f"[{', '.join(o(k, DEC) for k in v)}]"
    if isa(v, tuple): return f"({', '.join(o(k, DEC) for k in v)})"
    if callable(v):   return v.__name__
    if hasattr(v, "__dict__"): v = vars(v)
    if isa(v, dict): return "{" + " ".join(f":{k} {o(v[k], DEC)}" for k in v) + "}"
    return str(v)

def coerce(s: str) -> str | int | float | bool:
    """Converts a raw string into an int, float, or boolean where possible."""
    try: return int(s)
    except Exception as _:
        try: return float(s)
        except Exception as _:
            s = s.strip()
            return {"true": True, "false": False}.get(s, s)

def csv(fileName: str) -> Iterator[Row]:
    """Generator that yields lazily evaluated, coerced rows from a CSV file."""
    with open(fileName, encoding="utf-8") as f:
        for l in f:
            if (l := l.split("%")[0].strip()):
                yield [coerce(x) for x in l.split(",")]

def shuffle(lst: list[Any]) -> list[Any]: 
    """In-place shuffle of a list, returning the list itself."""
    random.shuffle(lst); return lst


#-----------------------------------------------------------------------------
# Global configurations setup from the module docstring
the: Obj = obj(**{m[0]: coerce(m[1]) for m in re.findall(r"(\w+)=(\S+)", __doc__)})

def go__all(file: str = the.data) -> None:
    """FILE : run all the following tests""" 
    for k, fun in globals().items():
        if k.startswith("go__") and k != "go__all":
            random.seed(the.seed)
            print("\n#", k, "------------")
            fun(file)

def go__num(_: Any = None) -> None:
    """: test Nums implementation"""
    num = adds(gauss(10, 2) for _ in range(1000))
    print(o(mu=num.mu, sd=sd(num)))
    assert 9.9 <= num.mu <= 10.1 and 1.9 <= sd(num) <= 2.1

def go__sym(_: Any = None) -> None:
    """: test Syms implementation"""
    sym = adds('Previously, we have defined an iterative data mining', Sym())
    print(sym.has)
    assert sym.has["a"] == 5

def go__csv(file: str = the.data) -> None:
    """FILE : test csv loading properly coerces elements"""
    total = 0
    for n, row in enumerate(csv(file)):
        if n > 0: total += len(row)
        if n > 0: assert isinstance(row[1], (float, int))
        if n % 40 == 0: print(row)
    assert 3184 == total

def go__data(file: str = the.data) -> None:
    """FILE : test adding columns from file directly to Data obj"""
    data = Data(csv(file))
    total = sum(len(row) for row in data.rows)
    print(*data.cols.names)
    assert Num is data.cols.all[0].it
    assert 3184 == total
    for col in data.cols.x: print(o(col))

def go__clone(file: str = the.data) -> None:
    """FILE : test echoing structure of a table to a new table"""
    data1 = Data(csv(file))
    data2 = clone(data1, data1.rows)
    assert data1.cols.x[1].mu == data2.cols.x[1].mu

def go__distx(file: str = the.data) -> None:
    """FILE : show we sort rows by their distance to one row"""
    data = Data(csv(file))
    print(*data.cols.names, "distx", sep=",")
    r1 = data.rows[0]
    data.rows.sort(key=lambda r2: distx(data, r1, r2))
    for n, r2 in enumerate(data.rows[1:]):
        assert 0 <= distx(data, r1, r2) <= 1
        if n % 40 == 0: print(*r2, o(distx(data, r1, r2)), sep=",")

def go__disty(file: str = the.data) -> None:
    """FILE : show we sort rows by their distance to 'heaven' (ideal target)"""
    data = Data(csv(file))
    print(*data.cols.names, "disty", sep=",")
    data.rows.sort(key=lambda r: disty(data, r))
    for n, r1 in enumerate(data.rows):
        if n > 0:
            r2 = data.rows[n-1]
            assert disty(data, r1) >= disty(data, r2)
        if n % 40 == 0: print(*r1, o(disty(data, r1)), sep=",")

def go__bins(file: str = the.data) -> None:
    """FILE : show the rankings of all bins computed for all features"""
    data = Data(csv(file))
    all_bins = (b for col in data.cols.x for b in cutsAll(col, data.rows, data))
    for b in sorted(all_bins, key=lambda b: cutScore(b)):
        print(f"{cutShow(b):20}", o(mu=b.y.mu, sd=sd(b.y), n=b.y.n, 
                                   scored=cutScore(b)), sep="\t")

def go__tree(file: str = the.data) -> None: 
    """FILE : run the optimizer once, show the tree output"""
    data = Data(csv(file)) 
    lo, mid = go_tree_stats(data) 
    rows = shuffle(data.rows) 
    n = len(rows) // 2
    best, tree, uses = trainTest(data, rows[:n][:the.Budget - the.Check], rows[n:])
    treeShow(tree, width=35)
    d = disty(data, best)
    print(o(uses=len(uses), x=len(data.cols.x), y=len(data.cols.y),
            rows=len(data.rows), ylo=lo, ymid=mid, guess=d, 
            score=go_tree_score(d, lo, mid)))

def go_tree_stats(data: Obj) -> tuple[float, float]:
    """Helper to compute baseline target spread."""
    out = sorted(disty(data, r) for r in data.rows)
    return out[0], out[len(out)//2] 

def trainTest(data: Obj, train: Rows, test: Rows) -> tuple[Row, Obj, set[str]]:
    """Helper orchestrating train-test split for Tree evaluation."""
    uses = set()
    tree = treeGrow(clone(data, train), uses=uses)
    ranking = sorted(test, key=lambda r: treeLeaf(tree, r).mu)
    return min(ranking[:the.Check], key=lambda r: disty(data, r)), tree, uses

def go_tree_score(d: float, lo: float, mid: float) -> int:
    """Helper scoring the tree guesses."""
    return int(100 * (1 - (d - lo) / (mid - lo + 1/BIG)))

def go__xais(file: str = the.data, repeats: int = 20) -> None: 
    """FILE : run the optimizer multiple times, report performance stats"""
    data = Data(csv(file)) 
    lo, mid = go_tree_stats(data) 
    wins, guesses = Num(), Num()
    for _ in range(repeats):
        rows = shuffle(data.rows) 
        n = len(rows) // 2
        best, _, _ = trainTest(data, rows[:n][:the.Budget - the.Check], rows[n:])
        d = disty(data, best)
        add(guesses, d)
        add(wins, go_tree_score(d, lo, mid))
    print(o(wins=int(wins.mu), n=guesses.n, lo=lo, mid=mid, guess=o(guesses.mu)),
           re.sub(r".*/", "", file))


#-----------------------------------------------------------------------------
def main(funs: dict[str, Callable], settings: Obj) -> Obj:
    """Main execution point for handling CLI args and running tests."""
    for n, s in enumerate(sys.argv):
        arg = coerce(sys.argv[n + 1]) if n < len(sys.argv) - 1 else None
        if fn := funs.get(f"go{s.replace('-', '_')}"):
            fn(arg) if arg is not None else fn()
        elif s == "-h":
            showHelp(funs)
        else:
            for k in settings.__dict__:
                if k[0] == s.lstrip("-")[0]: settings.__dict__[k] = arg
    return settings

def showHelp(funs: dict[str, Callable], prefix: str = "go_") -> None:
    """Prints the docstring help menu for CLI options."""
    print(__doc__)
    for k, f in funs.items():
        if k.startswith(prefix) and f.__doc__:
            left, right = f.__doc__.split(":")
            left = k[2:].replace("_", "-") + " " + left.strip()
            print(f"  {left:15}   {right.strip()}")

random.seed(the.seed)
if __name__ == "__main__": 
    the = main(vars(), the)

print(1)
