import json
import math
import sys


test1 = '0,[0, 12, 2, 18]; 1,[0, 7, 6, 19]; 2,[5, 0, 0, 19]; 3,[6, 2, 9, 10]; 4,[14, 0, 5, 10]; 5,[7, 12, 0, 0]; 6,[0, 0, 18, 7]; 7,[0, 17, 9, 7]; 8,[0, 0, 14, 17]'
solution1 = '2,2; 1,0; 6,0; 4,2; 3,0; 0,1; 8,2; 7,2; 5,3'


class Cube(object):
    def __init__(self, s):
        o = json.loads('[%s]' % s)
        self._id = o[0]
        self._values = o[1]
        self._orig_values = self._values[:]
        self._rotate = 0
        self._used = False

    # def __str__(self):
    #     return '%d,[%s]' % (self._id, ','.join([str(x) for x in self._values]))

    def show(self):
        return '%d,%d' % (self._id, self._rotate)

    def show1(self):
        return '%d' % (self._id)

    def zeros(self):
        return len([x for x in self._values if x == 0])

    def value(self, direction):
        try:
            return self._values[direction]
        except:
            pass
        return None

    def opposite(self, direction):
        return self._values[(direction + 2) % 4]

    def use(self):
        if self._used:
            return False
        self._used = True
        return True

    def release(self):
        self._used = False
        self._values = self._orig_values[:]
        self._rotate = 0

    def rotate(self):
        if self._rotate == 3:
            return False
        self._values = self._values[3:] + self._values[:3]
        self._rotate = (self._rotate + 1) % 4
        return True


class Cell(object):
    def __init__(self, neighbors=None):
        self._neighbors = [None] * 4
        self.place(neighbors)
        self._x = -1
        self._y = -1
        self._cubes = None
        self._cube = -1

    def indices(self, x, y):
        self._x = x
        self._y = y

    def place(self, neighbors):
        if neighbors:
            self._neighbors = neighbors  # top, right, bottom, left

    def zeros(self):
        return len([x for x in self._neighbors if x is None])

    def set_options(self, cubes):
        self._cubes = cubes

    def get_cube(self):
        if self._cube in range(len(self._cubes)):
            return self._cubes[self._cube]
        return None

    def get_connected(self, direction):
        if self._neighbors[direction] is None:
            return 0
        if self._neighbors[direction].get_cube() is None:
            return -1
        return self._neighbors[direction].get_cube().opposite(direction)

    def clear(self):
        if self._cube >= 0:
            self.get_cube().release()
            self._cube = -1

    def check_match(self):
        for d in range(4):
            op = self.get_connected(d)
            # if op < 0:
            #     return True
            if self.get_cube().value(d) != op:
                return False
        return True

    def check_match_frame(self, include_neighbors):
        for d in range(4):
            if self._neighbors[d] is None:
                if self.get_cube().value(d) != 0:
                    return False
            elif include_neighbors:
                if self._neighbors[d] is not None and self._neighbors[d].zeros() > 0:
                    if self.get_cube() is not None and self.get_cube().value(d) != self.get_connected(d):
                        return False
        return True

    def try_next(self):
        if self.get_cube():
            if self.zeros() == 0:
                if self.get_cube().rotate():
                    return True
            self.get_cube().release()
        while self._cube < len(self._cubes)-1:
            self._cube += 1
            if self.get_cube().use():
                self.turn_to_match_frame()
                return True
        self._cube = -1
        return False

    def turn_to_match_frame(self):
        while True:
            if self.check_match_frame(False):
                return True
            if not self.get_cube().rotate():
                break
        return False

    def turn_to_match(self):
        while True:
            if self.check_match():
                return True
            if not self.get_cube().rotate():
                break
        return False


class Board(object):
    def __init__(self, cubes):
        self._size = int(math.sqrt(len(cubes)))
        self._board = [[None]] * self._size
        self._cells = []
        self._frame = []
        self._inner = []
        for y in range(self._size):
            self._board[y] = [None] * self._size
            for x in range(self._size):
                cell = Cell()
                self._board[y][x] = cell
                self._board[y][x].indices(x, y)
                self._cells.append(cell)

        for y in range(self._size):
            for x in range(self._size):
                neighbors = [self._board[y-1][x] if y-1 >= 0 else None,
                             self._board[y][x+1] if x+1 < self._size else None,
                             self._board[y+1][x] if y+1 < self._size else None,
                             self._board[y][x-1] if x-1 >= 0 else None]
                self._board[y][x].place(neighbors)
        self.set_options(cubes)
        self._frame = [c for c in self._cells if c.zeros() > 0]
        self._inner = [c for c in self._cells if c not in self._frame]

    def set_options(self, cubes):
        corners = [c for c in cubes if c.zeros() == 2]
        frame = [c for c in cubes if c.zeros() == 1]
        inner = [c for c in cubes if c.zeros() == 0]

        for y in range(self._size):
            for x in range(self._size):
                if (y == 0 or y == self._size-1) and (x == 0 or x == self._size-1):
                    self._board[y][x].set_options(corners)
                elif (y == 0 or y == self._size-1) or (x == 0 or x == self._size-1):
                    self._board[y][x].set_options(frame)
                else:
                    self._board[y][x].set_options(inner)

    def __str__(self):
        s = ''
        for l in self._board:
            for cell in l:
                s += '[%s], ' % str(cell.get_cube())
            s += '\n'
        return s

    def show(self):
        s = ''
        for c in self._cells:
            s += '%s; ' % c.get_cube().show()
        return s

    def show1(self):
        s = ''
        for c in self._cells:
            s += '%s ' % (c.get_cube().show1() if c.get_cube() else 'N')
        return s

    def check(self, full):
        collection = self._cells if full else self._frame
        for c in collection:
            if c.get_cube() is None:
                return False
        sys.stdout.write('\n' + self.show1())
        sys.stdout.flush()
        for c in range(len(collection)):
            r = self._cells[c].check_match() if full else self._cells[c].check_match_frame(True)
            if not r:
                return False
        return True

    def solve(self, i, full):
        if full:
            for c in range(i, len(self._inner)):
                while self._inner[c].try_next():
                    if self.solve(c+1, True) or self.check(True):
                        return True
                self._inner[c].clear()
        else:
            for c in range(i, len(self._frame)):
                while self._frame[c].try_next():
                    if self.solve(c+1, False) or self.check(False):
                        return True
            if self.check(False):
                if self.solve(0, True):
                    return True
        return False


def main():
    cubes = []
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = f.read().replace('\n', '')
    else:
        data = test1

    for cube in data.rstrip().split(';'):
        if cube:
            cubes.append(Cube(cube))

    board = Board(cubes)
    if board.solve(0, False):
        print('DONE!')
        print(board.show()[:-2])
    else:
        print('Failed')


if __name__ == '__main__':
    main()