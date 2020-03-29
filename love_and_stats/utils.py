import bisect
from itertools import permutations
import statistics


def skippable_permutations(iterable, r=None):
    items = [i for i in iterable]
    if r is None:
        r = len(items)
    leave_prefix_len = r

    def swap(i, j):
        if i == j:
            return
        items[i], items[j] = items[j], items[i]

    def set_skip(i):
        nonlocal leave_prefix_len
        if i is not None:
            leave_prefix_len = i

    def recurse(n):
        nonlocal leave_prefix_len
        if n == r:
            set_skip((yield items[:r]))
            return

        for i in range(n, len(items)):
            swap(n, i)
            for item in recurse(n+1):
                set_skip((yield item))
                if leave_prefix_len <= n:
                    if leave_prefix_len == n:
                        leave_prefix_len = r
                    break
            swap(n, i)

    return recurse(0)


def play_game(item_ranks, mar_list):
    past_ranks = []
    for i, (rank, mar) in enumerate(zip(item_ranks, mar_list)):
        local_rank = bisect.bisect(past_ranks, rank)
        if local_rank < mar:
            return i
        else:
            past_ranks.insert(local_rank, rank)

    else:
        return len(mar_list)


def brute_force_expt_score(mar_list):
    return statistics.mean(
        item_ranks[play_game(item_ranks, mar_list)]
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


def min_list(iterable, key=lambda x: x):
    it = iter(iterable)
    try:
        results = [next(it)]
    except StopIteration:
        return []

    for item in it:
        if key(item) < key(results[0]):
            results = [item]
        elif key(item) == key(results[0]):
            results.append(item)

    return results
