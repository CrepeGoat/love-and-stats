
def reviter_max_allowable_ranks(N):
    beta_expt = N
    for n in range(N, 0, -1):
        m = N-n
        i_hat = (beta_expt*(n+1) - m)/(N+1)
        yield i_hat

        beta_expt = (
            ((n-i_hat) / n)*beta_expt
            + (i_hat / (n*(n+1))) * (m + 0.5*(i_hat-1)*(N+1))
        )


def max_allowable_ranks(N):
    result = tuple(reviter_max_allowable_ranks(N))[::-1]
    
    assert len(result) == N
    return result
