import pytest

from main import add, multiply, divide

@pytest.mark.parametrize('inputs,expected_result',
                         [((1, 1), 2),
                          ((1, 2), 3),
                          ((1, 2, 3), 6),
                          ((1, -1), 0),
                          ([], 0)])
def test_add(inputs, expected_result):
    assert add(*inputs) == expected_result
    assert add() == 0


@pytest.mark.parametrize('inputs,expected_result',
                         [((1, 1), 1),
                          ((1, 2), 2),
                          ((1, 2, 3), 6),
                          ((1, -1), -1),
                          ([], 1)])
def test_multiply(inputs, expected_result):
    assert multiply(*inputs) == expected_result
    assert multiply() == 1


@pytest.mark.parametrize('inputs,expected_result',
                         [((1, 1), 1),
                          ((1, 2), 0.5),
                          ((4, 2), 2),
                          ((1, 2, 4), 0.125),
                          ((1, -1), -1),
                          ((4,), 4)])
def test_divide_velid_inputs(inputs, expected_result):
    assert divide(*inputs) == expected_result


def test_divide_invalid_inputs():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with pytest.raises(ValueError):
        divide()

