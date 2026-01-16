# First Class Fucntions

In Lua, a function is just a value.  
Like a number.  
Like a string.

You can:
- store it in a variable
- pass it to another function
- return it from a function 

```lua
double = function(x) return x*x end
```    

IF we write functions to a table, we can make (e.g.) a demo
suite that we can call from the command-line; e.g. `lua fun.ad --a`.

```lua
eg,egs = {},{} -- "egs" used later
eg["--a"]= function(_) print(double(3)) end --> 9

function main(cli)
  for i,s in pairs(cli) do -- "arg" is the command line 
    if eg[s] then eg[s](cli[i+1]) end end end
```

Functions can be passed to other functions.

```lua
function kap(t,fn)  -- fn wants "key" and "value"
  local u={}; for k,v in pairs(t) do u[1+#u]=fn(k,v); end; return u end

function map(t,fn) -- fn wants just "value"
  return kap(t, function(_,v) return fn(v) end) end

eg["--b1"]=function(_) map({10,20,30}, print) end -->

-- 10
-- 20
-- 30

eg["--b2"]=function(_) 
   map(map({10,20,30}, double),print) end -->

-- 20
-- 40
-- 60

```

This can be used to (e.g.) fix a bug in Lua's table.concat function that 
crashed on booleans (we need to cast it to a string first).

```lua
function cat(t) return "{"..table.concat(map(t,tostring),", ") .. "}" end

eg["--c"]=function(_) print(cat({1,2,3}))end --> {1, 2, 3}
```
Of course we can to that recursively (X and Y or Z == Java;s X ? Y : Z)

```lua
function rat(t) return type(t)=="table" and cat(map(t,rat)) or tostring(t) end

eg["--d"]=function(_)
  print(rat({1,2,{10,20},{{300,400},50}})) end --> pretty recursive print
```
Functions store variables so first class functions can carray round state.

```lua
function lt(n) -- stand by for a function that returns... a function
  return function(a,b) return a[n] < b[n] end end

function sort(t,fn) -- Lua's built in sort does not return the table
  table.sort(t,fn)  -- if "fn" is nil, then just sort numerically
  return t end

eg["--eg"]=function(_,   t)
  t={{10,20,30,"a"},
     {30,10,20,"b"},
     {5, 30,50,"c"}}
  print("before:",rat(t))
  print("after:", rat(sort(t, lt(3))) end --> prints t sorted by last item
```
In Lua, some tables should be printed differently.
in Lua, some tables are simple arrays with numeric indexes 1,2,3... and
others are like dictionaries with symbolic indexes e.g. `{jan=31,feb=28,mar=31...}`. Lua can detect
dictionaries since the table size operator `#t` only counts consecutive numeric indexes (so `#t==0` for things with symbolic keys), 

```lua
function at(t)
  if type(t)~="table" then return tostring(t) end
  kv = function(k,v) return string.format("%s=%s", k, at(v)) end
  return cat(#t>0 and map(t,at) or sort(kap(t,kv))) end
```

Finally, a test suite:

```lua
eg["--all"]= function(_,    fn) 
  map(egs, function(s) print("\n"..s); assert(not eg[s](_)) end) end

eg["-h"] = function(_) print("lua fun.md " .. cat(egs)) end

for k,_ in pairs(eg) do if k ~= "--all" then egs[1+#egs]=k; table.sort(egs) end end
```

Main. In Lua, "arg" is the command line

```lua
main(arg)
```
