import bisect
from itertools import permutations
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


def play_game(local_ranks, mar_list):
    for i, (local_rank, mar) in enumerate(zip(local_ranks, mar_list)):
        if local_rank < mar:
            return i

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
