"""ESTABLISHED: exact finite sieve identities; no infinite positivity claim.

Proofs and complexity are recorded in docs/DISCRETE_SIEVE.md. All interval
endpoints and inclusion-exclusion terms use integer arithmetic.
"""

from bisect import bisect_right
from fractions import Fraction
from math import prod

from legendre_core import segmented_sieve


def _endpoints(n: int) -> tuple[int, int]:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    return n * n, n * n + 2 * n


def mobius_survivors(n: int, degree: int | None = None) -> int:
    """ESTABLISHED: full Mobius sum, or a Bonferroni partial sum.

    With degree=None this is the number of primes in (n**2, (n+1)**2).
    Odd degree gives a lower bound; even degree gives an upper bound.
    Products exceeding the upper endpoint contribute zero and are pruned.
    """
    lower, upper = _endpoints(n)
    if degree is not None and (
        isinstance(degree, bool) or not isinstance(degree, int) or degree < 0
    ):
        raise ValueError("degree must be a nonnegative integer or None")
    primes = segmented_sieve(n)
    max_degree = len(primes) if degree is None else min(degree, len(primes))

    def visit(product: int, start: int, depth: int, sign: int) -> int:
        subtotal = sign * (upper // product - lower // product)
        if depth == max_degree:
            return subtotal
        for index in range(start, len(primes)):
            next_product = product * primes[index]
            if next_product > upper:
                break
            subtotal += visit(next_product, index + 1, depth + 1, -sign)
        return subtotal

    return visit(1, 0, 0, 1)


def sieve_survivors(n: int, cutoff: int | None = None) -> list[int]:
    """ESTABLISHED: integers in A_n avoiding every prime <= cutoff.

    The default cutoff n gives exactly the primes in A_n. The optional
    cutoff is restricted to [0,n], so the sieve never erases a prime in A_n.
    """
    lower, upper = _endpoints(n)
    cutoff = n if cutoff is None else cutoff
    if isinstance(cutoff, bool) or not isinstance(cutoff, int) or not 0 <= cutoff <= n:
        raise ValueError("cutoff must be an integer in [0,n]")
    flags = bytearray(b"\x01") * (2 * n)
    for p in segmented_sieve(cutoff):
        first = (lower // p + 1) * p
        if first <= upper:
            flags[first - lower - 1 : : p] = b"\x00" * ((upper - first) // p + 1)
    return [lower + index + 1 for index, flag in enumerate(flags) if flag]


def cube_root_floor(value: int) -> int:
    """ESTABLISHED: floor(cube_root(value)), using integer binary search."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("value must be a nonnegative integer")
    low, high = 0, 1 << ((value.bit_length() + 2) // 3)
    while low + 1 < high:
        middle = (low + high) // 2
        if middle * middle * middle <= value:
            low = middle
        else:
            high = middle
    return low


def semiprime_split(n: int) -> tuple[int, int, int]:
    """ESTABLISHED: return (rough survivors, residual composites, primes).

    At z=floor(cube_root(n*n+2*n)), residual composites are unique pq with
    z < p <= n < q. Prime counts in the correction are evaluated exactly.
    """
    lower, upper = _endpoints(n)
    cutoff = min(n, cube_root_floor(upper))
    rough_count = len(sieve_survivors(n, cutoff))
    # ESTABLISHED: every larger factor q is <= upper/(cutoff+1).
    primes = segmented_sieve(upper // (cutoff + 1))
    correction = 0
    for p in primes:
        if p > n:
            break
        if p > cutoff:
            correction += bisect_right(primes, upper // p) - bisect_right(
                primes, lower // p
            )
    return rough_count, correction, rough_count - correction


def density_lower_bound(n: int) -> Fraction:
    """ESTABLISHED: exact rational H*prod(1-1/p)-(2**k-1).

    This rigorous but often negative lower bound discards remainder signs.
    """
    _endpoints(n)
    primes = segmented_sieve(n)
    density = Fraction(prod(p - 1 for p in primes), prod(primes))
    return 2 * n * density - (2 ** len(primes) - 1)
