import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from legendre_core import kernel, mellin_principal, segmented_sieve


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
