import sys
import time
from socket import create_connection

SERVER = ('tricky-guess.csa-challenge.com', 2222)
RECV_SIZE = 8192


def compare_words(a, b):
    #print(set(a.lower()))
    #print(set(b.lower()))
    #print(set(a.lower()).difference(set(b.lower())))
    return len(set(a.lower()).difference(set(b.lower())))


def find_guesses(word, words, score):
    res = []
    for w in words:
        if not w == word:
            if compare_words(word, w) == score:
                res.append(w)
    return res


def main():
    with open('tricky_guess_words.txt', 'r') as fin:
        words = fin.read().splitlines()
        #print(compare_words(words[0], words[1]))
        #return
    conn = create_connection(SERVER)
    options = words
    go = False
    solution = ''
    while True:
        response = conn.recv(RECV_SIZE).decode('utf-8')
        print(response)
        if not go:
            if 'GO !' not in response:
                continue
            go = True

        if 'csa' in response:
            break

        if solution is not '':
            score = int(response)
            options = find_guesses(solution, options, len(solution) - score)

        print('number of options left', len(options))
        if not options:
            break
        solution = options[0] + '\n'
        print('guessing', solution)
        conn.send(solution.encode())


if __name__ == '__main__':
    main()
