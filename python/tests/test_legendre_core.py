"""NUMERICAL regression checks; the associated proofs are in docs/."""

import math
import sys
from pathlib import Path

import mpmath as mp
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from legendre_core import (
    kernel, mellin_principal, segmented_sieve, prime_power_bound,
    trivial_zero_bound, weighted_prime_sum, weighted_von_mangoldt_sum,
)
from legendre_analysis import finite_ordinate_sum, zero_sum


def test_segmented_sieve_basic():
    assert segmented_sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_kernel_support():
    n = 10
    x = n * (n + 1)
    h = math.log1p(1 / n)
    assert kernel(n, x * math.exp(-h) * 1.001) > 0
    assert kernel(n, n * n + 1) > 0
    assert kernel(n, (n + 1) ** 2) == 0


def test_principal_term_asymptotic():
    n = 1000
    principal = mellin_principal(n)
    assert abs(principal / n - 1.0) < 0.002


@pytest.mark.parametrize("block_size", [1, 2, 7, 16, 64])
def test_segmented_sieve_against_trial_division(block_size):
    expected = [m for m in range(2, 301)
                if all(m % d for d in range(2, math.isqrt(m) + 1))]
    assert segmented_sieve(300, block_size) == expected


def test_sieve_rejects_empty_block():
    with pytest.raises(ValueError):
        segmented_sieve(30, 0)


@pytest.mark.parametrize("n", [1, 2, 10, 1000, 10**12])
def test_exact_support_and_peak(n):
    assert kernel(n, n * n) == 0
    assert kernel(n, n * n - 1) == 0
    assert kernel(n, (n + 1) ** 2) == 0
    assert kernel(n, n * (n + 1)) == 1
    for offset in [1, n, 2 * n]:
        assert 0 < kernel(n, n * n + offset) <= 1


@pytest.mark.parametrize("n", [1, 2, 10, 1000, 10**12])
def test_principal_against_high_precision_integral(n):
    with mp.workdps(60):
        h = mp.log1p(mp.mpf(1) / n)
        x = mp.mpf(n) * (n + 1)
        reference = x * h * mp.quad(
            lambda v: mp.exp(h * v / 2) * (1 - abs(v)), [-1, 0, 1]
        )
        assert math.isclose(mellin_principal(n), float(reference), rel_tol=5e-15)


@pytest.mark.parametrize("n", [1, 2, 7, 20, 100])
def test_prime_power_error_bound(n):
    upper = (n + 1) ** 2 - 1
    primes = segmented_sieve(upper)
    difference = weighted_von_mangoldt_sum(n, upper) - weighted_prime_sum(n, primes)
    assert -1e-12 <= difference <= prime_power_bound(n) + 1e-12
    assert all(not (n * n < p * p <= upper) for p in primes)


@pytest.mark.parametrize("n", [2, 3, 10, 100])
def test_trivial_zero_integral_bound(n):
    with mp.workdps(40):
        h = mp.log1p(mp.mpf(1) / n)
        x = mp.mpf(n) * (n + 1)
        residue = mp.quad(
            lambda u: mp.exp(-u / 2) * (1 - abs(u) / h)
            / ((x * mp.exp(u)) ** 2 - 1), [-h, 0, h]
        )
        assert 0 < residue < trivial_zero_bound(n)


def test_zero_sum_api_and_precision_restoration():
    old = mp.mp.dps
    with mp.workdps(60):
        gamma = mp.im(mp.zetazero(1))
        h = mp.log(mp.mpf(3) / 2)
        z = gamma * h / 2
        expected = 2 * mp.cos(gamma * mp.log(6)) * (mp.sin(z) / z) ** 2
    assert math.isclose(zero_sum(2, 1), float(expected), rel_tol=1e-14)
    assert zero_sum(2, 0) == 0
    assert finite_ordinate_sum(2, []) == 0
    assert mp.mp.dps == old
    for invalid in [0, -1, float("nan"), float("inf")]:
        with pytest.raises(ValueError):
            finite_ordinate_sum(2, [invalid])


def test_incomplete_mangoldt_range_is_rejected():
    with pytest.raises(ValueError):
        weighted_von_mangoldt_sum(10, 110)
