# Publication handoff

**ESTABLISHED / PUBLICATION PLANNING — 2026-11-25**

## Proposed title and author

**Prime Graph Algorithm (PGA): A Computational and Graph-Theoretic
Investigation of Legendre's Conjecture**

Author: Charalampos Nadiotis (n0711).

## Abstract candidate

We formulate a bipartite prime-divisibility graph for consecutive-square
integer intervals and derive exact vertex, edge, degree-two and degree-three
identities after a cube-root cutoff.  We separate exact combinatorial
results, RH-conditional explicit-formula estimates, numerical diagnostics,
and conjectural uniform cancellation.  We also audit generalized
sinc-power kernels and document the remaining one-sided zero-sum bound.
Finite experiments, C++20 implementations and Lean 4 certificates support
the discrete components.  The work does not claim a solution of Legendre's
conjecture.

## Scope and status

This handoff is publication preparation only.  The repository is not proof
of Legendre's conjecture.  Every statement must retain one of the project
status tags.

## Complete lemma inventory

### Established

- K001: exact kernel support and Mellin normalization.
- K002: higher prime-power bound \(O(\log n\log\log n)\).
- K003: RH-dependent explicit formula and exact zero sum.
- K004: trivial-zero bound \(O(n^{-5})\).
- K005: finite positive-prime criterion.
- K006: absolute-zero-envelope obstruction.
- L001: explicit zeta-zero truncation constants.
- Exact Möbius floor identity and square endpoint congruences.
- Cube-root semiprime decomposition and smaller-factor uniqueness.
- Fixed odd Bonferroni depth obstruction.
- Loop initialization, maintenance, termination and state classification.
- PGA-L007: non-isolated vertices have incident edges.
- PGA-L008: residual degree is at most two after the cube-root cutoff.
- PGA-L009: \(L=R-E+W-H\) and \(L\ge R-E+2W/3\).
- PGA-L029, form verified: fixed-k tail
  \(O_k(n^k\log T/T^{k-1})\), constants remain pending.
- PGA-L031: prime-power contribution \(o(n)\).

### RH-conditional

- Explicit-formula identification of the zeta-zero sum.
- The sufficient finite inequality for prime positivity.
- Candidate strict margin
  \(C_{n,k(n)}(T)\le(1-\epsilon)n\).

### Conjectural

- Uniform one-sided cancellation with fixed \(\epsilon>0\).
- PGA-L028: generalized smooth-kernel criterion.
- Effective threshold and explicit constants.

### Numerical

- Independent C++20 and Python identities.
- Degree-two counterexample and fixed-Bonferroni counterexamples.
- No certified complete zero list or outward-rounded enclosure.

### Failed or falsified

- Degree-two \(p^2q\) factorization: \(n=3,m=15=3\cdot5\).
- Fixed odd Bonferroni lower bounds.
- Monotone survivor induction.
- Independent CRT phases.
- Absolute zero sum as a positivity certificate.
- Semiprime density substitution without remainder control.

## Original contributions supported here

The repository may claim:

1. An exact presentation of the consecutive-square interval as a finite
   prime-divisibility graph with explicit state transitions.
2. A machine-checked generic formula for degree-zero vertex counts
   \(L=R-E+W-H\) and the \(2W/3\) lower bound.
3. Independent implementation and documentation of the exact cube-root
   residual decomposition.
4. A written audit distinguishing fixed-k, adaptive-k and two-scale forms.
5. Reproduction and formalization of the fixed-Bonferroni obstruction.

It may not claim novelty for standard explicit formulas, sieve identities,
zero-count asymptotics, or RH/GRH machinery without a literature-specific
technical comparison.

## C++ and Python algorithms

- **ESTABLISHED:** C++20 PGA uses two `2n` candidate arrays and an implicit residual graph.
  It sieves primes only through `n`, eliminates small-prime multiples, and
  counts residual prime-divisor degrees in the square interval.
- **NUMERICAL:** Python PGA independently computes the same interval statistics with
  byte-array sieving; tests compare the C++ output against this reference and
  compare the resulting prime count against trial division.
- Fixed and adaptive sinc-power weights:
  `fixed_kernel_weight`, `fixed_zero_sum`,
  `adaptive_k`, `adaptive_cutoff`, `adaptive_zero_sum`.
- Strict C++ build:
  `g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror`.

## Complexity

- **ESTABLISHED:** C++20 PGA graph analysis takes \(\Theta(n\log\log n)\) word operations and
  \(\Theta(n)\) bytes, including prime generation and candidate processing.
  Its \(b\)-bit input cost is \(\Theta(2^b\log b)\) word operations and is
  exponential in \(b\).
- Binary input length: \(b=\Theta(\log n)\); these algorithms are exponential
  in \(b\).
- **ESTABLISHED:** residual graph edges are counted implicitly while enumerating prime
  multiples; maximum candidate degree is two after the cube-root cutoff.
- Adaptive zero evaluation: \(\Theta(n\log n\log\log n)\), excluding
  zero generation and certified arithmetic.
- Master Theorem: applicable only to balanced recursive cube-root and
  divide-range procedures, not variable-prime recursion.

## Reproducible experimental results

Commands:

```powershell
python -m pytest python/tests/test_prime_graph.py -q
python -m pytest python/tests -q
g++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Wconversion -Wshadow -Werror
    cpp/prime_graph.cpp -o prime_graph
```

**NUMERICAL:** GCC 15.2 strict C++20 validation under WSL passed 9 segmented
sieve comparisons, 3 invalid-input cases, and 3 differential PGA cases.
The targeted PGA Python suite passed 1,012 tests; this is finite
implementation evidence, not a prime-existence proof.

Lean audit:

```sh
lake env lean LegendreAudit.lean
```

No numerical result is a proof.  No certified zero list is included.

## Lean verification

The pinned source, when compiled in the cached Lean 4.8.0/Mathlib mirror,
reports only `propext`, `Classical.choice`, and `Quot.sound` for the
PGA-L007–L009 declarations.  It does not prove Legendre's conjecture,
RH, a zero-sum bound or L001.

## Counterexample certificates

1. \(n=3,m=15=3\cdot5\): degree-two residual candidate, not \(p^2q\).
2. \(S(4)=3>S(5)=2\): no monotone survivor induction.
3. \(B_3(100)=0<S(100)=23\): fixed Bonferroni lower bound fails.
4. `density_lower_bound(3)<0` while the exact survivor count is positive:
  termwise Möbius envelope is not a proof.

## Remaining proof obligation

For fixed \(\epsilon>0\), prove uniformly for sufficiently large \(n\):
\[
C_{n,k(n)}(4k(n)(n+1))\le(1-\epsilon)n,
\]
with explicit normalized principal term, prime-power, trivial-zero,
zero-tail and arithmetic rounding bounds.

PGA-L029 and PGA-L030 remain separate: tail formulas are not substitutes
for a one-sided zero-sum theorem.

## Recommended article structure

1. Problem statement and scope.
2. Discrete interval graph.
3. Cube-root reduction and semiprimes.
4. Möbius and inclusion-exclusion identities.
5. RH explicit-formula kernel.
6. Adaptive zero-sum analysis.
7. C++20, Python and Lean verification.
8. Counterexamples and failed strategies.
9. Remaining obstacle.
10. Reproducibility and bibliography.

## Verified bibliography

- Dudek, Grenié and Molteni, *Primes in explicit short intervals on RH*,
  arXiv:1503.05403, DOI 10.48550/arXiv.1503.05403,
  https://arxiv.org/abs/1503.05403
- NIST Digital Library of Mathematical Functions, §25.10 Zeros,
  http://dlmf.nist.gov/25.10
- Alpöge, *Riemann hypothesis formal announcement note*, 20 Nov 2026,
  https://alpo.ge/remark.pdf
- Independent Lean verification record, Hertaspace,
  https://github.com/Hertaspace/alpoge-rh-lean-verification
- Riemann proof status and reading map, nasqret,
  https://github.com/nasqret/riemann-rev
- Andrew Sutherland RH/GRH Lean verification page,
  https://math.mit.edu/~drew/grh/
- Titchmarsh, *The Theory of the Riemann Zeta-Function*, 2nd ed.,
  revised by Heath-Brown, Oxford Science Publications.

## Commit references

- `f4397dc`: initial workspace and baseline.
- `e3a87c6`: L001 and exact sieve reductions.
- `721c271`: exact loop invariants and threshold phase audit.
- `35ab109`: PGA graph/degree lemmas and kernel audit.
- `2f25bd6`: publication research audit and kernel diagnostics.
- `68858ec`: release README/CITATION, interval-marking PGA, and strict C++ checks.
- `0d94fb2`: removed local environment details from the current Lean audit notes.
