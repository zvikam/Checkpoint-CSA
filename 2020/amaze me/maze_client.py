import socket
import pprint
import datetime
import string
import random
import time
import sys
import re
from math import sqrt


MAZE_SERVER = ('maze.csa-challenge.com', 80)
RECV_SIZE = 8192
DISPLAY_SIZE = 12


def cls():
    print(chr(27) + '[2j')
    print('\033c')
    print('\x1bc')


def display(maze, location):
    w = len(maze[0])
    h = len(maze)
    view = DISPLAY_SIZE
    for y in range(max(0, location[1]-view), min(h, location[1] + view)):
        for x in range(max(0, location[0]-view), min(w, location[0] + view)):
            c = 'X' if y == location[1] and x == location[0] else maze[y][x]
            sys.stdout.write('%s' % c)
        sys.stdout.write('\n')
    sys.stdout.write('\n')
    # time.sleep(1)


def main():
    global DISPLAY_SIZE

    random.seed()
    conn = socket.create_connection(MAZE_SERVER)
    steps = ''
    directions = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0]}
    revert = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r'}
    location = [1, 1]

    # maze is 250x250
    w = 252
    h = 252
    maze = [['.' for x in range(w)] for y in range(h)]

    g_responses = ['farfaraway', 'Yourdistancefromthetreasureis']
    h_responses = [
        "Don't forget to eat breakfast, it's the most important meal in the day",
        "I believe you could find it, just use your brain.",
        "I wish I could help you, but I can't.",
        "Don't give up, try harder.",
        "Really???"
    ]
    goal_locations = []
    for x in range(1, 250):
        for y in range(1, 250):
            goal_locations.append((x, y))

    def send_receive(c=None):
        if c:
            conn.send(c.encode())
        done = False
        lines = []
        while not done:
            response = conn.recv(RECV_SIZE)
            for line in response.splitlines():
                line = line.decode("utf-8")
                if line.startswith('>'):
                    done = True
                else:
                    if 'CSA' in line or 'csa' in line:
                        done = True
                    lines.append(line)
        return lines

    def send_command(c):
        nonlocal location
        nonlocal goal_locations

        res = False
        lines = send_receive(c)
        for line in lines:
            if 'csa' in line or 'CSA' in line:
                print(line)
                return
            elif line == '0':
                maze[location[1] + directions[c][1]][location[0] + directions[c][0]] = '#'
            elif line == '1':
                location = [location[0] + directions[c][0], location[1] + directions[c][1]]
            elif line.startswith('l='):
                for p in line.split(','):
                    d, v = p.strip().split('=')
                    if v == '0':
                        maze[location[1] + directions[d][1]][location[0] + directions[d][0]] = '#'
                    if v == '1':
                        #maze[location[1] + directions[d][1]][location[0] + directions[d][0]] = 'o'
                        pass
            elif line.startswith('('):
                m = re.search('\(([0-9]+),([0-9]+)\)$', line)
                location = [int(m.group(1)), int(m.group(2))]
            else:
                if c == 'g':
                    txt = ''.join([c for c in line if c in string.ascii_letters])
                    if txt not in g_responses:
                        print(line)
                        input('acknowledge new g response')
                        g_responses.append(txt)
                    if '√' in line:
                        distance_sq = int(line.split()[-1])
                        if len(goal_locations) > 1:
                            locations = []
                            for g in goal_locations:
                                dx = abs(location[0] - g[0])
                                dy = abs(location[1] - g[1])
                                d = dx**2 + dy**2
                                if d == distance_sq:
                                    locations.append(g)
                            goal_locations = locations
                            if len(goal_locations) == 1:
                                maze[goal_locations[0][1]][goal_locations[0][0]] = 'G'
                                print('GOAL FOUND', goal_locations)
                                send_command('s')
                                send_command('(%d,%d)' % (goal_locations[0][0], goal_locations[0][1]))
                                res = True
                            if len(goal_locations) == 0:
                                print('GOAL LOST!')
                        # print("distance to target:", sqrt(distance_sq), goal_locations)
                        if distance_sq == 0:
                            res = True
                        # send_command('h')
                elif c == 'h':
                    if line not in h_responses:
                        print(line)
                        # input('acknowledge new h response')
                        h_responses.append(line)
                else:
                    print(location, line)
        return res, lines

    def search(x, y, step):
        nonlocal steps

        # check geo-fence
        # if x < geo_fence['xmin'] or x > geo_fence['xmax'] or y < geo_fence['ymin'] or y > geo_fence['ymax']:
        #    print("geo-fence hit", x, y)
        #    return False

        # check if we shouldn't be here
        if maze[y][x] == '#':
            return False
        elif maze[y][x] == 'o':
            return False

        # move
        if step is not '':
            send_command(step)

        # get location
        send_command('c')
        # print(location, end='r')
        # sys.stdout.write('%s\t\r' % location)
        # sys.stdout.flush()

        # check if we're done
        res, lines = send_command('g')
        if res:
            print(lines)
            steps += step
            return True

        # check surroundings
        send_command('i')

        # GOAL found
        if maze[y][x] == 'G':
            print('GOAL')
            steps += step
            return True

        # mark as visited
        maze[y][x] = 'o'

        if len(goal_locations) == 1:
            dx = abs(location[0] - goal_locations[0][0])
            dy = abs(location[1] - goal_locations[0][1])
            # if dx < DISPLAY_SIZE and dy < DISPLAY_SIZE:
            # if dx**2 + dy**2 < 144:
            #    send_command('h')
            #    # display(maze, location)
            #    pass
        # display(maze, location)

        # explore neighbors clockwise starting by the one on the right
        if ((x < len(maze[0]) - 1 and search(x + 1, y, 'r'))
                or (x > 0 and search(x - 1, y, 'l'))
                or (y > 0 and search(x, y - 1, 'd'))
                or (y < len(maze) - 1 and search(x, y + 1, 'u'))):
            steps += step
            return True
        if step in revert:
            send_command(revert[step])
        return False

    try:
        # receive header
        send_receive()
        # check start position
        send_command('c')
        search(location[0], location[1], '')
        print(steps[::-1])
    except KeyboardInterrupt:
        pass
    # DISPLAY_SIZE = 250
    # display(maze, location)


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    main()
