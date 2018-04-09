import lib


def test_init_and_full1():
    g = lib.CLifegame()
    g.set_game(1, 2, 1)
    a = ["f", "f"]
    g.full(0, a)
    assert (g.height == 1 and g.length == 2 and g.steps == 1)
    assert g.arr == [["f", "f"]]


def test_init_and_full2():
    g = lib.CLifegame()
    g.set_game(2, 3, 1)
    a1 = ["f", "f", "f"]
    a2 = ["n", "f", "n"]
    g.full(0, a1)
    g.full(1, a2)
    assert (g.height == 2 and g.length == 3 and g.steps == 1)
    assert g.arr == [["f", "f", "f"], ["n", "f", "n"]]


def test_count1():
    g = lib.CLifegame()
    g.set_game(2, 3, 1)
    a = [[None]*3 for i in range(2)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    for i in range(2):
        g.full(i, a[i])
    b = [[None]*3 for i in range(2)]
    for i in range(2):
        for j in range(3):
            b[i][j] = g.count(i, j, "f")
    assert b == [[2, 3, 2], [3, 3, 3]]


def test_count2():
    g = lib.CLifegame()
    g.set_game(3, 4, 1)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full(i, a[i])
    b = [[None]*4 for i in range(3)]
    for i in range(3):
        for j in range(4):
            b[i][j] = g.count(i, j, "f")
    assert b == [[2, 2, 3, 0], [4, 3, 3, 1], [1, 2, 1, 0]]
    for i in range(3):
        for j in range(4):
            b[i][j] = g.count(i, j, "s")
    assert b == [[0, 0, 1, 1], [1, 2, 4, 2], [1, 1, 3, 2]]


def test_count3():
    g = lib.CLifegame()
    g.set_game(3, 3, 2)
    a = [[None]*3 for i in range(3)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    a[2] = ["s", "s", "s"]
    for i in range(3):
        g.full(i, a[i])
    b = [[None]*3 for i in range(3)]
    for i in range(3):
        for j in range(3):
            b[i][j] = g.count(i, j, "f")
    assert b == [[2, 3, 2], [3, 3, 3], [1, 1, 1]]
    for i in range(3):
        for j in range(3):
            b[i][j] = g.count(i, j, "s")
    assert b == [[0, 0, 0], [2, 3, 2], [1, 2, 1]]


def test_objects_update1():
    g = lib.CLifegame()
    g.set_game(3, 4, 1)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full(i, a[i])
    fish = lib.Fish()
    ocean = lib.Ocean()
    shrimp = lib.Shrimp()
    rock = lib.Rock()
    assert rock.update(g, 0, 2) == rock
    assert ocean.update(g, 1, 0) == ocean
    assert ocean.update(g, 1, 2) == fish
    assert fish.update(g, 0, 3) == ocean
    assert fish.update(g, 0, 0) == fish
    assert shrimp.update(g, 2, 2) == shrimp
    assert shrimp.update(g, 2, 1) == ocean


def test_objects_update2():
    g = lib.CLifegame()
    g.set_game(3, 3, 2)
    a = [[None]*3 for i in range(3)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    a[2] = ["s", "s", "s"]
    for i in range(3):
        g.full(i, a[i])
    fish = lib.Fish()
    ocean = lib.Ocean()
    shrimp = lib.Shrimp()
    assert ocean.update(g, 1, 0) == fish
    assert fish.update(g, 0, 2) == fish
    assert fish.update(g, 0, 1) == fish
    assert shrimp.update(g, 2, 2) == ocean
    assert shrimp.update(g, 2, 1) == shrimp


def test_next1():
    g = lib.CLifegame()
    g.set_game(2, 3, 1)
    a = [[None]*3 for i in range(2)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    for i in range(2):
        g.full(i, a[i])
    g.next()
    assert g.arr == [["f", "f", "f"], ["f", "f", "f"]]
    g.next()
    assert g.arr == [["f", "n", "f"], ["f", "n", "f"]]


def test_next2():
    g = lib.CLifegame()
    g.set_game(3, 4, 1)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full(i, a[i])
    g.next()
    assert g.arr == [["f", "f", "r", "n"], ["n", "f", "f", "s"], ["n", "n", "s", "s"]]


def test_next3():
    g = lib.CLifegame()
    g.set_game(3, 3, 2)
    a = [[None]*3 for i in range(3)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    a[2] = ["s", "s", "s"]
    for i in range(3):
        g.full(i, a[i])
    g.next()
    g.next()
    assert g.arr == [["f", "n", "f"], ["f", "n", "f"], ["n", "n", "n"]]


def test():
    test_init_and_full1()
    test_init_and_full2()
    test_count1()
    test_count2()
    test_count3()
    test_objects_update1()
    test_objects_update2()
    test_next1()
    test_next2()
    test_next3()
