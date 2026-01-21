-- <p align="center">
--   <a href="https://github.com/txt/guru26spr/blob/main/README.md"><img 
--      src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
--   <a href="https://github.com/txt/guru26spr/blob/main/docs/lect/syllabus.md"><img 
--       src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
--   <a href="https://docs.google.com/spreadsheets/d/1xZfIwkmu6hTJjXico1zIzklt1Tl9-L9j9uHrix9KToU/edit?usp=sharing"><img
--       src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
--   <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8119"><img 
--       src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
--   <a href="https://discord.gg/vCCXMfzQ"><img 
--       src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
--   <a href="https://github.com/txt/guru26spr/blob/main/LICENSE.md"><img 
--       src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
-- <h1 align="center">:cyclone: CSC491/591: How to be a SE Guru <br>NC State, Spring '26</h1>
-- <img src="https://raw.githubusercontent.com/txt/guru26spr/refs/heads/main/etc/img/banenr.png"> 
-- 
-- <!--- let g:markdown_fenced_languages = ['lua'] -->
-- 
-- In Lua, a function is just a value.  
-- Like a number.  
-- Like a string.
-- 
-- You can:
-- - store it in a variable
-- - pass it to another function
-- - return it from a function 
-- 

double = function(x) return x+x end
-- 
-- 
-- IF we write functions to a table, we can make (e.g.) a demo
-- suite that we can call from the command-line; e.g. `lua fun.ad --a`.
-- 

eg,egs = {},{} -- "egs" used later
eg["--a"]= function(_) print(double(3)) end --> 9

enumerate=pairs -- emualte pythons loop function (returns index and var)

function main()
  for i,s in enumerate(arg) do -- "arg" is the command line 
    if eg[s] then eg[s](arg[i+1]) end end end
-- 
-- 
-- Functions can be passed to other functions.
-- 

function same(x) return x end -- the classic "do nothing" function

function kap(t,fn)  -- fn wants "key" and "value"
  local u={}
  for k,v in enumerate(t) do u[1+#u] = (fn or same)(k,v) end
  return u end

function map(t,fn) -- fn wants just "value"
  return kap(t, function(_,v) return (fn or same)(v) end) end

  
eg["--b1"]=function(_) map({10,20,30}, print) end -->

-- 10
-- 20
-- 30

eg["--b2"]=function(_) 
   map(map({10,20,30}, double),print) end -->

-- 20
-- 40
-- 60

function sum(t,fn)
  local n=0; map(t, function(v) n = n + (fn or same)(v) end); return n end

eg["--b3"]=function(_) 
   print(sum({10,20,30}, double)) end --> 120

-- 
-- 
-- This can be used to (e.g.) fix a bug in Lua's table.concat function that 
-- crashed on booleans (we need to cast it to a string first).
-- 

function cat(t) return "{"..table.concat(map(t,tostring),", ") .. "}" end

eg["--c"]=function(_) print(cat({1,2,3}))end --> {1, 2, 3}
-- 
-- Of course we can to that recursively (X and Y or Z == Java;s X ? Y : Z)
-- 

function rat(t) return type(t)=="table" and cat(map(t,rat)) or tostring(t) end

eg["--d"]=function(_)
  print(rat({1,2,{10,20},{{300,400},50}})) end --> pretty recursive print
-- 
-- Functions store variables so first class functions can carray round state.
-- 

function lt(n) -- stand by for a function that returns... a function
  return function(a,b) return a[n] < b[n] end end -- lua tables start at "1", not ")"

function sort(t,fn) -- Lua's built in sort does not return the table
  table.sort(t,fn)  -- if "fn" is nil, then just sort numerically
  return t end

eg["--eg"]=function(_,   t)
  t={{10,20,30,"a"},
     {30,10,20,"b"},
     {5, 30,50,"c"}}
  print("before:",rat(t))
  print("after:", rat(sort(t, lt(3)))) end --> prints t sorted by last item
-- 
-- In Lua, some tables should be printed differently.
-- - some tables are simple arrays with numeric indexes 1,2,3... and
-- - others are like dictionaries with symbolic indexes e.g. `{jan=31,feb=28,mar=31...}`. 
-- - Lua can detect
-- dictionaries since the table size operator `#t` only counts consecutive numeric indexes (so `#t==0` for things with symbolic keys), 
-- 

function at(t)
  if type(t)~="table" then return tostring(t) end
  kv = function(k,v) return string.format("%s=%s", k, at(v)) end
  return cat(#t>0 and map(t,at) or sort(kap(t,kv))) end --  X and Y or Z == X ? Y : Z
-- 
-- 
-- Example of polymorphism: different shapes, same interface
-- 

function Circle(r) return {isa="circle", area=function(_) return 3.14*r*r end} end
function Rect(w,h) return {isa="rect", area=function(_) return w*h end} end
function Tri(b,h) return {isa="triangle", area=function(_) return 0.5*b*h end} end

eg["--poly"] = function(_,   shapes)
  shapes = {Circle(5), Rect(4,6), Tri(10,8)}
  print(rat(shapes))
  print("Total: ", sum(shapes, function(s) return s.area(s) end)) end
-- 
-- 
-- That polymorphism is so handy, its actually expected in Lua code
-- 

function isa(x,y) x.__index=x; return setmetatable(y,x) end 

Person={}
function Person:new(name,age) return isa(Person,{name=name, dob=age-1900}) end

NOW = 2026
function Person:age() return (NOW - self.dob) end

eg["--q"] = function(   who)
   who=Person:new("tim", 2000)
   print(at(who))
   print(who:age()) end
-- 
-- 
-- And finally, a test suite:
-- 

eg["--all"]= function(_,    fn) 
  map(egs, function(s) print("\n"..s); assert(not eg[s](_)) end) end

eg["-h"] = function(_) print("lua fun.md " .. cat(egs)) end

for k,_ in enumerate(eg) do 
  if k ~= "--all" then egs[1+#egs]=k; table.sort(egs) end end
-- 
-- 
-- Main. In Lua, "arg" is the command line
-- 

main()
-- 
