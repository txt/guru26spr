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

# More on Lua

Recall that Lua has "tables" that switch from arrays to dictionaries,
depending on their keys?

- all numeric keys running 1,2...n
  - `t` is an array!
  - `#t==n`
  - if we iterate thiugh `t`,  we always get the same order   
    `for j,n in pairs({"name","age") do print(j,n) end` prints  
    "1 name"    
    "2 age"   
- keys are symbols `apples`, `oranges` etc...
  - e.g. `t={applies=4, oranges}=2`
  - #t==0
  - if we iterate thiugh a table, we may not get the same order   
    `for j,n in pairs({name="tim",age=21) do print(j,n) end` prints  
    name or age first in any order.

So my pretty printer of nested tables had to:

```lua
local function o(t,     u,k)
  if math.type(t)=="float" then return fmt("%.2f",t) end
  if type(t)~="table" then return tostring(t) end u={}
  if #t>0 then for i=1,#t do u[i]=o(t[i]) end
  else 
     k={} 
     for n in pairs(t) do k[#k+1]=n end 
     table.sort(k)
     for i=1,#k do u[i]=fmt(":%s %s",k[i],o(t[k[i]])) end 
  end
  return "{"..table.concat(u," ").."}" end 
```
Now what is we spread some iterator magic? What about all that nonesens of ``are you
a table or ana array" was buried away inside an iterator.   

local function o(t,     u,k)

  if math.type(t)=="float" then return fmt("%.2f",t) end

  if type(t)~="table" then return tostring(t) end u={}

  if #t>0 then for i=1,#t do u[i]=o(t[i]) end

  else 

      k={} 

     for n in pairs(t) do k[#k+1]=n end 

     table.sort(k)

     for i=1,#k do u[i]=fmt(":%s %s",k[i],o(t[k[i]])) end 

  end

  return "{"..table.concat(u," ").."}" end
