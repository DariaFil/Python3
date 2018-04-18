'''Общий абстрактный класс объектов поля'''
class Playing_object:
    '''Код объекта, позволяющий переопределить равенство объектов и их хэширование.
        Код для каждого объекта уникален'''
    object_code = 0

    def __init__(self):
        pass

    def __eq__(self, other):
        if self.object_code == other.object_code:
            return True
        else:
            return False

    def __hash__(self):
        return self.object_code

    '''Функция поведения объекта при изменении состояния поля, переопределённая в каждом из потомков'''
    def update_cell(self, life, i, j):
        pass


'''Класс ячейки со скалами'''
class Rock(Playing_object):
    object_code = 1

    def update_cell(self, life, i, j):
        rock = Rock() #Возвращаемый объект
        return rock


'''Класс ячейки с рыбой'''
class Fish(Playing_object):
    object_code = 2

    def update_cell(self, life, i, j):
        if life.count_neighbours(i, j, 'f') > 3 or life.count_neighbours(i, j, 'f') < 2:
            ocean = Ocean() #Возвращаемый объект
            return ocean
        else:
            fish = Fish() #Возвращаемый объект
            return fish


'''Класс ячейки пустого океана'''
class Ocean(Playing_object):
    object_code = 0

    def update_cell(self, life, i, j):
        if life.count_neighbours(i, j, 'f') == 3:
            fish = Fish() #Возвращаемый объект
            return fish
        elif life.count_neighbours(i, j, 's') == 3:
            shrimp = Shrimp() #Возвращаемый объект
            return shrimp
        else:
            ocean = Ocean() #Возвращаемый объект
            return ocean


'''Класс ячейки с креветкой'''
class Shrimp(Playing_object):
    object_code = 3

    def update_cell(self, life, i, j):
        if life.count_neighbours(i, j, 's') > 3 or life.count_neighbours(i, j, 's') < 2:
            ocean = Ocean() #Возвращаемый объект
            return ocean
        else:
            shrimp = Shrimp() #Возвращаемый объект
            return shrimp


class CLifegame(object):
    def __init__(self, _height, _length):
        self.height = _height # Высота игрового поля
        self.length = _length #Длна строки игрового поля
        self.game_field = [[None]*self.length for i in range(self.height)] #Игровое поле
        self.def_ocean = Ocean() #Экземпляр объекта класса для составления словарей
        self.def_rock = Rock() #Экземпляр объекта класса для составления словарей
        self.def_fish = Fish() #Экземпляр объекта класса для составления словарей
        self.def_shrimp = Shrimp() #Экземпляр объекта класса для составления словарей
        '''Словари для преобразования символа поля в класс объекта, заданного этим символом, и обратно'''
        self.dictSymbol_to_object = {"n": self.def_ocean, "r": self.def_rock, "f": self.def_fish, "s": self.def_shrimp}
        self.dictObject_to_symbol = {self.def_ocean: "n", self.def_rock: "r", self.def_fish: "f", self.def_shrimp: "s"}

    '''Заполнение масиива поля игры'''
    def full_field(self, x, string_of_field): #Номер строки, содержание строки
        self.game_field[x] = string_of_field

    def get_cell(self, x, y): #
        return self.game_field[x][y]

    '''Проверка существования ячейки с данными координатами'''
    def is_field_cell_exist(self, x, y): #Координаты ячейки
        if 0 <= x < self.height and 0 <= y < self.length:
            return True
        else:
            return False

    '''Подсчёт соседей того же типа, что и объект в данной ячейке'''
    def count_neighbours(self, x, y, obj): #Координаты ячейка и объект, находящийся в ней
        number_of_neighbours = 0 #Количество соседей одного вида с объектом в клетке
        for x_inc in range(-1, 2):
            for y_inc in range(-1, 2):
                if not(x_inc == 0 and y_inc == 0):
                    if self.is_field_cell_exist(x + x_inc, y + y_inc) and self.game_field[x + x_inc][y + y_inc] == obj:
                        number_of_neighbours += 1
        return number_of_neighbours

    '''Переход к следующему состоянию океана'''
    def next_game_state(self):
        next_state_game_field = [[None]*self.length for l in range(self.height)] #Результат новой итерации игры
        for i in range(self.height):
            for j in range(self.length):
                obj = self.dictSymbol_to_object[self.game_field[i][j]] #Объект, находящийся в клетке, расшифрованный по словарю
                next_state_game_field[i][j] = self.dictObject_to_symbol[obj.update(self, i, j)]
        self.game_field = next_state_game_field

    '''Запуск игры '''
    def play(self, steps):
        for i in range(steps):
            self.next_game_state()
