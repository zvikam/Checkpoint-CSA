## problem
given an online work-guessing game and a list of words.
the game responds with number of correct letters.
## solver
write a client that plays the game.
starting with the whole list of words as candidates and a random guess (1st word in the list).
for each response, remove the words that would not have given the same response if the guess was server's word.
this converges pretty quickly.

