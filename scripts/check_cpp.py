"""NUMERICAL differential checks for the C++ sieve, including boundary blocks."""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from legendre_core import segmented_sieve
from prime_graph import analyze as analyze_pga


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiler", default="g++")
    args = parser.parse_args()
    cases = [(0, 1), (1, 2), (2, 1), (49, 7), (300, 1),
             (1000, 17), (100000, 65536), (1000000, 65536), (100, 2**64 - 1)]
    with tempfile.TemporaryDirectory(prefix="legendre-cpp-") as work:
        executable = Path(work) / "sieve"
        subprocess.run([args.compiler, "-std=c++17", "-O2", "-Wall", "-Wextra",
                        "-Werror", str(ROOT / "cpp/segmented_sieve.cpp"),
                        "-o", str(executable)], check=True)
        for limit, block in cases:
            result = subprocess.run([str(executable), str(limit), str(block)],
                                    capture_output=True, text=True, check=True)
            expected = len(segmented_sieve(limit))
            assert int(result.stdout) == expected, (limit, block, result.stdout, expected)
        for arguments in [("30", "0"), ("-1",), ("3.5",)]:
            result = subprocess.run([str(executable), *arguments], capture_output=True)
            assert result.returncode != 0
        pga_executable = Path(work) / "pga"
        subprocess.run(
            [args.compiler, "-std=c++20", "-O2", "-Wall", "-Wextra",
             "-Wpedantic", "-Wconversion", "-Wshadow", "-Werror",
             str(ROOT / "cpp/prime_graph.cpp"), "-o", str(pga_executable)],
            check=True,
        )
        for n in (1, 3, 10):
            output = subprocess.run(
                [str(pga_executable), str(n)], capture_output=True, text=True, check=True
            ).stdout.split()
            stats = analyze_pga(n)
            expected = [
                n, stats["R"], stats["E"], stats["degree_one"], stats["W"],
                stats["H"], stats["L"], 1, int(3 * stats["R"] + 2 * stats["W"] > 3 * stats["E"]),
            ]
            assert list(map(int, output)) == expected, (n, output, expected)
    print(
        f"NUMERICAL: {len(cases)} C++/Python sieve comparisons, 3 invalid-input "
        "checks and 3 C++20/Python PGA comparisons passed"
    )


if __name__ == "__main__":
    main()
