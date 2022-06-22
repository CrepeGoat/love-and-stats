from itertools import permutations
import statistics

import hypothesis as hyp
from utils import _strategies_ranks

from love_and_stats import simulate


def _expt_score_brute(mar_list):
    return statistics.mean(
        simulate.play_game(item_ranks, mar_list)
        for item_ranks in permutations(range(len(mar_list)))
    )


@hyp.given(ranks=_strategies_ranks(7))
def test_expt_score(ranks):
    assert float(simulate.expt_score(ranks)) == _expt_score_brute(ranks)
