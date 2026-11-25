"""NUMERICAL evaluations of the ESTABLISHED bounds in docs/L001_TRUNCATION.md.

Binary64 results are diagnostics, not outward-rounded certificates.  The
mathematical tail theorem is independent of RH; using its ordinate sum in the
prime explicit formula is RH-CONDITIONAL.  This module neither generates nor
certifies a complete zero list.
"""

import math
from collections.abc import Iterable


def _parameters(n: int) -> tuple[float, float]:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be an integer >= 1")
    # Limit diagnostics to exactly representable integer input, not a theorem limit.
    if n > 2**53:
        raise ValueError("binary64 diagnostics require n <= 2**53")
    return math.log1p(1.0 / n), math.log(n) + math.log(n + 1)


def truncation_bound(n: int, cutoff: float, *, sharper: bool = False) -> float:
    """NUMERICAL: evaluate B(n,T), for n >= 1 and finite T >= 1.

    With sharper=True use the direct Trudgian constants (0.317, 9.89425)
    instead of the requested relaxed constants (0.7, 18.175).  Both formulas
    are ESTABLISHED in exact real arithmetic.  Zeros at T belong in C_n(T).
    """
    h, _ = _parameters(n)
    cutoff = float(cutoff)
    if not math.isfinite(cutoff) or cutoff < 1.0:
        raise ValueError("cutoff must be finite and >= 1")
    log_t = math.log(cutoff)
    a, b = (0.317, 9.89425) if sharper else (0.7, 18.175)
    # Algebraically B = 8/h^2 * [main/T + remainder/T^2].
    # Dividing sequentially avoids overflow from T^2 and cancellation in log(T/tau).
    scaled_t = h * cutoff
    main = (log_t - math.log(math.tau) + 1.0) / math.tau / scaled_t
    remainder = (a * log_t + b) / cutoff / scaled_t
    return (8.0 / h) * (main + remainder)


def ordinate_error_bound(n: int, absolute_errors: Iterable[float]) -> float:
    """NUMERICAL: bound ordinate perturbations for a fixed, complete zero list.

    ESTABLISHED in real arithmetic: |delta C| <=
    2*(log(n(n+1)) + h/3)*sum_j |delta gamma_j|.
    This excludes missing zeros, multiplicity errors, uncertain cutoff
    membership, and arithmetic evaluation error.
    """
    h, log_x = _parameters(n)

    def validated():
        for error in absolute_errors:
            error = float(error)
            if not math.isfinite(error) or error < 0.0:
                raise ValueError("absolute errors must be finite and nonnegative")
            yield error

    return 2.0 * (log_x + h / 3.0) * math.fsum(validated())
