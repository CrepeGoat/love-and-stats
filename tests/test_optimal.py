import pytest
from love_and_stats import optimal, utils


@pytest.mark.parametrize('mar_list', [
    optimal.max_allowable_ranks(i)
    for i in range(1, 100)
])
def test_mar_is_valid(mar_list):
    assert all(isinstance(rank, int) for rank in mar_list)
    assert all(
        0 <= rank <= i
        for i, rank in enumerate(mar_list, 1)
    )


@pytest.mark.parametrize('opt_mar_list', [
    optimal.max_allowable_ranks(i)
    for i in range(1, 100)
])
def test_opt_mar_is_feasible(opt_mar_list):
    assert all(i <= j for i, j in zip(opt_mar_list[:-1], opt_mar_list[1:]))


def make_test_mar_is_optimal(n):
    opt_mar_list = optimal.max_allowable_ranks(n)
    opt_score = utils.expt_score(opt_mar_list)

    @pytest.mark.parametrize('some_mar_list', list(utils.gen_mar_lists(n)))
    def test_mar_is_optimal(some_mar_list):
        assert opt_score <= utils.expt_score(some_mar_list)

    return test_mar_is_optimal

test_mar_is_optimal = make_test_mar_is_optimal(6)
