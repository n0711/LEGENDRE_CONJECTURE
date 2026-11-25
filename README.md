# Prime Graph Algorithm (PGA): Legendre Conjecture Research

Research by Charalampos Nadiotis (GitHub: [@n0711](https://github.com/n0711)).
The project investigates Legendre's conjecture using discrete prime-divisibility
graphs, sieve identities, RH-conditional explicit formulas, C++20, Python and
Lean 4.

> **Research status:** Legendre's conjecture is not proved here. Numerical
> computations and finite verification are not an infinite proof. RH-dependent
> claims are labeled **RH-CONDITIONAL**; formalized lemmas are labeled
> **LEAN-CERTIFIED** in their verification record.

## Research objectives

- Study whether RH or techniques associated with its formal proof can control
  primes in every interval \((n^2,(n+1)^2)\).
- Model the interval by a bipartite graph between candidate integers and
  their prime divisors.
- Derive exact degree, sieve, Möbius, CRT and semiprime identities.
- Audit smooth explicit-formula kernels and seek a rigorous uniform
  one-sided zero-sum bound.
- Formalize established discrete results in Lean without `sorry`, `admit`, or
  custom axioms.

## Mathematical achievements

- **ESTABLISHED:** exact finite Möbius floor identity for square-interval prime counts and
  explicit square-endpoint congruences.
- **ESTABLISHED:** cube-root cutoff reduction: the remaining composite candidates have a
  unique smaller prime factor, yielding an exact aggregate semiprime
  correction.
- **LEAN-CERTIFIED:** PGA degree identity \(L=R-E+W-H\), and the bound
  \(L\ge R-E+2W/3\), formalized for bounded-degree finite graphs.
- **ESTABLISHED:** fixed odd Bonferroni truncations eventually fail as positive lower bounds;
  this does not exclude increasing-depth or optimized sieve methods.
- **RH-CONDITIONAL:** triangular-kernel explicit formula, with documented
  prime-power, trivial-zero and zero-truncation terms.
- **CONJECTURAL:** the decisive uniform cancellation estimate remains open:
  \(C_{n,k(n)}(T)\le(1-\epsilon)n\) for some fixed \(\epsilon>0\) and all
  sufficiently large \(n\).

See the [research handoff](docs/CHATGPT_HANDOFF.md), [publication handoff](docs/PUBLICATION_HANDOFF.md),
[PGA kernel audit](docs/PGA_KERNEL_AUDIT.md), [discrete sieve proofs](docs/DISCRETE_SIEVE.md),
[proof obligations](docs/PROOF_OBLIGATIONS.md), and [Lean verification status](docs/LEAN_VERIFICATION.md).

## Repository contents

- `cpp/`: C++20 PGA and segmented sieve.
- `python/`: exact finite graph/sieve models, kernel diagnostics, and tests.
- `lean/`: Lean 4/Mathlib proofs and axiom-report audit.
- `docs/`: mathematical proofs, complexity, limitations, and handoffs.
- `paper/`: XeLaTeX manuscript source.
- `.github/workflows/validate.yml`: reproducible Python, C++, Lean and TeX checks.

## Reproduce locally

### Python

Python 3.13 is used in CI. Install test/numerical dependencies and run:

```powershell
python -m pip install mpmath pytest
python -m pytest python/tests -q
python scripts/research_diagnostics.py
```

### C++20

With GCC:

```sh
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror \
  cpp/prime_graph.cpp -o prime_graph
./prime_graph 3
python scripts/check_cpp.py
```

The PGA executable prints finite interval graph statistics. It does not decide
Legendre's conjecture. `scripts/check_cpp.py` differentially checks both the
segmented sieve and PGA statistics against Python implementations.

### Lean 4

The pinned toolchain and Mathlib revision are specified under `lean/`.
Install Lean with `elan`, then from the repository root:

```sh
cd lean
lake update
lake exe cache get Mathlib/Analysis/SpecialFunctions/Log/Basic.lean Mathlib/Data/Nat/Prime.lean Mathlib/Order/Interval/Finset/Nat.lean Mathlib/Tactic/FieldSimp.lean Mathlib/Tactic/Linarith.lean Mathlib/Tactic/Positivity.lean Mathlib/Tactic/Ring.lean
cd ..
python lean/audit.py
python -m unittest discover -s lean -p test_audit.py
```

Only the declarations listed in [LEAN_VERIFICATION.md](docs/LEAN_VERIFICATION.md)
are certified. Lean does not prove RH or Legendre's conjecture in this project.

### XeLaTeX

```sh
xelatex -interaction=nonstopmode -halt-on-error -output-directory=paper paper/legendre_research.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=paper paper/legendre_research.tex
```

## Limitations

- No proof or counterexample to Legendre's conjecture is claimed.
- The prime graph and sieve prove classifications and identities, not that
  any interval has a prime.
- The central zero-sum cancellation bound is unproved; RH alone is not being
  used to silently assume localized cancellation or pair-correlation
  conjectures.
- Floating-point zero sums are diagnostic only. No complete certified zero
  list or outward-rounded enclosure is included.
- Finite numerical tests are not evidence of an infinite theorem.
- Algorithmic costs are polynomial or near-linear in the numerical value
  \(n\) for specified operations but exponential in the binary input length
  \(\Theta(\log n)\); see [COMPLEXITY.md](docs/COMPLEXITY.md).
- No implementation is imported from `n0711/P_EQUALS_NP`; that project remains
  separate.

## Citation

Please cite the software using the metadata in [CITATION.cff](CITATION.cff).
The citation metadata identifies this research workspace; it does not assert
that Legendre's conjecture is solved. For a paper citation, use the eventual
versioned preprint only after it has been independently reviewed and released.
