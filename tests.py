import lib


def test_init_and_full1():
    """
    Тестирование инициации и заполнения массива поля, тест 1
    """
    g = lib.LifeGame(1, 2)
    a = ["f", "f"]
    g.full_field(0, a)
    assert (g.height == 1 and g.length == 2), "Init1 not passed"
    assert g.game_field == [[lib.Fish(), lib.Fish()]], "full_field1 not passed"


def test_init_and_full():
    """
    Тестирование инициации и заполнения массива поля, тест 2
    """
    g = lib.LifeGame(2, 3)
    a1 = ["f", "f", "f"]
    a2 = ["n", "f", "n"]
    g.full_field(0, a1)
    g.full_field(1, a2)
    assert (g.height == 2 and g.length == 3), "Init2 not passed"
    assert g.game_field == [[lib.Fish(), lib.Fish(), lib.Fish()], [lib.Ocean(), lib.Fish(), lib.Ocean()]], "full_field2 not passed"


def test_return_neighbours1():
    """
    Тестирование функции подсчёта соседей, тест 1
    """
    g = lib.LifeGame(2, 3)
    a = [[], []]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    for i in range(2):
        g.full_field(i, a[i])
    b = [[], []]
    for i in range(2):
            b[i] = g.return_neighbours(i, 0)
    assert b == [[ lib.Fish(), lib.Ocean(), lib.Fish()], [lib.Fish(), lib.Fish(), lib.Fish()]], "return_neighbours1_1 not passed"
    for i in range(2):
            b[i] = g.return_neighbours(i, 1)
    assert b == [[lib.Fish(), lib.Fish(), lib.Ocean(), lib.Fish(), lib.Ocean()],
                 [lib.Fish(), lib.Fish(), lib.Fish(), lib.Ocean(), lib.Ocean()]], "return_neighbours1_2 not passed"
    for i in range(2):
            b[i] = g.return_neighbours(i, 2)
    assert b == [[lib.Fish(), lib.Fish(), lib.Ocean()], [lib.Fish(), lib.Fish(), lib.Fish()]], "return_neighbours1_3 not passed"


def test_return_neighbours2():
    """
    Тестирование функции подсчёта соседей, тест 2
    """
    g = lib.LifeGame(3, 4)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    b = [[], [], [], []]
    for j in range(4):
        b[j] = g.return_neighbours(0, j)
    assert b == [[lib.Fish(), lib.Ocean(), lib.Fish()],
                  [lib.Fish(), lib.Rock(), lib.Ocean(), lib.Fish(), lib.Ocean()],
                  [lib.Fish(), lib.Fish(), lib.Fish(), lib.Ocean(), lib.Shrimp()],
                  [lib.Rock(), lib.Ocean(), lib.Shrimp()]], "count_neighbours2_1 not passed"
    for j in range(4):
        b[j] = g.return_neighbours(1, j)
    assert b == [[lib.Fish(), lib.Fish(), lib.Fish(), lib.Fish(), lib.Shrimp()],
                  [lib.Fish(), lib.Fish(), lib.Rock(), lib.Ocean(), lib.Ocean(), lib.Fish(), lib.Shrimp(), lib.Shrimp()],
                  [lib.Fish(), lib.Rock(), lib.Fish(), lib.Fish(), lib.Shrimp(), lib.Shrimp(), lib.Shrimp(), lib.Shrimp()],
                  [lib.Rock(), lib.Fish(), lib.Ocean(), lib.Shrimp(), lib.Shrimp()]], "count_neighbours2_2 not passed"
    for j in range(4):
        b[j] = g.return_neighbours(2, j)
    assert b == [[lib.Ocean(), lib.Fish(), lib.Shrimp()],
                  [lib.Ocean(), lib.Fish(), lib.Ocean(), lib.Fish(), lib.Shrimp()],
                  [lib.Fish(), lib.Ocean(), lib.Shrimp(), lib.Shrimp(), lib.Shrimp()],
                  [lib.Ocean(), lib.Shrimp(), lib.Shrimp()]], "count_neighbours2_3 not passed"


def test_objects_update_cell1():
    """
    Тестирование функции объектов поля: обновление яцейки при новой игровой итерации, тест 1
    """
    g = lib.LifeGame(3, 4)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    fish = lib.Fish()
    ocean = lib.Ocean()
    shrimp = lib.Shrimp()
    rock = lib.Rock()
    assert rock.update_cell(g, 0, 2) == rock, "update_cell_rock not passed"
    assert ocean.update_cell(g, 1, 0) == ocean, "update_cell_ocean1_1 not passed"
    assert ocean.update_cell(g, 1, 2) == fish, "update_cell_ocean1_2 not passed"
    assert fish.update_cell(g, 0, 3) == ocean, "update_cell_fish1_1 not passed"
    assert fish.update_cell(g, 0, 0) == fish, "update_cell_fish1_2 not passed"
    assert shrimp.update_cell(g, 2, 2) == shrimp, "update_cell_shrimp1_1 not passed"
    assert shrimp.update_cell(g, 2, 1) == ocean, "update_cell_shrimp1_2 not passed"


def test_objects_update_cell2():
    """
    Тестирование функции объектов поля: обновление яцейки при новой игровой итерации, тест 2
    """
    g = lib.LifeGame(3, 3)
    a = [[None]*3 for i in range(3)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    a[2] = ["s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    fish = lib.Fish()
    ocean = lib.Ocean()
    shrimp = lib.Shrimp()
    assert ocean.update_cell(g, 1, 0) == fish, "update_cell_ocean2_1 not passed"
    assert fish.update_cell(g, 0, 2) == fish, "update_cell_fish2_1 not passed"
    assert fish.update_cell(g, 0, 1) == fish, "update_cell_fish2_2 not passed"
    assert shrimp.update_cell(g, 2, 2) == ocean, "update_cell_shrimp2_1 not passed"
    assert shrimp.update_cell(g, 2, 1) == shrimp, "update_cell_shrimp2_2 not passed"


def test_next1():
    """
    Тестирование поведения игры при переходе в очередное состояние, тест 1
    """
    g = lib.LifeGame(2, 3)
    a = [[None]*3 for i in range(2)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    for i in range(2):
        g.full_field(i, a[i])
    g.play(1)
    for i in range(2):
            for j in range(3):
                a[i][j] = g.get_cell(i, j)
    assert a == [["f", "f", "f"], ["f", "f", "f"]], "Next1_1 not passed"
    g.play(1)
    for i in range(2):
            for j in range(3):
                a[i][j] = g.get_cell(i, j)
    assert a == [["f", "n", "f"], ["f", "n", "f"]], "Next1_2 not passed"


def test_next2():
    """
    Тестирование поведения игры при переходе в очередное состояние, тест 2
    """
    g = lib.LifeGame(3, 4)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    g.play(1)
    for i in range(3):
            for j in range(4):
                a[i][j] = g.get_cell(i, j)
    assert a == [["f", "f", "r", "n"], ["n", "f", "f", "s"], ["n", "n", "s", "s"]], "Next2 not passed"


def test_next3():
    """
    Тестирование поведения игры при переходе в очередное состояние, тест 3
    """
    g = lib.LifeGame(3, 3)
    a = [[None]*3 for i in range(3)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    a[2] = ["s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    g.play(2)
    for i in range(3):
            for j in range(3):
                a[i][j] = g.get_cell(i, j)
    assert a == [["f", "n", "f"], ["f", "n", "f"], ["n", "n", "n"]], "Next3 not passed"


def test_factory():
    fact = lib.Factory()
    assert fact.get_object('f') == lib.Fish(), "Factory1 not passed"
    assert fact.get_object('n') == lib.Ocean(), "Factory2 not passed"
    assert fact.get_object('s') == lib.Shrimp(), "Factory3 not passed"
    assert fact.get_object('r') == lib.Rock(), "Factory4 not passed"


def test():
    """
    Воспроизведение всех тестов
    """
    test_init_and_full()
    test_init_and_full()
    test_return_neighbours1()
    test_return_neighbours2()
    test_objects_update_cell1()
    test_objects_update_cell2()
    test_next1()
    test_next2()
    test_next3()
    test_factory()
