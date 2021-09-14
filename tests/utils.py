import hypothesis.strategies as hyp_st


@hyp_st.composite
def _strategies_ranks(draw, size):
    return [draw(hyp_st.integers(0, i)) for i in range(1, size + 1)]
