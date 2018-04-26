class PlayingObject:
    """
Общий абстрактный класс объектов поля
object_code - код объекта, позволяющий переопределить равенство объектов и их хэширование.
Код для каждого объекта уникален
    """

    object_code = 0

    def __init__(self):
        pass

    def __eq__(self, other):
        return self.object_code == other.object_code

    def __hash__(self):
        return self.object_code

    def update_cell(self, life, i, j):
        """
        Функция поведения объекта при изменении состояния поля, переопределённая в каждом из потомков
        :param life: текущая игра, в которой содержится объект
        :param i: х-координата объекта
        :param j: у-координата объекта
        :return: новый объект клетки типа, наследуемого от PlayingObject
        """
        pass


class Rock(PlayingObject):
    """
Класс ячейки со скалами
    """
    object_code = 1

    def update_cell(self, life, i, j):
        return Rock()  # Возвращаемый объект


class Fish(PlayingObject):
    """
Класс ячейки с рыбой
    """
    object_code = 2

    def update_cell(self, life, i, j):
        if life.count_neighbours(i, j, 'f') > 3 or life.count_neighbours(i, j, 'f') < 2:
            return Ocean()  # Возвращаемый объект
        else:
            return Fish()  # Возвращаемый объект


class Ocean(PlayingObject):
    """
Класс ячейки пустого океана
    """
    object_code = 0

    def update_cell(self, life, i, j):
        if life.count_neighbours(i, j, 'f') == 3:
            return Fish()  # Возвращаемый объект
        elif life.count_neighbours(i, j, 's') == 3:
            return Shrimp()  # Возвращаемый объект
        else:
            return Ocean()  # Возвращаемый объект


class Shrimp(PlayingObject):
    """
Класс ячейки с креветкой
    """
    object_code = 3

    def update_cell(self, life, i, j):
        if life.count_neighbours(i, j, 's') > 3 or life.count_neighbours(i, j, 's') < 2:
            return Ocean()  # Возвращаемый объект
        else:
            return Shrimp()  # Возвращаемый объект


class LifeGame(object):
    """
Класс игры
Метод задаётся высотой поля и длиной поля
    """

    def __init__(self, _height, _length):
        self.height = _height  # Высота игрового поля
        self.length = _length  # Длна строки игрового поля
        self.game_field = [[None]*self.length for i in range(self.height)]  # Игровое поле
        self.def_ocean = Ocean()  # Экземпляр объекта класса для составления словарей
        self.def_rock = Rock()  # Экземпляр объекта класса для составления словарей
        self.def_fish = Fish()  # Экземпляр объекта класса для составления словарей
        self.def_shrimp = Shrimp()  # Экземпляр объекта класса для составления словарей
        """
Словари для преобразования символа поля в класс объекта, заданного этим символом, и обратно
        """
        self.dictSymbol_to_object = {'n': self.def_ocean, 'r': self.def_rock, 'f': self.def_fish, 's': self.def_shrimp}
        self.dictObject_to_symbol = {self.def_ocean: 'n', self.def_rock: 'r', self.def_fish: 'f', self.def_shrimp: 's'}

    def full_field(self, x, string_of_field):
        """
        Заполнение массива поля игры
        :param x: номер строки
        :param string_of_field: содежрание строки
        """
        self.game_field[x] = string_of_field

    def get_cell(self, x, y):
        """
        Возвращает значение игровой клетки
        :param x: х-координата клетки
        :param y: у-координата клетки
        :return: символ - игровой объект в ячейке
        """
        return self.game_field[x][y]

    def _is_field_cell_exist(self, x, y):
        """
        Проверка существования ячейки с данными координатами
        :param x: х-координата клетки
        :param y: у-координата клетки
        :return: True, если клетка игрового поля существует,
                 False, если клетка находится за границами игрового поля
        """
        return 0 <= x < self.height and 0 <= y < self.length

    def count_neighbours(self, x, y, obj):
        """
        Подсчёт соседей того же типа, что и объект в данной ячейке
        :param x: х-координата клетки
        :param y: у-координата клетки
        :param obj: игровой объект, находящийся в данной ячейке
        :return: количество соседей данного типа объектов
        """
        number_of_neighbours = 0  # Количество соседей одного вида с объектом в клетке
        for x_inc in range(-1, 2):
            for y_inc in range(-1, 2):
                if not(x_inc == 0 and y_inc == 0):
                    if self._is_field_cell_exist(x + x_inc, y + y_inc) and self.game_field[x + x_inc][y + y_inc] == obj:
                        number_of_neighbours += 1
        return number_of_neighbours

    def next_game_state(self):
        """
        Переход к следующему состоянию океана
        В результате обновляется состояние игрового поля
        """
        next_state_game_field = [[None]*self.length for l in range(self.height)]  # Результат новой итерации игры
        for i in range(self.height):
            for j in range(self.length):
                obj = self.dictSymbol_to_object[self.game_field[i][j]]  # Объект, находящийся в клетке, расшифрованный по словарю
                next_state_game_field[i][j] = self.dictObject_to_symbol[obj.update_cell(self, i, j)]
        self.game_field = next_state_game_field

    def play(self, steps):
        """
        Запуск игры на определённое количество итераций
        :param steps: количество игровых итераций
        :return: обновляется состояние игры
        """
        for i in range(steps):
            self.next_game_state()
