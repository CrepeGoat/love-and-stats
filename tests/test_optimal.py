import pytest
from love_and_stats import optimal, utils


@pytest.mark.parametrize(
    "mar_list", [optimal.max_allowable_ranks(i) for i in range(1, 100)]
)
def test_mar_is_valid(mar_list):
    assert all(isinstance(rank, int) for rank in mar_list)
    assert all(0 <= rank <= i for i, rank in enumerate(mar_list, 1))


@pytest.mark.parametrize(
    "opt_mar_list", [optimal.max_allowable_ranks(i) for i in range(1, 100)]
)
def test_opt_mar_is_feasible(opt_mar_list):
    assert all(i <= j for i, j in zip(opt_mar_list[:-1], opt_mar_list[1:]))


@pytest.mark.parametrize("some_mar_list", list(utils.gen_mar_lists(4)))
def test_mar_is_optimal(some_mar_list):
    assert utils.expt_score(
        optimal.max_allowable_ranks(len(some_mar_list))
    ) <= utils.expt_score(some_mar_list)
