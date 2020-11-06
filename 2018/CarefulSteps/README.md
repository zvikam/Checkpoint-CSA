## problem
given a set of archives, each with a comment field in the form of
```X, N```
where 
- X is a letter
- N is a number

## solver
we start with archive 0,  
advance forward (or backward) N steps to the next archive in line,  
appending its letter to the result.  
