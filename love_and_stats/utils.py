import bisect
from functools import reduce
from operator import mul
import statistics


def paused_iter(iterable):
    iterator = iter(iterable)
    while True:
        item = next(iterator)
        while (yield item):
            pass


def skippable_insertions(n):
    leave_prefix_len = n

    def set_skip(i):
        nonlocal leave_prefix_len
        if i is not None:
            leave_prefix_len = i

    ranges = []

    def fill_ranges():
        for i in range(len(ranges), n):
            ranges.append(paused_iter(range(i+1)))
            next(ranges[-1])

    def increment_ranges():
        while ranges:
            try:
                next(ranges[-1])
                break
            except StopIteration:
                ranges.pop()

    def yield_value():
        return tuple(r.send(True) for r in ranges)
    
    fill_ranges()

    while ranges:
        fill_ranges()
        prefix_len = (yield yield_value())
        if prefix_len is not None:
            del ranges[prefix_len:]
        increment_ranges()


def nPr(n, r):
    return reduce(mul, range(n-r+1, n+1), 1)


def play_game(local_ranks, mar_list):
    for i, (local_rank, mar) in enumerate(zip(local_ranks, mar_list)):
        if local_rank < mar:
            return i

    else:
        return len(mar_list)


def insertions_to_permutation(insertions):
    def invert_perm(perm):
        result = [None for _ in range(len(perm))]
        for i, p in enumerate(perm):
            result[p] = i
        return result

    result = []
    for i, pos in enumerate(insertions):
        result.insert(pos, i)
    return invert_perm(result)


def brute_force_expt_score(mar_list):
    n = len(mar_list)
    total = 0
    iterator = skippable_insertions(n)

    local_ranks = next(iterator)

    while True:
        choice = play_game(local_ranks, mar_list)
        total += nPr(n, choice) * (
            insertions_to_permutation(local_ranks)[choice] if choice < n
            else choice
        )
        try:
            item_ranks = iterator.send(choice)
        except StopIteration:
            break
    return total / nPr(n, n)


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
