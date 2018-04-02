class CLifegame(object):
    def __init__(self):
        self.n = 0
        self.m = 0
        self.k = 0
        self.arr = []

    def set_game(self, n, m, k):
        self.n = n
        self.m = m
        self.k = k
        self.arr = [[None]*m for i in range(n)]

    def full(self, i, d):
        self.arr[i] = d

    def count(self, i, j, d):
        c = 0
        if i > 0:
            if self.arr[i - 1][j] == d:
                c += 1
            if j > 0 and self.arr[i - 1][j - 1] == d:
                c += 1
            if j < self.m - 1 and self.arr[i - 1][j + 1] == d:
                c += 1
        if i < self.n - 1:
            if self.arr[i + 1][j] == d:
                c += 1
            if j > 0 and self.arr[i + 1][j - 1] == d:
                c += 1
            if j < self.m - 1 and self.arr[i + 1][j + 1] == d:
                c += 1
        if j > 0 and self.arr[i][j - 1] == d:
            c += 1
        if j < self.m - 1 and self.arr[i][j + 1] == d:
            c += 1
        return c

    def next(self):
        arr2 = [[None]*self.m for l in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                if self.arr[i][j] == 'n':
                    if self.count(i, j, 'f') == 3:
                        arr2[i][j] = 'f'
                    elif self.count(i, j, 's') == 3:
                        arr2[i][j] = 's'
                    else:
                        arr2[i][j] = self.arr[i][j]
                elif self.arr[i][j] == 'f':
                    if self.count(i, j, 'f') > 3 or self.count(i, j, 'f') < 2:
                        arr2[i][j] = 'n'
                    else:
                        arr2[i][j] = self.arr[i][j]
                elif self.arr[i][j] == 's':
                    if self.count(i, j, 's') > 3 or self.count(i, j, 's') < 2:
                        arr2[i][j] = 'n'
                    else:
                        arr2[i][j] = self.arr[i][j]
                else:
                    arr2[i][j] = self.arr[i][j]
        self.arr = arr2
    arr = []
    n = 0
    m = 0
    k = 0


def console_input():
    l = list(input().split())
    cgame = CLifegame()
    cgame.set_game(int(l[0]), int(l[1]), int(l[2]))
    for i in range(cgame.n):
        l = list(input())
        cgame.full(i, l)
    return cgame


def console_output(cgame):
    for i in range(cgame.n):
        for j in range(cgame.m):
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
    for i in range(cgame.n):
        for j in range(cgame.m):
            f.write(cgame.arr[i][j])
        f.write('\n')


def run():
    game = console_input()
    for i1 in range(game.k):
        game.next()
    console_output(game)


def file_run():
    game = file_input()
    for i1 in range(game.k):
        game.next()
    file_output(game)
