# Research Log

## 2026-11-25

- Inspected the requested workspace; it was empty and not a Git repository.
- Searched for the exact target repository on GitHub: no public repository was
  found under `n0711/LEGENDRE_CONJECTURE`.
- Verified original Alpöge announcement source and several independent
  verification reports.
- Initialized a new workspace implementation.
- Historical support audit was incorrect; see the correction below.
- **NUMERICAL:** ran a finite Legendre scan through `n=10000`; 5,762,536 primes were sieved
  and no counterexample or missing interval was found.

## 2026-11-25 continuation from f4397dc

- **ESTABLISHED:** corrected positive support to `(n²,(n+1)²)`, proved the
  Mellin normalization and explicit prime-power/trivial-zero bounds.
- **ESTABLISHED:** proved L001 for `T>=1`, checked Trudgian's original
  constants, and derived an ordinate-error budget. No certified zero data
  or interval-arithmetic verification is claimed.
- **ESTABLISHED:** derived exact Möbius inversion and semiprime identities;
  proved every fixed odd Bonferroni truncation eventually negative.
- **ESTABLISHED:** implemented and tested the supplied three-state loop
  boundaries and maintenance rules. State 0 is exactly the prime set;
  state 1 is threshold-eliminated; state 2 is a large-prime residual.
- **LEAN-CERTIFIED:** the threshold-phase membership lemma compiled and
  is consistent with the same standard three-axiom report.
- **AUDITED:** generalized sinc weights, adaptive k/T, fixed-k truncation
  form and adaptive zero count.  PGA-L029 is retained with constants pending;
  PGA-L030 and PGA-L028 remain unproved.  The degree-two p²q claim was
  falsified by `n=3,m=15`.
- **PUBLICATION:** added `docs/PUBLICATION_HANDOFF.md` with lemma inventory,
  literature links, reproducibility commands and remaining proof blockers.
- **LEAN-CERTIFIED:** compiled 11 elementary reduction lemmas with pinned
  Lean/Mathlib and only the standard three axioms; see the verifier record.
- **NUMERICAL:** 347 formula/identity checks, five Lean-audit runner checks,
  and 12 C++ checks passed. MATLAB produced
  diagnostic figures. The large historical scan was not repeated.
- Inspected the reported RH proof's terminal dependency chain; no stronger
  short-interval result was extracted. RH remains an explicit assumption.
- **CONJECTURAL:** the signed sieve remainder and zero-sum margin remain
  unresolved; exact inequalities and next objectives are in the handoff.
- Updated the XeLaTeX manuscript and configured Python/C++/Lean/LaTeX CI.
  XeLaTeX is not installed locally; the manuscript build and remote Actions
  execution remain unverified. This does not alter the local Lean result.
