import pytest
from love_and_stats import core

import bisect
from itertools import permutations
import statistics


def play_game(item_ranks, mar_list):
    past_ranks = []
    for rank, mar in zip(item_ranks, mar_list):
        local_rank = bisect.bisect(past_ranks, rank)
        if local_rank >= mar:
            return rank
        else:
            past_ranks.insert(local_rank, rank)

    else:
        return -1


def brute_force_expt_score(mar_list):
    return statistics.mean(
        play_game(item_ranks, mar_list)
        for item_ranks in permutations(range(len(mar_list)))
    )


def gen_mar_lists(N, suffix=()):
    if N == 0:
        yield suffix
        return

    yield from (
        mar
        for i in range(N+1)
        for mar in gen_mar_lists(N-1, (i,)+suffix) 
    )


@pytest.mark.parametrize('some_mar_list', list(gen_mar_lists(4)))
def test_mar(some_mar_list):
    assert (
        brute_force_expt_score(core.min_allowable_ranks(len(some_mar_list)))
        >= brute_force_expt_score(some_mar_list)
    )
