import lib


def test_init_and_full1():
    g = lib.CLifegame(1, 2)
    a = ["f", "f"]
    g.full_field(0, a)
    assert (g.height == 1 and g.length == 2), "Init1 not passed"
    assert g.game_field == [["f", "f"]], "full_field1 not passed"


def test_init_and_full():
    g = lib.CLifegame(2, 3)
    a1 = ["f", "f", "f"]
    a2 = ["n", "f", "n"]
    g.full_field(0, a1)
    g.full_field(1, a2)
    assert (g.height == 2 and g.length == 3), "Init2 not passed"
    assert g.game_field == [["f", "f", "f"], ["n", "f", "n"]], "full_field2 not passed"


def test_count_neighbours1():
    g = lib.CLifegame(2, 3)
    a = [[None]*3 for i in range(2)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    for i in range(2):
        g.full_field(i, a[i])
    b = [[None]*3 for i in range(2)]
    for i in range(2):
        for j in range(3):
            b[i][j] = g.count_neighbours(i, j, "f")
    assert b == [[2, 3, 2], [3, 3, 3]], "count_neighbours1 not passed"


def test_count_neighbours2():
    g = lib.CLifegame(3, 4)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    b = [[None]*4 for i in range(3)]
    for i in range(3):
        for j in range(4):
            b[i][j] = g.count_neighbours(i, j, "f")
    assert b == [[2, 2, 3, 0], [4, 3, 3, 1], [1, 2, 1, 0]], "count_neighbours2_1 not passed"
    for i in range(3):
        for j in range(4):
            b[i][j] = g.count_neighbours(i, j, "s")
    assert b == [[0, 0, 1, 1], [1, 2, 4, 2], [1, 1, 3, 2]], "count_neighbours2_2 not passed"


def test_count_neighbours3():
    g = lib.CLifegame(3, 3)
    a = [[None]*3 for i in range(3)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    a[2] = ["s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    b = [[None]*3 for i in range(3)]
    for i in range(3):
        for j in range(3):
            b[i][j] = g.count_neighbours(i, j, "f")
    assert b == [[2, 3, 2], [3, 3, 3], [1, 1, 1]], "count_neighbours3_1 not passed"
    for i in range(3):
        for j in range(3):
            b[i][j] = g.count_neighbours(i, j, "s")
    assert b == [[0, 0, 0], [2, 3, 2], [1, 2, 1]], "count_neighbours3_2 not passed"


def test_objects_update_cell1():
    g = lib.CLifegame(3, 4)
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
    g = lib.CLifegame(3, 3)
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
    g = lib.CLifegame(2, 3)
    a = [[None]*3 for i in range(2)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    for i in range(2):
        g.full_field(i, a[i])
    g.next_game_state()
    assert g.game_field == [["f", "f", "f"], ["f", "f", "f"]], "Next1_1 not passed"
    g.next_game_state()
    assert g.game_field == [["f", "n", "f"], ["f", "n", "f"]], "Next1_2 not passed"


def test_next2():
    g = lib.CLifegame(3, 4)
    a = [[None]*4 for i in range(3)]
    a[0] = ["f", "f", "r", "f"]
    a[1] = ["n", "f", "n", "s"]
    a[2] = ["f", "s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    g.next_game_state()
    assert g.game_field == [["f", "f", "r", "n"], ["n", "f", "f", "s"], ["n", "n", "s", "s"]], "Next2 not passed"


def test_next3():
    g = lib.CLifegame(3, 3)
    a = [[None]*3 for i in range(3)]
    a[0] = ["f", "f", "f"]
    a[1] = ["n", "f", "n"]
    a[2] = ["s", "s", "s"]
    for i in range(3):
        g.full_field(i, a[i])
    g.play(2)
    assert g.game_field == [["f", "n", "f"], ["f", "n", "f"], ["n", "n", "n"]], "Next3 not passed"


def test():
    test_init_and_full()
    test_init_and_full()
    test_count_neighbours1()
    test_count_neighbours2()
    test_count_neighbours3()
    test_objects_update_cell1()
    test_objects_update_cell2()
    test_next1()
    test_next2()
    test_next3()
