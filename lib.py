'''Общий абстрактный класс объектов поля'''
class Object:
    def __init__(self):
        pass

    def __eq__(self, other):
        if self.object_code() == other.object_code():
            return True
        else:
            return False

    def __hash__(self):
        return self.object_code()

    '''Возвращние кода объекта, позволяющее переопределить равенство объектов и их хэширование.
        Код для каждого объекта уникален, метод переопределён в каждом из потомков'''
    def object_code(self):
        pass

    '''Функция поведения объекта при изменении состояния поля, переопределённая в каждом из потомков'''
    def update_cell(self, life, i, j):
        pass


'''Класс ячейки со скалами'''
class Rock(Object):
    def object_code(self):
        return 1

    def update_cell(self, life, i, j):
        rock = Rock()
        return rock


'''Класс ячейки с рыбой'''
class Fish(Object):
    def object_code(self):
        return 2

    def update_cell(self, life, i, j):
        if life.count_neighbors(i, j, 'f') > 3 or life.count_neighbors(i, j, 'f') < 2:
            ocean = Ocean()
            return ocean
        else:
            fish = Fish()
            return fish


'''Класс ячейки пустого океана'''
class Ocean(Object):
    def object_code(self):
        return 0

    def update_cell(self, life, i, j):
        if life.count_neighbors(i, j, 'f') == 3:
            fish = Fish()
            return fish
        elif life.count_neighbors(i, j, 's') == 3:
            shrimp = Shrimp()
            return shrimp
        else:
            ocean = Ocean()
            return ocean


'''Класс ячейки с креветкой'''
class Shrimp(Object):
    def object_code(self):
        return 3

    def update_cell(self, life, i, j):
        if life.count_neighbors(i, j, 's') > 3 or life.count_neighbors(i, j, 's') < 2:
            ocean = Ocean()
            return ocean
        else:
            shrimp = Shrimp()
            return shrimp


class CLifegame(object):
    def __init__(self, _height, _length):
        self.height = _height
        self.length = _length
        self.arr = [[None]*self.length for i in range(self.height)]
        self.def_ocean = Ocean()
        self.def_rock = Rock()
        self.def_fish = Fish()
        self.def_shrimp = Shrimp()
        '''Словари для преобразования символа поля в класс объекта, заданного этим символом, и обратно'''
        self.dictSymbol_to_object = {"n": self.def_ocean, "r": self.def_rock, "f": self.def_fish, "s": self.def_shrimp}
        self.dictObject_to_symbol = {self.def_ocean: "n", self.def_rock: "r", self.def_fish: "f", self.def_shrimp: "s"}

    '''Заполнение масиива поля игры'''
    def full_field(self, x, string_of_field):
        self.arr[x] = string_of_field

    def get_cell(self, x, y):
        return self.arr[x][y]

    '''Проверка существования ячейки с данными координатами'''
    def is_field_cell_exist(self, x, y):
        if 0 <= x < self.height and 0 <= y < self.length:
            return True
        else:
            return False

    '''Подсчёт соседей того же типа, что и объект в данной ячейке'''
    def count_neighbors(self, x, y, obj):
        c = 0
        for x_inc in range(-1, 2):
            for y_inc in range(-1, 2):
                if not(x_inc == 0 and y_inc == 0):
                    if self.is_field_cell_exist(x + x_inc, y + y_inc) and self.arr[x + x_inc][y + y_inc] == obj:
                        c += 1
        return c

    '''Переход к следующему состоянию океана'''
    def next_game_state(self):
        next_state_arr = [[None]*self.length for l in range(self.height)]
        for i in range(self.height):
            for j in range(self.length):
                obj = self.dictSymbol_to_object[self.arr[i][j]]
                next_state_arr[i][j] = self.dictObject_to_symbol[obj.update(self, i, j)]

        self.arr = next_state_arr

    '''Запуск игры'''
    def play(self, steps):
        for i in range(steps):
            self.next_game_state()
