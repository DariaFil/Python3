class PlayingObject:
    """
Общий абстрактный класс объектов поля
object_code - код объекта, позволяющий переопределить равенство объектов и их хэширование.
Код для каждого объекта уникален
    """

    symbol = ''

    def __init__(self):
        pass

    def __eq__(self, other):
        return self.symbol == other.symbol

    def update_cell(self, game, x, y):
        """
        Функция поведения объекта при изменении состояния поля, переопределённая в каждом из потомков
        :param game: Игра, из которой взят объект
        :param x: х-координата объекта на поле игры
        :param y: у-координата объекта на поле игры
        :return: объект, получившийся после обновления ячейки
        """
        pass


class Ocean(PlayingObject):
    """
Класс ячейки пустого океана
    """
    symbol = "n"

    def update_cell(self, game, x, y):
        neighbours = game.return_neighbours(x, y)  # Массив объектов-соседей
        fish_count = 0  # Количество рыб среди соседей
        shrimp_count = 0  # Количество креветок среди соседей
        for i in neighbours:
            if i == Fish():
                fish_count += 1
            elif i == Shrimp:
                shrimp_count += 1
        if fish_count == 3:
            return Fish()
        elif shrimp_count == 3:
            return Shrimp()
        else:
            return Ocean()


class Rock(PlayingObject):
    """
Класс ячейки со скалами
    """
    symbol = "r"

    def update_cell(self, game, x, y):
        return Rock()


class Fish(PlayingObject):
    """
Класс ячейки с рыбой
    """
    symbol = "f"

    def update_cell(self, game, x, y):
        neighbours = game.return_neighbours(x, y)  # Массив объектов-соседей
        fish_count = 0  # Количество рыб среди соседей
        for i in neighbours:
            if i == Fish():
                fish_count += 1
        if 1 < fish_count < 4:
            return Fish()
        else:
            return Ocean()


class Shrimp(PlayingObject):
    """
Класс ячейки с креветкой
    """
    symbol = "s"

    def update_cell(self, game, x, y):
        neighbours = game.return_neighbours(x, y)  # Массив объектов-соседей
        shrimp_count = 0  # Количество креветок среди соседей
        for i in neighbours:
            if i == Shrimp():
                shrimp_count += 1
        if 1 < shrimp_count < 4:
            return Shrimp()
        else:
            return Ocean()


class Factory:
    """
    Фабрика игровых объектов
    Метод __init__ инициирует массив игровых объектов - потомков PlayingObject
    """
    def __init__(self):
        self.object_list = PlayingObject.__subclasses__()  # Массив слабых ссылок на все типы игровых объектов

    def get_object(self, symbol):
        """
        Возвращает объект по его символу
        :param symbol: символ объекта
        :return: игровой объект
        """
        i = 0
        while self.object_list[i].symbol != symbol:
            i += 1
        return self.object_list[i]()


class LifeGame:
    """
Класс игры
Метод __init__ задаётся высотой поля и длиной поля и инициирует, помимо
параметров, поле игры в незаполненном варианте
    """
    def __init__(self, _height, _length):
        self.height = _height  # Высота игрового поля
        self.length = _length  # Длна строки игрового поля
        self.game_field = [[PlayingObject]*self.length for i in range(self.height)]  # Игровое поле

    def full_field(self, x, string_of_field):
        """
        Заполнение массива поля игры
        :param x: номер строки
        :param string_of_field: содежрание строки
        """
        factory = Factory()
        for i in range(len(string_of_field)):
            self.game_field[x][i] = factory.get_object(string_of_field[i])

    def get_cell(self, x, y):
        """
        Возвращает значение игровой клетки
        :param x: х-координата клетки
        :param y: у-координата клетки
        :return: символ - игровой объект в ячейке
        """
        return self.game_field[x][y].symbol

    def __is_field_cell_exist(self, x, y):
        """
        Проверка существования ячейки с данными координатами
        :param x: х-координата клетки
        :param y: у-координата клетки
        :return: True, если клетка игрового поля существует,
                 False, если клетка находится за границами игрового поля
        """
        return 0 <= x < self.height and 0 <= y < self.length

    def return_neighbours(self, x, y):
        """
        Подсчёт соседей того же типа, что и объект в данной ячейке
        :param x: х-координата клетки
        :param y: у-координата клетки
        :return: количество соседей данного типа объектов
        """
        neighbours_counts = []  # Массив соседей-объектов
        for x_inc in range(-1, 2):
            for y_inc in range(-1, 2):
                if not(x_inc == 0 and y_inc == 0):
                    if self.__is_field_cell_exist(x + x_inc, y + y_inc):
                        neighbours_counts.append(self.game_field[x + x_inc][y + y_inc])
        return neighbours_counts

    def __next_game_state(self):
        """
        Переход к следующему состоянию океана
        В результате обновляется состояние игрового поля
        """
        next_state_game_field = [[PlayingObject]*self.length for l in range(self.height)]  # Результат новой итерации игры
        for i in range(self.height):
            for j in range(self.length):
                next_state_game_field[i][j] = self.game_field[i][j].update_cell(self, i, j)  # Новый объект в текущей ячейке
        self.game_field = next_state_game_field

    def play(self, steps):
        """
        Запуск игры на определённое количество итераций
        :param steps: количество игровых итераций
        :return: обновляется состояние игры
        """
        for i in range(steps):
            self.__next_game_state()
