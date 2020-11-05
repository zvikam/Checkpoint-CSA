## problem
given an input file with a list of tiles
```
I, [N1, N2, N3, N4]; ...
```
where
- I is the index of the tile
- N[1-4] are numbers on the sides of the tiles
we need to find out the order of the tiles and how many times we should rotate each of them such that the numbers on 2 adjacent tiles match

e.g.
test
```
0,[0, 12, 2, 18]; 1,[0, 7, 6, 19]; 2,[5, 0, 0, 19]; 3,[6, 2, 9, 10]; 4,[14, 0, 5, 10]; 5,[7, 12, 0, 0]; 6,[0, 0, 18, 7]; 7,[0, 17, 9, 7]; 8,[0, 0, 14, 17]
```
solution
```
2,2; 1,0; 6,0; 4,2; 3,0; 0,1; 8,2; 7,2; 5,3'
```
## solver
implemented using recursive backtracking
