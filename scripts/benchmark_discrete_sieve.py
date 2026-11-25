"""NUMERICAL: modest reproducible timings of exact sieve identity checks."""

import argparse
import json
import platform
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "python"))

from discrete_sieve import mobius_survivors, semiprime_split, sieve_survivors
from legendre_core import segmented_sieve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, nargs="+", default=[30, 100, 300])
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if args.repeats < 1 or any(n < 1 for n in args.n):
        parser.error("n and repeats must be positive")
    algorithms = {
        "mobius": mobius_survivors,
        "interval": lambda n: len(sieve_survivors(n)),
        "semiprime": lambda n: semiprime_split(n)[2],
        "baseline_full": lambda n: sum(p > n * n for p in segmented_sieve(n * n + 2 * n)),
    }
    rows = []
    for n in args.n:
        expected = None
        for name, algorithm in algorithms.items():
            elapsed = []
            for _ in range(args.repeats):
                start = time.perf_counter()
                result = algorithm(n)
                elapsed.append(time.perf_counter() - start)
                if expected is None:
                    expected = result
                if result != expected:
                    raise AssertionError((n, name, result, expected))
            rows.append({"n": n, "algorithm": name, "count": expected, "median_ms": round(statistics.median(elapsed) * 1000, 4)})
    print(json.dumps({"category": "NUMERICAL", "python": sys.version.split()[0], "platform": platform.platform(), "repeats": args.repeats, "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
