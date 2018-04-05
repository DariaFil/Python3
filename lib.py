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

    def sham_behavior(self, i, j):
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
                    arr2[i][j] = self.sham_behavior(i, j)
                elif self.arr[i][j] == 'r':
                    arr2[i][j] = self.rock_behavior(i, j)
        self.arr = arr2
    arr = []
    height = 0
    length = 0
    steps = 0


def console_input():
    l = list(input().split())
    cgame = CLifegame()
    cgame.set_game(int(l[0]), int(l[1]), int(l[2]))
    for i in range(cgame.height):
        l = list(input())
        cgame.full(i, l)
    return cgame


def console_output(cgame):
    for i in range(cgame.height):
        for j in range(cgame.length):
            print(cgame.arr[i][j], end='')
        print()


def file_input():
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
    f.close()
    return cgame


def file_output(cgame):
    f = open('output.txt', 'w')
    for i in range(cgame.height):
        for j in range(cgame.length):
            f.write(cgame.arr[i][j])
        f.write('\n')


def run():
    game = console_input()
    for i1 in range(game.steps):
        game.next()
    console_output(game)


def file_run():
    game = file_input()
    for i1 in range(game.steps):
        game.next()
    file_output(game)
