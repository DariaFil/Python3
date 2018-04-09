import sys

class CLifegame(object):
    def __init__(self):
        self.height = 0
        self.length = 0
        self.steps = 0
        self.arr = []

    def set_game(self, height, length, steps):
        self.height = height
        self.length = length
        self.steps = steps
        self.arr = [[None]*length for i in range(height)]

    def full(self, i, d):
        self.arr[i] = d

    def exist(self, i, j):
        if 0 <= i < self.height and 0 <= j < self.length:
            return True
        else:
            return False

    def count(self, i, j, d):
        c = 0
        for i_inc in range(-1, 2):
            for j_inc in range(-1, 2):
                if not(i_inc == 0 and j_inc == 0):
                    if self.exist(i + i_inc, j + j_inc) and self.arr[i + i_inc][j + j_inc] == d:
                        c += 1
        return c

    def ocean_behavior(self, i, j):
        if self.count(i, j, 'f') == 3:
            return 'f'
        elif self.count(i, j, 's') == 3:
            return 's'
        else:
            return self.arr[i][j]

    def rock_behavior(self, i, j):
        return self.arr[i][j]

    def fish_behavior(self, i, j):
        if self.count(i, j, 'f') > 3 or self.count(i, j, 'f') < 2:
            return 'n'
        else:
            return self.arr[i][j]

    def shrimp_behavior(self, i, j):
        if self.count(i, j, 's') > 3 or self.count(i, j, 's') < 2:
            return 'n'
        else:
            return self.arr[i][j]

    def next(self):
        arr2 = [[None]*self.length for l in range(self.height)]
        for i in range(self.height):
            for j in range(self.length):
                if self.arr[i][j] == 'n':
                    arr2[i][j] = self.ocean_behavior(i, j)
                elif self.arr[i][j] == 'f':
                    arr2[i][j] = self.fish_behavior(i, j)
                elif self.arr[i][j] == 's':
                    arr2[i][j] = self.shrimp_behavior(i, j)
                elif self.arr[i][j] == 'r':
                    arr2[i][j] = self.rock_behavior(i, j)
        self.arr = arr2
    arr = []
    height = 0
    length = 0
    steps = 0


class Rock:
    pass


class Fish:
    pass


class Ocean:
    pass


class Shrimp:
    pass


def input(ans):
    f = sys.stdin
    if ans == "file":
        f = open('input.txt', 'r')
    l = []
    i = -1
    cgame = CLifegame()
    for line in f:
        if i == -1:
            l = list(line.split())
            cgame.set_game(int(l[0]), int(l[1]), int(l[2]))
            i += 1
        else:
            l = list(line)
            cgame.full(i, l)
            i += 1
    if ans == "file":
        f.close()
    return cgame


def output(ans, cgame):
    f = sys.stdout
    if ans == "file":
        f = open('output.txt', 'w')
    for i in range(cgame.height):
        for j in range(cgame.length):
            f.write(cgame.arr[i][j])
        f.write('\n')
    if ans == "file":
        f.close()


def run(ans):
    game = input(ans)
    for i1 in range(game.steps):
        game.next()
    output(ans, game)
