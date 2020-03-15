import fractions
import itertools


def ksumCk(*k_array):
    """
    Effectively computes nCk over a set of k values, where n is the sum of all
    k values. Generically extends to being an n-ary commutative and associative
    operator.
    """
    result = 1
    for i, j in enumerate((m for k in k_array for m in range(1, k+1)), 1):
        result = (result * i) // j
    return result


def chance_of_best(rank, seen_count, remaining_count):
    if not 0 <= rank < seen_count:
        raise ValueError('rank {} not in range [0, {})'.format(rank, seen_count))
    return fractions.Fraction(
        ksumCk(rank, remaining_count),
        ksumCk(seen_count, remaining_count)
    )
