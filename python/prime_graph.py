"""ESTABLISHED: exact PGA finite residual graph model.

This module does not claim a prime exists.  It verifies degree and graph
identities against trial division and the independent interval sieve.
"""

import math

from legendre_core import segmented_sieve


def sinc(value: float) -> float:
    return 1.0 if value == 0.0 else math.sin(value) / value


def fixed_kernel_weight(gamma: float, h: float, k: int) -> float:
    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer")
    if k % 2:
        raise ValueError("PGA kernels currently require even k")
    return sinc(gamma * h / k) ** k


def adaptive_k(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    return 2 * max(2, math.ceil(math.log(math.log(n + 1))))


def adaptive_cutoff(n: int) -> int:
    return 4 * adaptive_k(n) * (n + 1)


def fixed_zero_sum(n: int, ordinates: list[float], k: int, cutoff: float) -> float:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    if k <= 0 or k % 2:
        raise ValueError("k must be a positive even integer")
    h = math.log1p(1.0 / n)
    x = n * (n + 1)
    total = 0.0
    for gamma in ordinates:
        if not math.isfinite(gamma) or gamma <= 0:
            raise ValueError("ordinates must be positive finite values")
        if gamma <= cutoff:
            total += 2.0 * math.cos(gamma * math.log(x)) * fixed_kernel_weight(gamma, h, k)
    return total


def adaptive_zero_sum(n: int, ordinates: list[float]) -> float:
    k = adaptive_k(n)
    return fixed_zero_sum(n, ordinates, k, float(adaptive_cutoff(n)))


def cube_root_floor(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("value must be a nonnegative integer")
    if value <= 1:
        return value
    low, high = 0, 1 << ((value.bit_length() + 2) // 3)
    while low + 1 < high:
        middle = (low + high) // 2
        if middle ** 3 <= value:
            low = middle
        else:
            high = middle
    return low


def analyze(n: int) -> dict[str, int]:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    lower, upper = n * n, n * n + 2 * n
    cutoff = cube_root_floor(upper)
    primes = segmented_sieve(n)
    live = bytearray(b"\x01") * (2 * n)
    degree = bytearray(2 * n)

    for p in primes:
        if p > cutoff:
            break
        first = p - lower % p
        for offset in range(first, 2 * n + 1, p):
            live[offset - 1] = 0

    for p in primes:
        if p <= cutoff:
            continue
        first = p - lower % p
        for offset in range(first, 2 * n + 1, p):
            index = offset - 1
            if live[index]:
                degree[index] += 1

    rough = [index for index, active in enumerate(live) if active]
    degree_one = sum(degree[index] == 1 for index in rough)
    degree_two = sum(degree[index] == 2 for index in rough)
    degree_three = sum(degree[index] >= 3 for index in rough)
    edge_incidence = sum(degree[index] for index in rough)
    primes_count = sum(degree[index] == 0 for index in rough)

    r = len(rough)
    h = degree_three
    g = 3 * r + 2 * degree_two - 3 * edge_incidence
    lower_bound = r - edge_incidence + (2 * degree_two) // 3
    exact = r - edge_incidence + degree_two - h
    return {
        "n": n,
        "R": r,
        "E": edge_incidence,
        "W": degree_two,
        "H": h,
        "L": primes_count,
        "degree_one": degree_one,
        "G": g,
        "exact": exact,
        "lower_bound": lower_bound,
    }
