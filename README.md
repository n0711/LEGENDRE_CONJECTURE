# Legendre Conjecture Research

Research code and documentation for exact discrete sieve identities and
RH-conditional triangular-kernel bounds for Legendre's conjecture.

This repository does not claim that Legendre's conjecture has been solved.

## Layout

- `python/`: prime/zero numerical computations and tests.
- `cpp/`: segmented sieve and integration hooks.
- `lean/`: formalized established and conditional lemmas.
- `docs/`: research log, audit, obligations, and handoff.
- `paper/`: XeLaTeX research paper.
- `scripts/`: reproducible validation entry points.

## Prime Graph Algorithm (PGA)

PGA is the current graph-theoretic development by Charalampos Nadiotis.
Its finite C++20 implementation is [prime_graph.cpp](cpp/prime_graph.cpp),
with independent Python checks in [test_prime_graph.py](python/tests/test_prime_graph.py).
The kernel audit is in [PGA_KERNEL_AUDIT.md](docs/PGA_KERNEL_AUDIT.md).
PGA reuses no code or implementation claim from `n0711/P_EQUALS_NP`;
that repository remains separate.

## Quick start

```powershell
python -m pytest python/tests
python scripts/benchmark_discrete_sieve.py
python scripts/check_cpp.py
python scripts/research_diagnostics.py
```

The C++ check requires `g++`. For MATLAB figures run
`matlab -batch "addpath('matlab'); legendre_visualization"` after diagnostics.
The legacy finite-scan CLI remains available, but larger scans do not address
the unresolved proof inequalities. The misleading unused `--zero-count` flag
was removed; finite zero sums are available through `legendre_analysis.zero_sum`.

Start with [the handoff](docs/CHATGPT_HANDOFF.md),
[exact sieve proofs](docs/DISCRETE_SIEVE.md),
[L001](docs/L001_TRUNCATION.md), and
[Lean verification](docs/LEAN_VERIFICATION.md).
The manuscript is `paper/legendre_research.tex`; build from the repository
root with `xelatex -interaction=nonstopmode -halt-on-error -output-directory=paper paper/legendre_research.tex`
(twice for references). See [the cost audit](docs/COMPLEXITY.md) for input-size,
preprocessing and precision costs.
