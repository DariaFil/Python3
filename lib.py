import sys


'''Общий абстрактный класс объектов поля'''
class Object:
    def __init__(self):
        pass

    def __eq__(self, other):
        if self.code() == other.code():
            return True
        else:
            return False

    def __hash__(self):
        return self.code()

    '''Возвращние кода объекта, позволяющее переопределить равенство объектов и их хэширование.
        Код для каждого объекта уникален, метод переопределён в каждом из потомков'''
    def code(self):
        pass

    '''Функция поведения объекта при изменении состояния поля, переопределённая в каждом из потомков'''
    def update(self, life, i, j):
        pass


'''Класс ячейки со скалами'''
class Rock(Object):
    def code(self):
        return 1

    def update(self, life, i, j):
        rock = Rock()
        return rock


'''Класс ячейки с рыбой'''
class Fish(Object):
    def code(self):
        return 2

    def update(self, life, i, j):
        if life.count(i, j, 'f') > 3 or life.count(i, j, 'f') < 2:
            ocean = Ocean()
            return ocean
        else:
            fish = Fish()
            return fish


'''Класс ячейки пустого океана'''
class Ocean(Object):
    def code(self):
        return 0

    def update(self, life, i, j):
        if life.count(i, j, 'f') == 3:
            fish = Fish()
            return fish
        elif life.count(i, j, 's') == 3:
            shrimp = Shrimp()
            return shrimp
        else:
            ocean = Ocean()
            return ocean


'''Класс ячейки с креветкой'''
class Shrimp(Object):
    def code(self):
        return 3

    def update(self, life, i, j):
        if life.count(i, j, 's') > 3 or life.count(i, j, 's') < 2:
            ocean = Ocean()
            return ocean
        else:
            shrimp = Shrimp()
            return shrimp


class CLifegame(object):
    def __init__(self):
        self.height = 0
        self.length = 0
        self.steps = 0
        self.arr = []
        self.def_ocean = Ocean()
        self.def_rock = Rock()
        self.def_fish = Fish()
        self.def_shrimp = Shrimp()
        '''Словари для преобразования символа поля в класс объекта, заданного этим символом, и обратно'''
        self.diction = {"n": self.def_ocean, "r": self.def_rock, "f": self.def_fish, "s": self.def_shrimp}
        self.undiction = {self.def_ocean: "n", self.def_rock: "r", self.def_fish: "f", self.def_shrimp: "s"}

    '''Инициация параметорв поля'''
    def set_game(self, height, length, steps):
        self.height = height
        self.length = length
        self.steps = steps
        self.arr = [[None]*length for i in range(height)]

    '''Заполнение масиива поля игры'''
    def full(self, i, d):
        self.arr[i] = d

    '''Проверка существования ячейки с данными координатами'''
    def exist(self, i, j):
        if 0 <= i < self.height and 0 <= j < self.length:
            return True
        else:
            return False

    '''Подсчёт соседей того же типа, что и объект в данной ячейке'''
    def count(self, i, j, d):
        c = 0
        for i_inc in range(-1, 2):
            for j_inc in range(-1, 2):
                if not(i_inc == 0 and j_inc == 0):
                    if self.exist(i + i_inc, j + j_inc) and self.arr[i + i_inc][j + j_inc] == d:
                        c += 1
        return c

    '''Переход к следующему состоянию океана'''
    def next(self):
        arr2 = [[None]*self.length for l in range(self.height)]
        for i in range(self.height):
            for j in range(self.length):
                obj = self.diction[self.arr[i][j]]
                arr2[i][j] = self.undiction[obj.update(self, i, j)]

        self.arr = arr2


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
