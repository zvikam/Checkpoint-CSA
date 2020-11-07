## problem
given an online maze game
## solver
try different commands, find
- u = up
- d = down
- r = right
- l = left  

try to write a recursive decent client to exit the maze, which fails after a few minutes.  
print the maze and discover it has no exit, but appears to contain unreachable islands.  
  
try some more commands, find:
- g = goal - distance to goal if close enough
- c = current - current location
- i = inspect - get content of surrounding cells
- s = solve - send a solution

modify client to use ```inspect``` to make the maze converge faster, and issue ```goal``` command to try and reach the goal.  
every time the ```goal``` command returns a distance, use _Pythagoras Theorem_ to eliminate all the cells that can not contain the solution. after _3_ responses we find the goal location.  
try to reach goal, discover goal is always inside an unreachable island.  
send ```solve``` request with goal location as soon as we triangulate it's location.  
