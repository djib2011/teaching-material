from main import add, multiply


def test_add():
    assert add(1, 1) == 2
    assert add(1, 2, 3) == 6
    assert add(1, -1) == 0
    assert add() == 0


def test_multiply():
    assert multiply(1, 1) == 1
    assert multiply(1, 2, 3) == 6
    assert multiply(1, -1) == -1
    assert multiply() == 1

