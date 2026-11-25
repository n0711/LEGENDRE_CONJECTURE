import math
from bisect import bisect_left, bisect_right
from typing import Iterable


def segmented_sieve(limit: int, block_size: int = 1 << 16) -> list[int]:
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
    primes.extend(p for p in base_primes if p >= 2 and p not in primes)
    return sorted(set(primes))


def kernel(n: int, t: float) -> float:
    x = n * (n + 1)
    h = math.log1p(1.0 / n)
    u = abs(math.log(t / x))
    if u >= h:
        return 0.0
    return math.sqrt(x / t) * (1.0 - u / h)


def weighted_prime_sum(n: int, primes: Iterable[int]) -> float:
    if not hasattr(primes, "__getitem__"):
        primes = list(primes)
    x = n * (n + 1)
    h = math.log1p(1.0 / n)
    lo = x * math.exp(-h)
    hi = x * math.exp(h)
    total = 0.0
    first = bisect_right(primes, lo)
    last = bisect_left(primes, hi)
    for p in primes[first:last]:
        total += math.log(p) * kernel(n, p)
    return total


def weighted_von_mangoldt_sum(n: int, limit: int) -> float:
    primes = segmented_sieve(limit)
    x = n * (n + 1)
    h = math.log1p(1.0 / n)
    lo = x * math.exp(-h)
    hi = x * math.exp(h)
    total = 0.0
    for p in primes:
        power = p
        while power <= limit:
            if lo < power < hi:
                total += math.log(p) * kernel(n, power)
            power *= p
    return total


def mellin_principal(n: int) -> float:
    x = n * (n + 1)
    h = math.log1p(1.0 / n)
    a = 0.5
    return 2.0 * x * (math.cosh(a * h) - 1.0) / (h * a * a)


def first_standard_gap(n: int, primes: Iterable[int]) -> tuple[int, int] | None:
    ps = sorted(p for p in primes if n * n < p < (n + 1) ** 2)
    return (ps[0], ps[-1]) if ps else None
