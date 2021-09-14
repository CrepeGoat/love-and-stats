import hypothesis as hyp
import hypothesis.strategies as hyp_st

from utils import _strategies_ranks
from love_and_stats import optimal, simulate


@hyp.given(optimal_ranks=hyp_st.integers(1, 200).map(optimal.max_allowable_ranks))
def test_mar_is_valid(optimal_ranks):
    assert all(isinstance(rank, int) for rank in optimal_ranks)
    assert all(0 <= rank <= i for i, rank in enumerate(optimal_ranks, 1))


@hyp.given(optimal_ranks=hyp_st.integers(1, 200).map(optimal.max_allowable_ranks))
def test_mar_is_feasible(optimal_ranks):
    assert all(i <= j for i, j in zip(optimal_ranks[:-1], optimal_ranks[1:]))


@hyp.given(ranks=_strategies_ranks(20))
def test_mar_is_optimal(ranks):
    n = len(ranks)
    optimal_ranks = optimal.max_allowable_ranks(n)
    assert simulate.expt_score(optimal_ranks) <= simulate.expt_score(ranks)
