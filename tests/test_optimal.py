import pytest
from love_and_stats import optimal, utils


@pytest.mark.parametrize('some_mar_list', list(utils.gen_mar_lists(4)))
def test_mar(some_mar_list):
    assert (
        utils.brute_force_expt_score(optimal.max_allowable_ranks(len(some_mar_list)))
        >= utils.brute_force_expt_score(some_mar_list)
    )
