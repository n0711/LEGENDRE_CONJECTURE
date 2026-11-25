# Exact discrete sieve and its remaining inequality

All claims below are **ESTABLISHED** by the displayed elementary arguments
unless a different category is given. No RH assumption is used. These proofs
have not yet been translated to Lean, and no novelty is claimed.

## Exact inversion and square endpoints

## Loop invariant for the three-state sieve

Let `r=1,...,2n` and `m=n²+r`.  Before processing any prime, every state is
zero.  Processing prime `p` performs exactly:

- if `p<=y`, set every still-eligible offset congruent to `-n² (mod p)` to 1;
- if `p>y`, set only candidates still in state 0 to 2.

Here `start=p-(n² mod p)` gives the first positive offset.  More generally,
the first offset is the least positive residue of `-n² mod p`; if `n²` is
divisible by `p`, that residue is `p`, so `r=p` is the first offset and
`r=0` is not a candidate.  After a complete pass:

- state 0 iff no prime `p<=n` divides `m`, iff `m` is prime;
- state 1 iff a prime `p<=y` divides `m`;
- state 2 iff no prime `p<=y` divides `m` and some prime `y<p<=n` divides `m`.

The maintenance rule is exact because membership is monotone for state 1 and
the large-prime branch has a strict `state==0` guard.  Termination occurs
after all primes in ascending order, and the union of states 1 and 2 is
`covered(n)`.  No counterexample to these classifications was found through
`n<=100`.

For completeness, state 2 candidates must be semiprimes when
`y=floor(cuberoot(n²+2n)`: if `m=pq` has `p<=n<q`, uniqueness follows from
cube-root reduction and the fact that `q` is coprime to the processed
small-prime set.  This is an exact residual decomposition, not a guarantee
that state 0 remains nonempty.

Write `L=n²`, `U=n²+2n`, `H=2n`, `P={p prime:p≤n}`, and
`Q=∏_{p∈P}p`. Empty products have value one. A composite `m∈(L,U]` has a
prime divisor `p≤√m<n+1`, hence `p≤n`. Conversely every prime in this
interval exceeds `n`. Therefore the survivor count is exactly

\[
 S(n)=\pi(U)-\pi(L)
 =\sum_{d\mid Q}\mu(d)\left(\left\lfloor U/d\right\rfloor
                         -\left\lfloor L/d\right\rfloor\right).
\]

Proof: for each `m`, expand `∏_{p∈P}(1−1_{p|m})` and sum. Each subset of
distinct primes corresponds to its squarefree product `d`; the number of
multiples in `(L,U]` is the displayed floor difference. Thus Legendre is
equivalent to `S(n)≥1`, including `n=1`, when `S(1)=2`.

For offsets `m=n²+j`, a subset with product `d` marks exactly
`j≡−n² (mod d)`. CRT gives this one residue class; its phase is determined
by `n²`, so independent phases cannot be assumed. Two special cases are

\[
d\mid n:\quad \lfloor U/d\rfloor-\lfloor L/d\rfloor=2n/d,
\qquad
d\mid n+1,\ d>1:\quad \lfloor U/d\rfloor-\lfloor L/d\rfloor
=2(n+1)/d-1.
\]

The first follows because both endpoints are divisible by `d`. For the
second, the endpoint residues are `1` and `d−1` (equal when `d=2`).

Set `V=∏_{p≤n}(1−1/p)` and

\[
 E(n)=\sum_{d\mid Q}\mu(d)\bigl(\{L/d\}-\{U/d\}\bigr).
 \qquad S(n)=2nV+E(n).
\]

Each nontrivial summand has magnitude less than one; the `d=1` term
vanishes. Consequently the exact rational expression
`2nV−(2^|P|−1)` is a rigorous lower bound. **FAILED:** it is already negative
at `n=3` (`−1`), while `S(3)=2`. This does not establish the stronger
inequality required for all `n`:

\[
 \boxed{E(n)>-2nV.}
\]

**CONJECTURAL:** this boxed inequality for every positive integer `n` is
equivalent to Legendre, not an independent result or a consequence proved
here from RH.

## Bonferroni bounds and a uniform obstruction

For an integer `r≥0`, let

\[
 B_r(n)=\sum_{\substack{d\mid Q\\\omega(d)\le r}}
       \mu(d)(\lfloor U/d\rfloor-\lfloor L/d\rfloor).
\]

For an integer divisible by `t` primes of `P`, its contribution is one if
`t=0`; for `t≥1` it is
`Σ_{j=0}^r (−1)^j binom(t,j)=(−1)^r binom(t−1,r)`, with out-of-range
binomial coefficients zero. The identity follows by Pascal's rule and
telescoping. Therefore `B_r≤S` for odd `r`, and `B_r≥S` for even `r`.

**ESTABLISHED (fixed-degree obstruction).** For every fixed odd `r≥1`,
`B_r(n)<0` for all sufficiently large `n`.

Proof: first use only primes `p≤z=⌊log n⌋`, and put
`a=Σ_{p≤z}1/p`. This tends to infinity: otherwise the Euler products
`∏_{p≤N}(1−1/p)^{-1}` would remain bounded, contradicting their lower
bound `Σ_{m≤N}1/m` obtained by expanding the finite products. If `e_j` is
the degree-`j` elementary symmetric function of these reciprocals, then

\[
 e_0=1,\quad e_1=a,\quad
 e_j=a^j/j!+O_j(a^{j-2})\quad(j\ge2).
\]

Indeed, the distinct-index terms in `a^j` sum to `j!e_j`; the repeated-index
terms are at most `binom(j,2)(Σ_p p^{-2})a^{j−2}`, by choosing an equal
pair of positions. The square sum is bounded by `Σ_{m≥2}m^{-2}`. Replacing
each floor difference by `2n/d` costs at most
`Σ_{j≤r} binom(π(z),j)=O_r((1+z)^r)`. The restricted partial sum is thus

\[
 -\frac{2n}{r!}a^r+O_r(n a^{r-1})+O_r((1+\log n)^r)<0
\]

eventually, since `a→∞` and `(log n)^r/n→0`. Adding more sieving primes
cannot increase an odd-degree partial sum: its pointwise value changes
from one to zero when `t` changes from zero to one, and thereafter is
`−binom(t−1,r)`, a nonincreasing function of `t`. This proves the claim.

**FAILED:** any fixed-depth inclusion-exclusion lower bound eventually
loses positivity even with the actual square-interval residues. RH does
not remove this unconditional obstruction. This result does not rule out
depth increasing with `n`, optimized sieve weights, or a proof controlling
the complete signed remainder.

## Disjoint residual composites after a small-prime sieve

Let `z=⌊U^(1/3)⌋` and let `S_z(n)` count members of `A_n` with no prime
factor at most `z`. A surviving composite has at least two prime factors
counted with multiplicity, but cannot have three: each would exceed `z`,
giving a product at least `(z+1)^3>U`. It is therefore `pq` with primes
`z<p≤q`. There are no integer squares in `A_n`, so `p<q`. The smaller
factor is at most `n`; the larger exceeds `n`, since otherwise `pq≤n²`.
Unique factorization makes these residual classes disjoint. Hence

\[
 S(n)=S_z(n)-R_z(n),\qquad
 R_z(n)=\sum_{z<p\le n}
       [\pi(\lfloor U/p\rfloor)-\pi(\lfloor n^2/p\rfloor)].
\]

The lower bound on `q` automatically exceeds `n≥p`, so no extra condition
inside the prime counts is needed. The empty-sum cases `n=1,2` also hold.
For every prime `p>z`, the two reduced endpoints are less than
`(z+1)²`; a surviving cofactor greater than one below this threshold is
itself prime. This explains why the residual composite classes are
disjoint after the initial sieve.

**CONJECTURAL:** proving `S_z(n)>R_z(n)` uniformly is again exactly the
remaining problem. The decomposition gives no independence assumption and
no unexplained favorable sign. The required local prime counts have
interval lengths at most `2n/p+1`; for `p` near `n` these are bounded.
**FAILED:** replacing each such count by its length times a density is
not a rigorous inequality. No RH-assisted bound controlling their total
error sufficiently sharply has been established in this milestone.

## Algorithms and complexity

**ESTABLISHED.** Let `b=⌈log₂(n+1)⌉`, `k=π(n)`, and let `D(b)` dominate
integer multiplication and division on `O(b)`-bit integers. Word-operation
counts below assume such integers fit a word; bit costs are stated
separately. All routines are deterministic, with no average-case claim
because no input distribution is specified.

Reuse of `legendre_core.segmented_sieve(v)` includes generation costs.
For block length `B`, a valid upper bound for its word time is
`G(v)=O(v log log(v+2)+ceil(v/B)π(√v))`; the second term counts scanning
all base primes for every block. Its stored output costs `π(v)` words,
plus `O(√v+B)` bytes of sieve storage. This implementation scans the full
range and has time `Ω(v)` even in its best case. With fixed `B`, its
base-prime loop term must not be silently dropped in an asymptotic claim.

- `mobius_survivors`: products `d>U` contribute zero and are pruned before
  recursion. If `M_r` is the number of squarefree products `d≤U` of at most
  `r` primes from `P`, including one, traversal costs `Θ(M_r)` word
  operations: each accepted edge creates one node, and each node tests at
  most one failed product before breaking. The full sum has
  `M≤min(2^k,U)`, hence `O(n²)` traversal time. It also has `M=Ω(n)`:
  every squarefree integer at most `n` is a node, and the number excluded
  by square divisibility is at most
  `n Σ_{a≥2}1/a²≤3n/4`. This lower bound does not assert `Θ(n²)`.
  Recursion depth is `O(b)` because each new prime is at least two.
  Excluding prime generation, auxiliary storage is `O(k+b)` words,
  and bit time is `O(M_r D(b))`. Recursive subtotals have `O(b)` bits:
  a crude absolute sum bound is `O(U²)`.
  The recurrence is `T(d,i,r)=Σ_{allowed j≥i}T(dp_j,j+1,r−1)+O(1+#children)`;
  variable branching and unequal child sizes prevent application of the
  Master Theorem. An unpruned enumeration has `2^k` subsets, even though
  most of their floor terms vanish.
- `sieve_survivors`: marks the interval directly, with
  `O(n+Σ_{p≤z}(2n/p+1))+G(z)` word time for cutoff `z≤n`, hence
  `O(n log log(n+2)+π(n))+G(n)` in the full case. The output scan and flag
  initialization force `Ω(n)` best- and worst-case time. Auxiliary storage
  is `O(n)` bytes plus the primes and returned integers. A conservative
  bit upper bound multiplies these word costs by `D(b)`; the actual flag
  stores are single bytes. This is exponential in binary input length,
  since `n=2^{Θ(b)}`, despite being nearly linear in numerical `n`.
- `cube_root_floor`: integer binary search has recurrence
  `T(w)=T(⌈w/2⌉)+Θ(1)` on search-range width `w`; Master Theorem applies
  with `a=1,b=2`, giving `Θ(log(value+2))` word iterations. Bit time is
  `O(ell D(ell))` and storage `O(ell)` bits, where `ell` is the input bit
  length. It uses no floating approximation.
- `semiprime_split`: generate all primes up to
  `v=⌊U/(z+1)⌋=Θ(n^(4/3))`, compute the partial interval sieve, and use two
  binary searches for every `z<p≤n`. Time is
  `G(v)+O(n log log(n+2)+k log(v+2))`; space is the interval flags, returned
  rough integers, and `π(v)` stored primes, plus generator workspace.
  The displayed bound includes the expensive cofactor-prime data, and
  does not claim a better counting algorithm than direct interval sieving.
- `density_lower_bound`: products forming the rational density have at
  most `O(kb)` bits. A conservative schoolbook bit upper bound is
  `O(k(kb)^2)+` prime-generation cost (including exact fraction reduction);
  storage is `O(kb)` bits plus generator workspace. This diagnostic is
  not used to replace the exact signed sum.

**ESTABLISHED.** The finite experiments use integer and rational
arithmetic, so there is no precision budget or zero-data generation cost.
Their favorable operation counts do not prove any infinite assertion.

## Tests, counterexamples, and small benchmark

**NUMERICAL.** `python -m pytest python/tests/test_discrete_sieve.py -q`
passes 228 tests. Exact inversion and direct marking are compared against
independent trial division for `1≤n≤80`; Bonferroni bounds are checked
against pointwise binomial sums for `1≤n≤40` and degrees zero through six;
the semiprime split and unique factors are checked for `1≤n≤100`.
Integer cube-root tests include numbers with more than 700 bits.

**NUMERICAL.** Counterexamples to plausible shortcuts:
`S(4)=3>S(5)=2` disproves monotonicity of survivor counts;
`B₁(6)=0<S(6)=4`, `B₁(7)=−3`, and `B₃(100)=0<S(100)=23` defeat positive
lower bounds from these truncations. They do not contradict Legendre.

**NUMERICAL.** Reproduce with `python scripts/benchmark_discrete_sieve.py`.
Medians of five complete calls, including prime generation, on Windows 11,
Python 3.13.16 (AMD64 Family 23 Model 96), in milliseconds:

| n | Exact count | Möbius | Interval sieve | Semiprime split | Current core sieve through U |
|---:|---:|---:|---:|---:|---:|
| 30 | 8 | 0.0756 | 0.0183 | 0.0298 | 0.1018 |
| 100 | 23 | 0.7150 | 0.0296 | 0.0599 | 0.6619 |
| 300 | 56 | 5.1102 | 0.0769 | 0.1865 | 5.2285 |

**NUMERICAL.** The full-range baseline calls the current repaired core sieve,
after removal of its redundant final membership checks and sorting; these
are not timings of the untouched `f4397dc` implementation. The short, variable
timings compare Python implementations and verify equal answers. They are
not asymptotic evidence, a C++ benchmark,
or a reason to run a larger scan. The research objective is a uniform bound
on `E(n)` or on `R_z(n)−S_z(n)`, rather than additional finite prime counts.
