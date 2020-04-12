import pytest
from love_and_stats import utils

from itertools import permutations
import statistics


def brute_force_expt_score(mar_list):
    return statistics.mean(
        utils.play_game(item_ranks, mar_list)
        for item_ranks in permutations(range(len(mar_list)))
    )


@pytest.mark.parametrize('some_mar_list', list(utils.gen_mar_lists(4)))
def test_expt_score(some_mar_list):
    assert (
        float(utils.expt_score(some_mar_list))
        == brute_force_expt_score(some_mar_list)
    )
