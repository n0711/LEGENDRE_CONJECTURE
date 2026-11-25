"""NUMERICAL regression checks; these do not prove the infinite zero-tail bound."""

import math
import sys
from pathlib import Path

import mpmath as mp
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from zero_tail import ordinate_error_bound, truncation_bound


@pytest.mark.parametrize("n", [1, 2, 10, 1000, 10**12, 2**53])
@pytest.mark.parametrize("cutoff", [1.0, 2.0, 14.0, 1000.0, 1e12, 1e200])
@pytest.mark.parametrize("sharper", [False, True])
def test_tail_matches_independent_high_precision_formula(n, cutoff, sharper):
    with mp.workdps(80):
        h, t = mp.log1p(mp.mpf(1) / n), mp.mpf(cutoff)
        a, b = ("0.317", "9.89425") if sharper else ("0.7", "18.175")
        reference = 8 / h**2 * (
            (mp.log(t / (2 * mp.pi)) + 1) / (2 * mp.pi * t)
            + (mp.mpf(a) * mp.log(t) + mp.mpf(b)) / t**2
        )
        assert math.isclose(truncation_bound(n, cutoff, sharper=sharper),
                            float(reference), rel_tol=2e-14)


def test_abel_error_integral_and_constants():
    # Independent quadrature after t = T exp(u), avoiding an infinite t interval.
    with mp.workdps(60):
        for a, b in [(mp.mpf("0.35"), mp.mpf(9)),
                     (mp.mpf("0.1585"), mp.mpf("4.9075"))]:
            for t in [mp.mpf(1), mp.mpf(14), mp.mpf(1000)]:
                integral = 2 / t**2 * mp.quad(
                    lambda u: (a * (mp.log(t) + u) + b) * mp.exp(-2 * u),
                    [0, mp.inf],
                )
                actual = (a * mp.log(t) + b) / t**2 + integral
                expected = (2*a*mp.log(t) + 2*b + a/2) / t**2
                assert mp.almosteq(actual, expected)


def test_tail_order_and_sharp_improvement():
    for n in [1, 10, 10000]:
        previous = math.inf
        for t in [1, 2, 10, 100, 10000, 1e8]:
            coarse = truncation_bound(n, t)
            sharp = truncation_bound(n, t, sharper=True)
            assert 0 < sharp < coarse < previous
            previous = coarse


def test_finite_actual_zero_block_obeys_tail():
    # Four independently computed ordinates provide a small regression block.
    # No claim of certified zero data or infinite verification is made.
    with mp.workdps(45):
        zeros = [mp.zetazero(k).imag for k in range(1, 5)]
        cutoff = mp.mpf(14)
        inverse_square_block = sum(1/g**2 for g in zeros)
        bound = ((mp.log(cutoff/(2*mp.pi)) + 1)/(2*mp.pi*cutoff)
                 + (mp.mpf("0.7")*mp.log(cutoff)+mp.mpf("18.175"))/cutoff**2)
        assert inverse_square_block < bound
        for n in [1, 2, 10, 1000]:
            h, log_x = mp.log1p(mp.mpf(1)/n), mp.log(n*(n+1))
            block = 2*sum(mp.cos(g*log_x)*mp.sinc(g*h/2)**2 for g in zeros)
            assert abs(block) < truncation_bound(n, float(cutoff))


def test_ordinate_error_bound_and_perturbations():
    for n in [1, 10, 1000]:
        errors = [0.0, 1e-8, 0.01, 0.3]
        h = math.log1p(1/n)
        log_x = math.log(n*(n+1))
        expected = 2*(log_x+h/3)*math.fsum(errors)
        assert math.isclose(ordinate_error_bound(n, iter(errors)), expected,
                            rel_tol=2e-15)
        for g, error in zip([0.0, 14.1, 50.0, 1000.0], errors):
            def term(t):
                z = t*h/2
                return 2*math.cos(t*log_x)*(math.sin(z)/z if z else 1)**2
            assert abs(term(g+error)-term(g)) <= 2*(log_x+h/3)*error + 1e-14
    assert ordinate_error_bound(10, []) == 0


@pytest.mark.parametrize("n", [0, -1, 1.5, True, 2**53+1])
def test_invalid_n(n):
    with pytest.raises(ValueError):
        truncation_bound(n, 10)
    with pytest.raises(ValueError):
        ordinate_error_bound(n, [])


@pytest.mark.parametrize("cutoff", [0, -1, 0.9, math.inf, math.nan])
def test_invalid_cutoff(cutoff):
    with pytest.raises(ValueError):
        truncation_bound(1, cutoff)


@pytest.mark.parametrize("error", [-1, math.inf, math.nan])
def test_invalid_ordinate_error(error):
    with pytest.raises(ValueError):
        ordinate_error_bound(1, [error])
