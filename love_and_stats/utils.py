import bisect
from itertools import permutations
import statistics


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


def brute_force_expt_score(mar_list):
    return statistics.mean(
        play_game(item_ranks, mar_list)
        for item_ranks in permutations(range(len(mar_list)))
    )


def gen_mar_lists(N):

    def recurse(N, suffix=()):
        if N == 0:
            yield suffix
            return

        # If ith place out of n with m remaining is good enough,
        # then ith place out of n+1 with m-1 remaining is also good enough
        # -> a MAR-list that breaks this rule can*not* be optimal 
        max_i = suffix[0] if suffix else N
        yield from (
            mar
            for i in range(max_i+1)
            for mar in recurse(N-1, (i,)+suffix) 
        )

    return recurse(N)

