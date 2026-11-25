import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from legendre_core import segmented_sieve
from prime_graph import (
    adaptive_cutoff,
    adaptive_k,
    adaptive_zero_sum,
    analyze,
    cube_root_floor,
    fixed_kernel_weight,
    fixed_zero_sum,
)


def trial_prime(m):
    return m >= 2 and all(m % d for d in range(2, math.isqrt(m) + 1))


@pytest.mark.parametrize(("value", "root"), [(0, 0), (1, 1), (2, 1), (7, 1), (8, 2), (27, 3)])
def test_pga_cube_root_floor_boundaries(value, root):
    assert cube_root_floor(value) == root


@pytest.mark.parametrize("n", range(1, 501))
def test_pga_identity_and_degree_limit(n):
    upper = n * n + 2 * n
    cutoff = cube_root_floor(upper)
    primes = segmented_sieve(upper)
    independent_primes = [m for m in range(n * n + 1, upper + 1) if trial_prime(m)]

    result = analyze(n)
    assert result["H"] == 0
    assert result["L"] == len(independent_primes)
    assert result["R"] == sum(
        all((n * n + offset) % p for p in primes if p <= cutoff)
        for offset in range(1, 2 * n + 1)
    )
    assert result["R"] - result["E"] + result["W"] - result["H"] == result["L"]
    assert 3 * result["R"] + 2 * result["W"] - 3 * result["E"] == 3 * result["L"] - result["W"]
    assert result["G"] > 0

    # The residual graph is degree at most two after the cube-root cutoff.
    for m in range(n * n + 1, upper + 1):
        if all(m % p for p in primes if p <= cutoff):
            degree = sum(p > cutoff and p < m and m % p == 0 for p in primes)
            assert degree <= 2


def test_degree_two_is_not_always_p_squared_q():
    n = 3
    upper = n * n + 2 * n
    cutoff = cube_root_floor(upper)
    assert cutoff == 2
    m = 15
    divisors = [p for p in segmented_sieve(upper) if cutoff < p < m and m % p == 0]
    assert divisors == [3, 5]
    exponents = []
    for p in divisors:
        exponent = 0
        x = m
        while x % p == 0:
            exponent += 1
            x //= p
        exponents.append(exponent)
    assert exponents == [1, 1]
    assert sorted(exponents) != [1, 2]


@pytest.mark.parametrize("n", range(1, 501))
def test_pga_lower_bound(n):
    result = analyze(n)
    identity_lower = 3 * result["R"] - 3 * result["E"] + 2 * result["W"]
    exact_three_lower = 3 * result["L"]
    assert exact_three_lower >= identity_lower


def test_fixed_and_adaptive_kernel_definitions():
    h = math.log1p(1 / 100)
    assert fixed_kernel_weight(0.0, h, 4) == 1.0
    for k in (2, 4, 6, 8):
        assert 0.0 <= fixed_kernel_weight(100.0, h, k) <= 1.0
    assert adaptive_k(1) == 4
    assert adaptive_k(100) == 2 * max(2, math.ceil(math.log(math.log(101))))
    assert adaptive_cutoff(100) == 4 * adaptive_k(100) * 101


def test_fixed_and_adaptive_zero_sums():
    ordinates = [14.134725, 21.022040, 25.010858]
    fixed = fixed_zero_sum(100, ordinates, 4, 100.0)
    adaptive = adaptive_zero_sum(100, ordinates)
    assert math.isfinite(fixed)
    assert math.isfinite(adaptive)
    assert fixed_zero_sum(100, [], 4, 100.0) == 0.0
    with pytest.raises(ValueError):
        fixed_zero_sum(100, [-1.0], 4, 100.0)


@pytest.mark.parametrize("n", [10, 100, 1000])
def test_adaptive_tail_budget_decay(n):
    k = adaptive_k(n)
    t = adaptive_cutoff(n)
    tail_proxy = k * t * 4 ** (-k)
    principal_scale = n
    assert tail_proxy / principal_scale < 1.0
