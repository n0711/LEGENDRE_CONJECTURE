"""NUMERICAL experiments only; zero lists and floating outputs are uncertified."""

import argparse
from bisect import bisect_left, bisect_right
import csv
import json
import math
from pathlib import Path

import mpmath as mp

from legendre_core import kernel, mellin_principal, segmented_sieve, weighted_prime_sum


def finite_ordinate_sum(n: int, ordinates, dps: int = 50) -> float:
    """NUMERICAL C_n(T); ordinates must be complete to T for L001 to apply.

    This function does not certify zeros, completeness, or floating-point error.
    Pass strings or high-precision numbers to avoid prior binary64 rounding.
    """
    if n < 1 or dps < 15:
        raise ValueError("require n >= 1 and dps >= 15")
    with mp.workdps(dps):
        x = mp.mpf(n) * (n + 1)
        h = mp.log1p(mp.mpf(1) / n)
        total = mp.mpf(0)
        for gamma in ordinates:
            g = mp.mpf(gamma)
            if not mp.isfinite(g) or g <= 0:
                raise ValueError("ordinates must be positive and finite")
            z = g * h / 2
            total += 2 * mp.cos(g * mp.log(x)) * (mp.sin(z) / z) ** 2
        return float(total)


def zero_sum(n: int, zero_count: int, dps: int = 50) -> float:
    """NUMERICAL sum over the first zero_count mpmath approximations."""
    if n < 1 or zero_count < 0 or dps < 15:
        raise ValueError("require n >= 1, zero_count >= 0, dps >= 15")
    with mp.workdps(dps):
        return finite_ordinate_sum(
            n, (mp.im(mp.zetazero(k)) for k in range(1, zero_count + 1)), dps
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-max", type=int, default=10000)
    parser.add_argument("--output-dir", type=Path, default=Path("data"))
    args = parser.parse_args()
    if args.n_max < 1:
        parser.error("--n-max must be positive")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    limit = (args.n_max + 1) ** 2
    primes = segmented_sieve(limit)

    csv_path = args.output_dir / "legendre_scan.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["n", "weighted_sum", "principal", "prime_count", "prime_interval"])
        failures = []
        for n in range(1, args.n_max + 1):
            weighted = weighted_prime_sum(n, primes)
            principal = mellin_principal(n)
            count = bisect_left(primes, (n + 1) ** 2) - bisect_right(primes, n * n)
            if not count:
                failures.append(n)
            writer.writerow([n, format(weighted, ".17g"), format(principal, ".17g"), count,
                             json.dumps(count > 0)])

    summary = {
        "n_max": args.n_max,
        "prime_limit": limit,
        "prime_count": len(primes),
        "status": "NUMERICAL",
        "failures": failures[:100],
        "failure_count": len(failures),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
