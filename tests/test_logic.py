import pytest

from love_and_stats import logic


def test_factorial():
    assert logic.factorial(0) == 1
    assert logic.factorial(1) == 1
    assert logic.factorial(2) == 2
    assert logic.factorial(3) == 6
    assert logic.factorial(4) == 24
    assert logic.factorial(5) == 120
    assert logic.factorial(6) == 720


def test_nPk():
    for i in range(5):
        assert logic.nPk(5, i) == logic.factorial(5) // logic.factorial(5-i)


def test_nCk():
    for i in range(5):
        assert logic.ksumCk(i, 5-i) == logic.factorial(5) // (
            logic.factorial(5-i) * logic.factorial(i)
        )


def test_nIk():
    for i in range(5):
        assert logic.nIk(5, i) == logic.factorial(5+i) // logic.factorial(5)


def test_iter_nIk():
    for i, iIk in zip(range(10), logic.iter_iIk(5)):
        assert iIk == logic.nIk(i, 5)
