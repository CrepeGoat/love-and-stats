import pytest
from love_and_stats import core

import bisect
import itertools
import statistics


def play_game(item_ranks, mar_list):
    past_ranks = []
    for rank, mar in zip(item_ranks, mar_list):
        local_rank = bisect.bisect(past_ranks, rank)
        if local_rank >= mar:
            return rank

    else:
        return -1


def brute_force_expt_score(mar_list):
    return statistics.mean(
        play_game(item_ranks, mar_list)
        for item_ranks in itertools.permutations(range(len(mar_list)))
    )


def is_feasible(mar_list):
    """
    Regardless of how a MAR list is determined, the Rth place out of n+1 items
    with m-1 items remaining is *always* better than Rth place out of n items
    with m items remaining. Any MAR list that contradicts this rule is
    "infeasible" and can be ruled out without further assessment.
    """
    pass


def gen_mar_lists(N):
    return (
        mar_list
        for mar_list in itertools.product(*(range(i+2) for i in range(N)))
        if is_feasible(mar_list)
    )


@pytest.mark.parametrize('some_mar_list', list(gen_mar_lists(4)))
def test_mar(some_mar_list):
    assert (
        brute_force_expt_score(core.min_allowable_ranks(len(some_mar_list)))
        >= brute_force_expt_score(some_mar_list)
    )
