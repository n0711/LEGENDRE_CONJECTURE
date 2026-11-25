# Computational cost audit

All asymptotic statements are **ESTABLISHED** operation-count bounds for
the specified algorithms. They imply no new prime-existence theorem.
Let `b=ceil(log₂(n+1))`, `ell=ceil(log₂(L+1))`, and let `D(k)` bound
multiplication/division of `k`-bit integers. Word bounds presume the
integer quantities fit a word; conservative bit bounds multiply arithmetic
work by `D(ell)`. No input distribution is supplied, so no distinct
average-case performance theorem is claimed.

## Prime generation, including the inherited implementations

The Python and C++ segmented sieves through `L` with block length `B` use

`O(L log log(L+2) + ceil(L/B) pi(sqrt L))`

word time. The second term is necessary for these implementations: every
block loops over every base prime. Fixed `B` is not an asymptotically
optimal choice as `L` grows. Initializing/scanning the range costs
`Omega(L)` even in the best case. There is no early exit on a prime witness.
Storage is `O(sqrt L+B)` flags plus `pi(L)+pi(sqrt L)` output/base integers;
Python uses bytes for flags and C++ `vector<bool>` uses packed bits.
Output alone requires `Omega(pi(L))` words. The bit model includes the
`O(ell)` bits per integer and integer division during block initialization.

The Python baseline redundantly searched for each already-emitted base
prime in the output, then sorted a set of the whole list. The membership
part took `Theta(pi(sqrt L)^2)` comparisons (the primes occur early in the
ordered list), not necessarily a scan of the entire output each time.
Set construction and sorting incurred additional time and memory. They
were removed; no change in the leading sieve complexity is asserted.
The C++ changes correct integer square-root rounding and prevent overflow
in block endpoints and marking increments, without changing these bounds.
Its scalar type still limits inputs to unsigned 64-bit integers, and
allocation feasibility is a separate constraint.

## Weighted sums and finite zeros

Given a sorted prime list of length `P` and `I` primes in the square
interval, `weighted_prime_sum` costs `O(log(P+1)+I)` word/transcendental
operations. Its list slice uses `O(I)` extra references. Constructing the
prime list is additional. `weighted_von_mangoldt_sum` first generates
all primes through the supplied limit `L`, then visits their powers;
the number of visits is `sum_{k<=log₂L}pi(L^(1/k))=Theta(pi(L))`
as `L` grows. This routine is a small-test oracle, not a proposed efficient
universal verification method. `first_standard_gap` filters all supplied
primes and sorts those retained: `O(P+I log(I+1))` time and `O(I)` storage.

At fixed floating precision, kernel/principal/trivial-zero evaluations
use `Theta(1)` operations. `prime_power_bound` sums `Theta(log n)` terms;
its current `fsum` usage has a conservative `O(log n)` workspace bound.
These word counts exclude growing-precision integer or real arithmetic.
The corrected sinh expression is algebraically identical to the old
cosh expression; it fixes numerical cancellation, not asymptotic cost.

**NUMERICAL regression:** at `n=10^8` and `n=10^12`, the baseline cosh
implementation returns zero; the repaired function returns `n+0.5` in
binary64, agreeing with independent high-precision quadrature in tests.

**ESTABLISHED:**

For a supplied list of `M` ordinates, `finite_ordinate_sum` uses
`Theta(M)` iterations and can stream the list. With working precision `p`
bits and arguments of magnitude at most `T log(n(n+1))`, write `A(p,T,n)`
for the cost of the required multiprecision arithmetic and transcendental
evaluation including argument reduction. Total time is `O(M A(p,T,n))`,
plus `Omega(M)` input reads, with a constant number of working real values.
The final return is rounded to binary64. Increasing internal precision
does not produce a rigorous enclosure. `zero_sum` additionally computes
the first `M` mpmath zeros; add `sum_{j=1}^M Z(j,p)`, where `Z` is the actual
zero-generator cost. No undocumented polynomial bound for `Z` or certified
completeness is claimed. There is no Master-Theorem recurrence here.

For height versus binary-length costs, ordinate accuracy and data
certification obligations, see [L001_TRUNCATION.md](L001_TRUNCATION.md).
For exact Möbius traversal, cube-root binary search (where the Master
Theorem does apply), sieve and semiprime complexities, see
[DISCRETE_SIEVE.md](DISCRETE_SIEVE.md).

## Reproducibility costs and benchmarks

**NUMERICAL:** `scripts/benchmark_discrete_sieve.py` includes preprocessing
and compares four algorithms on the same exact finite outputs. The
recorded five-run benchmark is in `DISCRETE_SIEVE.md`; the current repaired
full-range generator is its baseline. L001's formula-evaluation benchmark
is in its own document. No cross-language speedup is asserted: C++ checks
compare correctness and include compilation in their run time.

**ESTABLISHED:** the 30-row diagnostic generator costs the sum of the two
Bonferroni traversals, one interval sieve and constant-time tail evaluations
per sampled `n`, with their preprocessing included. CSV storage and MATLAB
plotting data are linear in the row count; PDF/PNG rendering cost also
depends on output resolution and renderer. Plotting performs no new sieve
or independent implementation of the mathematical bounds.

Lean toolchain/dependency download and compilation are preprocessing;
the actual versions, selected cache size and compiler/axiom status are
recorded in `LEAN_VERIFICATION.md`. Proof-checking a fixed finite development
is not an algorithm deciding Legendre for all integers. The manuscript is
XeLaTeX source; its build is specified in CI, separately from proof validity.

## PGA generalized-kernel complexity

**ESTABLISHED — adaptive ordinates.**  For
`k(n)=Theta(loglog n)` and `T(n)=Theta(k(n)n)`, the standard zero-count
asymptotic gives `N(T)=Theta(TlogT)=Theta(nlogn loglogn)`.  Evaluating
all supplied ordinates to a fixed precision is
`Theta(nlogn loglogn)`, excluding zero generation, interval certification
and precision-dependent arithmetic.

**ESTABLISHED — fixed-k tail.**  For fixed even `k>=2`, the truncation
bound is `O_k(n^k logT/T^(k-1))`, with no constant made effective here.

**DERIVED — adaptive tail.**  Substituting the adaptive scale gives
`O(knlogT4^-k)=o(n)`, but this claim requires explicit Stieltjes constants
and is not currently a certified numeric bound.
