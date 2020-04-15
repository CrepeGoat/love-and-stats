import pytest
from love_and_stats import interval

from itertools import product


def demo_Interval_str():
    for b_lwr, b_upr, incl_lwr, incl_upr in product(
        range(10), range(10), (False, True), (False, True)
    ):
        itvl = interval.Interval.from_values(b_lwr, b_upr, incl_lwr, incl_upr)
        #print(itvl._bounds)
        print(b_lwr, b_upr, incl_lwr, incl_upr, "\t->", itvl)

    return


@pytest.mark.parametrize('x, itvl, result', [
    # (Literal) Edge Cases - Left Bound
    (1, interval.Interval.from_values(1, 3, False, False), False),
    (1, interval.Interval.from_values(1, 3, False, True), False),
    (1, interval.Interval.from_values(1, 3, True, False), True),
    (1, interval.Interval.from_values(1, 3, True, True), True),
    # (Literal) Edge Cases - Right Bound
    (6.2, interval.Interval.from_values(-1/2, 6.2, False, False), False),
    (6.2, interval.Interval.from_values(-1/2, 6.2, False, True), True),
    (6.2, interval.Interval.from_values(-1/2, 6.2, True, False), False),
    (6.2, interval.Interval.from_values(-1/2, 6.2, True, True), True),
    # Zero-width cases
    (7, interval.Interval.from_values(7, 7), False),
    (0, interval.Interval.from_values(0, 0, True, True), True),
    (0, interval.Interval.from_values(0, 0, False, True), False),
    (0, interval.Interval.from_values(0, 0, True, False), False),
    (0, interval.Interval.from_values(0, 0, False, False), False),
    # Misordered-bound cases
    (1, interval.Interval.from_values(10, 0, True, True), False),
    (1, interval.Interval.from_values(10, 0, False, True), False),
    (1, interval.Interval.from_values(10, 0, True, False), False),
    (1, interval.Interval.from_values(10, 0, False, False), False),
    (0, interval.Interval.from_values(10, 0, True, True), False),
    (5, interval.Interval.from_values(10, 0, True, True), False),
    (13, interval.Interval.from_values(10, 0, True, True), False),
    (-4, interval.Interval.from_values(10, 0, True, True), False),
    # Whatever cases
    (2, interval.Interval.from_values(1, 10), True),
    (5, interval.Interval.from_values(1, 10), True),
    (10, interval.Interval.from_values(1, 10), False),
    (2, interval.Interval.from_values(-4, 1), False),
])
def test_Interval_in(x, itvl, result):
    assert (x in itvl) == result


@pytest.mark.parametrize('itvl1, itvl2, result', [
    # Infinite-bound cases
    (interval.Interval.from_values(3.4, 4.0), interval.Interval.from_values(lower_bound=1), True),
    (interval.Interval.from_values(-3.8, 7.5), interval.Interval.from_values(upper_bound=4), False),
    # Heterogeneous Type Cases
    (interval.Interval.from_values(2.0, 5.3), interval.Interval.from_values(1, 8), True),
    (interval.Interval.from_values(-2.7, 5), interval.Interval.from_values(1, 8.2), False),
    # Whatever cases
    (interval.Interval.from_values(2, 5), interval.Interval.from_values(1, 8), True),
    (interval.Interval.from_values(1, 8), interval.Interval.from_values(2, 5), False),
])
def test_Interval_subeqset(itvl1, itvl2, result):
    assert (itvl1 in itvl2) == result


if __name__ == "__main__":
    pytest.main()
