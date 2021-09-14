import bisect
from fractions import Fraction


def play_game(item_ranks, mar_list):
    past_ranks = []
    for rank, mar in zip(item_ranks, mar_list):
        local_rank = bisect.bisect(past_ranks, rank)
        if local_rank < mar:
            return rank
        else:
            past_ranks.insert(local_rank, rank)

    else:
        return len(mar_list)


def riter_round_expt_scores(N, score_on_bust=None):
    """
    Iterates in reverse round order the expected round scores for a particular
    MAR list. MAR items are passed in via the generator `send` method.
    """
    beta_expt = score_on_bust if score_on_bust is not None else N
    for n in range(N, 0, -1):
        i = Fraction((yield (n + 1, beta_expt)))

        m = N - n
        beta_expt = ((n - i) / n) * beta_expt + (i / n) * (
            m + (i - 1) * (N + 1) / 2
        ) / (n + 1)

    yield (n, beta_expt)


def send_to(generator, values):
    """
    Iterates items yielded from passing values to a generator object via its
    `send` method.
    """
    iterator = iter(generator)
    yield next(iterator)
    for value in values:
        yield iterator.send(value)


def expt_score(mar_list):
    for _, result in send_to(riter_round_expt_scores(len(mar_list)), mar_list[::-1]):
        pass
    return result


def gen_mar_lists(N):
    def recurse(N, suffix=()):
        if N == 0:
            yield suffix
            return

        yield from (mar for i in range(N + 1) for mar in recurse(N - 1, (i,) + suffix))

    return recurse(N)
