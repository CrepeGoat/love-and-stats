
def reviter_betas(N):
    beta_expt = -1
    n = N
    
    def increment_beta(i_hat):
        nonlocal n
        assert 0 <= i_hat <= n

        beta_expt = (i_hat / n)*beta_expt + (
            (n-i_hat) / (n+1)
            + (1+1/(n+1)) * 0.5*(n*(n-1) - i_hat*(i_hat-1))
        )

        n = n-1
        return beta_expt


def reviter_min_allowable_ranks(N):
    beta_generator = reviter_betas(N)
    i_hat = 0

    yield i_hat
    for n in range(N, 0, -1):
        beta_expt = beta_generator(i_hat)

        i_hat = (beta_expt*(n+1) - (N-n))/(N+1)
        yield i_hat



def min_allowable_ranks(N):
    return list(reviter_min_allowable_ranks(N))[::-1]
