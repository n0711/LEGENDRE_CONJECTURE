# ChatGPT handoff

Updated 2026-11-25, continuing clean commit `f4397dc`. Legendre remains
**CONJECTURAL**; no universal proof is claimed. RH is an explicit assumption
only for statements tagged **RH-CONDITIONAL**.

## 1. New results and proofs

- **ESTABLISHED/DERIVED:** generalized sinc weights are now defined and
  audited; fixed-k truncation has the form
  `O_k(n^k log(T)/T^(k-1))`, adaptive substitution gives the proposed
  `O(kn logT 4^-k)=o(n)` only as a derived bound with constants pending.
- **ESTABLISHED:** prime-power contamination is at least no worse than
  `O(logn loglogn)=o(n)`; the square `(loglogn)^2` claim is a looser bound.
- **ESTABLISHED:** adaptive cutoff ordinates number
  `Theta(n logn loglogn)`.
- **ESTABLISHED:** `Lambda(n(n+1))=0` for n>=2.
- **LEAN-CERTIFIED:** PGA-L007-L009 generic degree identities compile:
  incident-component witness, residual degree <=3, exact `L=R-E+W-H`,
  and `3L>=3R-3E+2W`.
- **NUMERICAL:** targeted PGA tests and strict C++20 compile pass; selected
  C++ n=4264 gives `G=3L-W=15` in the repository's present variable
  convention. This is finite evidence only.
- **IMPLEMENTED:** C++20/Python fixed and adaptive `C_n,k(T)` evaluators
  consume supplied ordinate lists and return floating-point diagnostics only;
  they are not certified enclosures.

- **ESTABLISHED:** loop-state 1 and state 2 transitions, first-residue
  boundary handling, maintenance, and state-0/compositeness classification
  are now implemented and tested through `n<=100` (447 repository tests pass).
  Lean defines the threshold phases and certifies small-phase membership.
  The exact finite-state model is not Legendre's conjecture.

- **ESTABLISHED:** L001 holds for every `n>=1,T>=1`. The requested constants
  follow from Trudgian's original Theorem 2; the optional sharper numerator
  is `0.317 log T+9.89425`. See `L001_TRUNCATION.md`.
- **ESTABLISHED:** the kernel's positive set is `(n²,(n+1)²)`. The previous
  `n²-1` endpoint was wrong. Mellin normalization is `h sqrt(x) C_n`.
- **ESTABLISHED:** prime-power contamination is at most
  `D_n=log(n²+2n) sum_{k=3}^{floor(log₂(n²+2n))}1/k=o(n)`;
  trivial zeros contribute at most `E_n=(2n+1)/(n²(n⁴-1))`, for `n>=2`.
- **ESTABLISHED:** exact Möbius floor identity, square-endpoint congruences,
  and unique semiprime correction after cube-root sieving.
- **ESTABLISHED / FAILED approach:** every fixed odd Bonferroni truncation
  eventually becomes negative, even for the actual square residues.
  This excludes fixed depth, not all combinatorial methods. Full proofs:
  `DISCRETE_SIEVE.md` and `VERIFIED_LEMMAS.md`; no novelty claim.
- **LEAN-CERTIFIED:** 11 elementary lemmas compiled, including both kernel
  endpoints, interval cardinality, small-factor coverage, survivor/primality
  equivalence, and the union-cardinality equivalence. Each axiom audit has
  only `propext`, `Classical.choice`, `Quot.sound`. Details and pinned
  dependencies are in `LEAN_VERIFICATION.md`. L001 is not Lean-certified.

## 2. Assumptions and dependencies

Trudgian's zero-count theorem is a cited external analytic input, specialized
and integrated independently here. L001 as an ordinate statement needs no
RH; the explicit-formula identification does. No pair-correlation,
independence, or GRH hypothesis has been imported silently.
Alpöge's announcement, Sutherland's dated verification report, and selected
source statements were inspected. Their terminal nonvanishing result gives
no extracted square-interval estimate. The enormous external proof was not
replayed locally. See `RH_PROOF_ANALYSIS.md` for exact scope and source hashes.

## 3. Complexity

**ESTABLISHED:** pruned Möbius traversal is `Theta(M)` word operations with
`Omega(n)<=M<=O(n²)`, plus prime generation. Direct interval sieving uses
`O(n log log n+pi(n))` work plus preprocessing and `O(n)` flags. These costs
are exponential in binary input length. Fixed-block preprocessing overhead
is retained in the analysis; variable-branch recursion does not satisfy the
Master Theorem. Zero truncation at `T=Theta(n log n)` needs
`Theta(n log²n)` ordinates for a fixed relative tail budget, plus generation,
completeness checks and precision costs. See the lemma documents and
`COMPLEXITY.md` for model details.

## 4. Experimental evidence and tests

**NUMERICAL:** 347 mathematical Python tests and five Lean-audit runner tests
pass. The C++ sieve passes nine Python
comparisons and three invalid-input checks under WSL g++. Exact finite
counterexamples to shortcuts include `S(4)=3>S(5)=2` and `B_3(100)=0<S(100)=23`.
The modest benchmark compares four exact implementations at `n=30,100,300`,
including preprocessing. MATLAB R2026b successfully exported PNG and vector
PDF diagnostics from 30 rows; regenerate using `scripts/research_diagnostics.py`
and `matlab/legendre_visualization.m`. Outputs are ignored under `data/`.

GitHub Actions now specify Python, C++, Lean axiom auditing, and XeLaTeX
builds. These workflow jobs have not been run on GitHub in this continuation.
XeLaTeX is unavailable locally, so the updated manuscript has not been
compiled here; its mathematical content was reviewed separately.

The inherited scan through `n=10000` is historical finite evidence and was
not rerun in this continuation. Float zero sums and bounds are diagnostics,
not outward-rounded certificates; no certified complete zero list is supplied.

## 5. Failed approaches

- **FALSIFIED:** a degree-two residual candidate need not be `p²q`;
  `n=3,m=15=3·5` is a counterexample.

- **FAILED:** a loop-state invariant alone can prove classification and
  completeness, but it supplies no lower bound forcing state 0 to remain
  nonempty. The universal survivor inequality remains the exact obstruction.

Fixed odd inclusion-exclusion depth fails eventually. Termwise Möbius error
bounds fail already at `n=3`. CRT phases are tied to `-n² mod d`, so uniform
independence is not available. The absolute zero envelope is
**ESTABLISHED** to be `Theta(n log n)`, too large for the `Theta(n)` main term.
The previous target `gap=o(sqrt(x)log x)` would not itself suffice.
See `FAILED_APPROACHES.md`.

## 6. Exact unresolved inequalities

The decisive central obligation remains the uniform bound
`C_{n,k(n)}(4k(n)(n+1)) <= (1-epsilon)n` with fixed epsilon and effective
constants. PGA-L029/L030 are not substitutes until their constants and
generalized principal-term remainder are written rigorously.

**CONJECTURAL:** for every `n>=1`, with `L=n²,U=n²+2n,Q=product_{p<=n}p`,

`sum_{d|Q} mu(d)({L/d}-{U/d}) > -2n product_{p<=n}(1-1/p)`.

Equivalently, for `z=floor(U^(1/3))`,

`S_z(n) > sum_{z<p<=n}[pi(floor(U/p))-pi(floor(L/p))]`.

**RH-CONDITIONAL implication:** a sufficient analytic certificate is

`C_n(T)+B(n,T) < [F(1)-D_n-E_n]/[h sqrt(x)]`.

**RH-CONDITIONAL:** nonnegativity already gives `limsup C_n/n<=1`.
**CONJECTURAL:** the strict `<1` target remains unproved and would imply
many primes per interval, more than the single prime required. An effective
cutoff and finite verification are also needed for a universal conclusion.

## 7. Questions for ChatGPT

Can the tied square phases control the full signed Möbius remainder, rather
than a fixed-degree truncation? Can the aggregate disjoint semiprime correction
be bounded sharply without estimating each bounded-length cofactor interval
separately? Is there a precisely stated, quantitatively stronger intermediate
result in the reported RH development that addresses either inequality?

## 8. Next research objective

The exact remaining analytic target is the uniform one-sided bound
`C_{n,k(n)}(T)<= (1-epsilon)n` with effective constants and explicit
kernel/truncation remainders.

The next candidate is a signed-remainder bound using the consecutive-square
phase `-n² mod d`, or an aggregate bound for residual semiprimes. State
classification is complete; the missing theorem is positivity of the
signed sum.

Seek a uniform bound for the signed remainder or aggregate semiprime correction.
Use increasing-depth/optimized sieve weights only with explicit remainder
control; search for counterexamples before promoting a proposed bound.
Do not spend the next milestone merely extending the finite prime scan or
improving tail constants without progress on the signed margin.
