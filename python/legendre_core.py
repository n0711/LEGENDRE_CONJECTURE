"""ESTABLISHED formulas; floating-point outputs are NUMERICAL, not certificates."""

import math
from bisect import bisect_left, bisect_right
from typing import Iterable


def segmented_sieve(limit: int, block_size: int = 1 << 16) -> list[int]:
    if block_size < 1:
        raise ValueError("block_size must be positive")
    if limit < 2:
        return []

    small_limit = math.isqrt(limit)
    small = bytearray(b"\x01") * (small_limit + 1)
    small[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(small_limit) + 1):
        if small[p]:
            small[p * p : small_limit + 1 : p] = b"\x00" * (
                ((small_limit - p * p) // p) + 1
            )
    base_primes = [i for i in range(2, small_limit + 1) if small[i]]

    primes: list[int] = []
    for lo in range(2, limit + 1, block_size):
        hi = min(lo + block_size - 1, limit)
        block = bytearray(b"\x01") * (hi - lo + 1)
        for p in base_primes:
            first = max(p * p, ((lo + p - 1) // p) * p)
            if first > hi:
                continue
            block[first - lo : hi - lo + 1 : p] = b"\x00" * (
                ((hi - first) // p) + 1
            )
        primes.extend(lo + i for i in range(len(block)) if block[i])
    return primes


def kernel(n: int, t: float) -> float:
    if n < 1:
        raise ValueError("n must be positive")
    if t <= n * n or t >= (n + 1) ** 2:
        return 0.0
    x = n * (n + 1)
    h = math.log1p(1.0 / n)
    u = abs(math.log1p((t - x) / x))
    if u >= h:
        return 0.0
    return math.sqrt(x / t) * (1.0 - u / h)


def weighted_prime_sum(n: int, primes: Iterable[int]) -> float:
    """NUMERICAL weighted sum; input must be increasing, distinct primes."""
    if not hasattr(primes, "__getitem__"):
        primes = list(primes)
    if n < 1:
        raise ValueError("n must be positive")
    lo = n * n
    hi = (n + 1) ** 2
    total = 0.0
    first = bisect_right(primes, lo)
    last = bisect_left(primes, hi)
    for p in primes[first:last]:
        total += math.log(p) * kernel(n, p)
    return total


def weighted_von_mangoldt_sum(n: int, limit: int) -> float:
    if n < 1:
        raise ValueError("n must be positive")
    if limit < (n + 1) ** 2 - 1:
        raise ValueError("limit must cover the complete square interval")
    primes = segmented_sieve(limit)
    lo = n * n
    hi = (n + 1) ** 2
    total = 0.0
    for p in primes:
        power = p
        while power <= limit:
            if lo < power < hi:
                total += math.log(p) * kernel(n, power)
            power *= p
    return total


def mellin_principal(n: int) -> float:
    if n < 1:
        raise ValueError("n must be positive")
    x = n * (n + 1)
    h = math.log1p(1.0 / n)
    # ESTABLISHED: cosh(h/2)-1 = 2*sinh(h/4)^2 avoids cancellation.
    z = h / 4.0
    return x * h * (math.sinh(z) / z) ** 2


def prime_power_bound(n: int) -> float:
    """NUMERICAL evaluation of the proved bound in docs/VERIFIED_LEMMAS.md."""
    if n < 1:
        raise ValueError("n must be positive")
    upper = n * (n + 2)
    max_exponent = upper.bit_length() - 1
    return math.log(upper) * math.fsum(1.0 / k for k in range(3, max_exponent + 1))


def trivial_zero_bound(n: int) -> float:
    """NUMERICAL evaluation of an ESTABLISHED bound, for n >= 2."""
    if n < 2:
        raise ValueError("the bound requires n >= 2")
    return (2 * n + 1) / (n * n * (n ** 4 - 1))


def first_standard_gap(n: int, primes: Iterable[int]) -> tuple[int, int] | None:
    ps = sorted(p for p in primes if n * n < p < (n + 1) ** 2)
    return (ps[0], ps[-1]) if ps else None
