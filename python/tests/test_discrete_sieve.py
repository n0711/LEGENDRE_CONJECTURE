"""NUMERICAL: finite independent checks of the established sieve identities."""

import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from discrete_sieve import (
    cube_root_floor,
    density_lower_bound,
    mobius_survivors,
    semiprime_split,
    sieve_survivors,
)


def is_prime_trial(value):
    return value >= 2 and all(value % d for d in range(2, math.isqrt(value) + 1))


def expected_primes(n):
    return [m for m in range(n * n + 1, (n + 1) ** 2) if is_prime_trial(m)]


@pytest.mark.parametrize("n", range(1, 81))
def test_exact_mobius_and_union_against_trial_division(n):
    expected = expected_primes(n)
    assert mobius_survivors(n) == len(expected)
    assert sieve_survivors(n) == expected
    assert density_lower_bound(n) <= len(expected)


@pytest.mark.parametrize("n", range(1, 41))
def test_bonferroni_against_pointwise_binomial_identity(n):
    primes = [p for p in range(2, n + 1) if is_prime_trial(p)]
    actual = len(expected_primes(n))
    multiplicities = [sum(m % p == 0 for p in primes) for m in range(n * n + 1, (n + 1) ** 2)]
    for degree in range(7):
        direct = sum(
            sum((-1) ** j * math.comb(t, j) for j in range(min(degree, t) + 1))
            for t in multiplicities
        )
        result = mobius_survivors(n, degree)
        assert result == direct
        assert result <= actual if degree % 2 else result >= actual


@pytest.mark.parametrize("n", range(1, 101))
def test_semiprime_correction_and_unique_factor_structure(n):
    upper = n * n + 2 * n
    z = min(n, cube_root_floor(upper))
    rough = sieve_survivors(n, z)
    residual = [m for m in rough if not is_prime_trial(m)]
    for m in residual:
        pairs = [(p, m // p) for p in range(z + 1, n + 1) if m % p == 0 and is_prime_trial(p)]
        assert len(pairs) == 1
        p, q = pairs[0]
        assert z < p <= n < q and is_prime_trial(q)
    assert semiprime_split(n) == (len(rough), len(residual), len(expected_primes(n)))


def test_cube_root_integer_boundaries_and_large_precision():
    for root in list(range(1, 100)) + [2 ** 60, 10 ** 80 + 37]:
        for delta, expected in [(-1, root - 1), (0, root), (1, root)]:
            value = root ** 3 + delta
            result = cube_root_floor(value)
            assert result == expected
            assert result ** 3 <= value < (result + 1) ** 3
    assert cube_root_floor(0) == 0


def test_counterexamples_and_small_exact_values():
    assert density_lower_bound(1) == 2
    assert density_lower_bound(5) == Fraction(-13, 3)
    assert mobius_survivors(5) == 2
    # A prime count need not increase with n; a union bound can be nonpositive.
    assert mobius_survivors(4) == 3 > mobius_survivors(5)
    assert mobius_survivors(6, degree=1) == 0
    assert mobius_survivors(6) == 4
    assert mobius_survivors(7, degree=1) == -3
    assert mobius_survivors(100, degree=3) == 0
    assert mobius_survivors(100) == 23


def test_square_endpoint_divisor_identities():
    for n in range(1, 101):
        for d in range(1, n + 2):
            actual = sum(m % d == 0 for m in range(n * n + 1, (n + 1) ** 2))
            if n % d == 0:
                assert actual == 2 * n // d
            if d > 1 and (n + 1) % d == 0:
                assert actual == 2 * ((n + 1) // d) - 1


@pytest.mark.parametrize("bad", [0, -1, True, 1.5])
def test_invalid_n(bad):
    for function in (mobius_survivors, sieve_survivors, semiprime_split, density_lower_bound):
        with pytest.raises(ValueError):
            function(bad)


def test_invalid_cutoffs_and_degrees():
    for bad in (-1, True, 1.5):
        with pytest.raises(ValueError):
            mobius_survivors(5, bad)
        with pytest.raises(ValueError):
            cube_root_floor(bad)
    for bad in (-1, 6, True, 1.5):
        with pytest.raises(ValueError):
            sieve_survivors(5, bad)
