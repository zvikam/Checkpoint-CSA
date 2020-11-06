import socket
import pprint
import datetime
import random
import time
import sys
import re


MAZE_SERVER = ('maze.csa-challenge.com', 80)
RECV_SIZE = 8192


def cls():
    print(chr(27) + '[2j')
    print('\033c')
    print('\x1bc')


def display(maze, location):
    w = len(maze[0])
    h = len(maze)
    view = 18
    for y in range(max(0, location[1]-view), min(h, location[1] + view)):
        for x in range(max(0, location[0]-view), min(w, location[0] + view)):
            c = 'X' if y == location[1] and x == location[0] else maze[y][x]
            sys.stdout.write('%s' % c)
        sys.stdout.write('\n')
    sys.stdout.write('\n')


def read_move(maze, location, allmoves):
    display(maze, location)
    move = input('$')
    allmoves += move
    return False, move


def find_move(maze, visits, location, dirnames, directions, allmoves):
    cls()
    display(maze, location)
    # pick a new move
    grade = []
    done = False
    w = len(maze[0])
    h = len(maze)
    for d in dirnames:
        # find out where we've never been and go there
        # outside is best!
        if (location[0] + directions[d][0]) < 0 or (location[0] + directions[d][0]) >= w or (
                location[1] + directions[d][1] < 0) or (location[1] + directions[d][1]) >= h:
            c = '*'
            #done = True
        else:
            c = maze[location[1] + directions[d][1]][location[0] + directions[d][0]]
            v = visits[location[1] + directions[d][1]][location[0] + directions[d][0]]
        g = {'#': 9999, 'o': v, '.': 0, '*': 9998}[c]
        grade.append({'dir': d, 'grade': g})
    m = min(grade, key=lambda k: k['grade'])
    # print(location, m, grade, end='\r')
    time.sleep(0.3)
    if m['grade'] == 9999:
        print("STUCK!")
        return True, 'h'
    move = m['dir']
    allmoves += move
    return done, move


def main():
    random.seed()
    conn = socket.create_connection(MAZE_SERVER)
    steps = ''

    def send_command(c):
        response = conn.recv(RECV_SIZE)

    def search(x, y, step):
        if maze[y][x] == 'X':
            steps += step
            return True
        elif maze[y][x] == '#':
            return False
        elif maze[y][x] == 'o':
            return False

        # mark as visited
        maze[y][x] = 'o'

        # explore neighbors clockwise starting by the one on the right
        if ((x < len(maze[0]) - 1 and search(x + 1, y, '>'))
                or (x > 0 and search(x - 1, y, '<'))
                or (y > 0 and search(x, y - 1, '^'))
                or (y < len(maze) - 1 and search(x, y + 1, 'V'))):
            steps += step
            return True
        return False

    allmoves = ''
    directions = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0]}
    dirnames = ['u', 'r', 'd', 'l']
    move = 'u'
    location = [1, 1]
    wall = False
    move_count = 0
    game_on = False
    deadlocked = 0

    # maze is 250x250, make room for the perimeter
    w = 252
    h = 252
    maze = [['.' for x in range(w)] for y in range(h)]
    visits = [[0 for x in range(w)] for y in range(h)]

    do_action = [
        lambda: (False, 'i'),
        lambda: find_move(maze, visits, location, dirnames, directions, allmoves),
        #lambda: read_move(maze, location, allmoves),
        lambda: (False, 'c'),
        lambda: (False, 'g')
    ]
    state = 0
    response = ''
    while True:
        #cls()
        moved = False
        game_on = False
        for line in response.splitlines():
            line = line.decode("utf-8")
            #print(line)
            if 'your starting position is' in line:
                m = re.search('\(([0-9]+),([0-9]+)\)$', line)
                location[0] = int(m.group(1))
                location[1] = int(m.group(2))
                moved = True
                continue
            elif 'csa' in line or 'CSA' in line:
                print(line)
                return
            elif line.startswith('>'):
                game_on = True
                continue
            elif line == '0':
                maze[location[1] + directions[move][1]][location[0] + directions[move][0]] = '#'
            elif line == '1':
                location = [location[0] + directions[move][0], location[1] + directions[move][1]]
                moved = True
            elif line.startswith('l='):
                for p in line.split(','):
                    d, v = p.strip().split('=')
                    if v == '0':
                        maze[location[1] + directions[d][1]][location[0] + directions[d][0]] = '#'
            elif line.startswith('('):
                m = re.search('\(([0-9]+),([0-9]+)\)$', line)
                loc = [int(m.group(1)), int(m.group(2))]
                if location != loc:
                    print("TRANSPORTED", location, loc)
                    loc = location
            else:
                print(line)
                pass

        if moved:
            # mark current location as visited
            maze[location[1]][location[0]] = 'o'
            # increment visits counter
            visits[location[1]][location[0]] += 1
            deadlocked = 0

        if game_on:
            if not moved:
                deadlocked += 1
                if deadlocked > 10:
                    print("DEADLOCK")
                    return

            done, move = do_action[state]()
            state = (state + 1) % len(do_action)

            #print(move)
            if done:
                solution = allmoves
                print('DONE!')
                print(solution)
                conn.send('s'.encode())
                conn.send(solution.encode())
            else:
                conn.send(move.encode())
                move_count += 1
        response = conn.recv(RECV_SIZE)


if __name__ == '__main__':
    main()

