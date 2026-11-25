"""NUMERICAL: small diagnostics for the two unresolved proof inequalities."""

import csv
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from discrete_sieve import mobius_survivors, sieve_survivors
from zero_tail import truncation_bound


def main():
    output = ROOT / "data/research_diagnostics.csv"
    output.parent.mkdir(exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["n", "survivors_per_n", "bonferroni_1_per_n",
                         "bonferroni_3_per_n", "tail_kappa_1_per_n",
                         "tail_kappa_10_per_n"])
        for n in range(10, 301, 10):
            writer.writerow([n, len(sieve_survivors(n)) / n,
                             mobius_survivors(n, 1) / n,
                             mobius_survivors(n, 3) / n,
                             truncation_bound(n, n * math.log(n)) / n,
                             truncation_bound(n, 10 * n * math.log(n)) / n])
    print(f"NUMERICAL: 30 diagnostic rows written to {output}")


if __name__ == "__main__":
    main()
