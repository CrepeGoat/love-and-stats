from love_and_stats import simulate


def _int_div_ceil(n, d):
    return -((-n) // d)


def reviter_max_allowable_ranks(N):
    riter_betas = iter(simulate.riter_round_expt_scores(N))
    n2, beta_expt = next(riter_betas)
    assert n2 == N + 1

    for n in range(N, 0, -1):
        m = N - n
        i_hat = int(_int_div_ceil(beta_expt * (n + 1) - m, (N + 1)))
        yield i_hat

        n2, beta_expt = riter_betas.send(i_hat)
        assert n2 == n


def max_allowable_ranks(N):
    result = tuple(reviter_max_allowable_ranks(N))[::-1]

    assert len(result) == N
    return result
