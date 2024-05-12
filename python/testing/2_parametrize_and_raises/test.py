import pytest

from main import add, multiply


@pytest.mark.parametrize('inputs', 'expected_result',
                         [((1, 1), 2),
                          ((1, 2), 3),
                          ((1, 2, 3), 6),
                          ((1, -1), 0)])
def test_add(inputs, expected_result):
    assert add(*inputs) == expected_result
    assert add() == 0


@pytest.mark.parametrize('inputs', 'expected_result',
                         [((1, 1), 1),
                          ((1, 2), 2),
                          ((1, 2, 3), 6),
                          ((1, -1), -1)])
def test_multiply(inputs, expected_result):
    assert multiply(*inputs) == expected_result
    assert multiply() == 1

