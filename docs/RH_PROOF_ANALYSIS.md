# Riemann Hypothesis Proof Analysis

## External verification reports, checked 2026-11-25

**LEAN-CERTIFIED (externally reported; not replayed locally):** The announcement
archive contains 175,187 Lean modules and claims `RiemannHypothesis` plus four
Dirichlet-L-function statements.  Independent 2026-11-20 through 2026-11-24
build and replay reports describe a successful build, byte-matching statements,
the standard axiom set `{propext, Classical.choice, Quot.sound}`, and acceptance
by several independent or external kernels/checkers.

Primary sources:

- https://alpo.ge/remark.pdf
- https://alpo.ge/lean.tar.gz.part01 through `part14`
- https://github.com/Hertaspace/alpoge-rh-lean-verification
- https://github.com/nasqret/riemann-rev
- https://math.mit.edu/~drew/grh/

The current announcement and Andrew Sutherland's primary report were read
again in this continuation. The report is dated 2026-11-24 05:25 UTC and
distinguishes completed checks from a still-running v4.36 comparator job.
Its reported RH/Dirichlet-GRH scope and axiom audit were checked against its
displayed statements. No local replay of the enormous external proof was
performed. RH remains the user's explicit assumption; no part of this work
depends on deciding the announcement's broader status.

## Inspected intermediate machinery

The published archive is too large to use as a single source of a Legendre
inequality.  The direct terminal statement only supplies RH/GRH.  Any proposed
Legendre use must locate an actual stronger intermediate theorem in the Lean
code or paper; raw RH does not imply any known extra uniform gap bound merely
by the mere fact of a formal proof.

**ESTABLISHED (source inspection, not a local kernel check):** the source
mirror now redirects to
[leanprover-community/riemann-hypothesis](https://github.com/leanprover-community/riemann-hypothesis).
The inspected head was `91b273530883b723ef4422436e0dc3557749325a`.
Files inspected through the GitHub connector:

- [src/Main.lean](https://github.com/leanprover-community/riemann-hypothesis/blob/91b273530883b723ef4422436e0dc3557749325a/src/Main.lean),
  blob `eb95ca808793dd61984cc853ab5630f54a74490c`: the terminal RH theorem
  is deduced from `UpperTheory.FinalTheorems.everyCharacter`.
- [EveryCharacter.lean](https://github.com/leanprover-community/riemann-hypothesis/blob/91b273530883b723ef4422436e0dc3557749325a/src/Development/AutomorphicArithmetic/CharacterBoxes/EveryCharacter.lean),
  blob `9a65d9a696d587236c415d94f2eb8d547b69b15b`: `UpperTheory.EveryCharacter`
  is defined as `DirichletLNonvanishingRightOfHalf`.
- [MainConclusion.lean](https://github.com/leanprover-community/riemann-hypothesis/blob/91b273530883b723ef4422436e0dc3557749325a/src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean),
  blob `d834a44196956df3feb46337ff1c474a986e923d`: inspected the final
  dependency block and theta-lift/geometric realization declarations.
  `everyCharacter_of_row` passes a local-global representation hypothesis
  through `every_character_of_literature_of_vWin` and `vwin_of_row`.

The announcement describes determinant positivity, theta-lift multiplicity,
and trace/Parseval arguments. These descriptions are research leads, not
quantitative square-interval lemmas. The inspected terminal statements give
nonvanishing, and supply no bound on the signed sum `C_n` or the short-interval
Möbius remainder. This is a limited inspection, not a claim that every
intermediate theorem was searched or that stronger results cannot exist.

**RH-CONDITIONAL (literature):**
[Dudek–Grenié–Molteni, Theorem 1.1](https://arxiv.org/html/1503.05403v2#S1.Thmtheorem1)
gives a prime within `(1/2+2/log x)sqrt(x)log x` of every `x>=2` under RH.
The published radius still exceeds the required square-interval radius
asymptotically. Its smoothing and zero-tail method is relevant; it supplies
no justification for removing the logarithmic factor here.

**CONJECTURAL:** transferring determinant positivity or theta-lift estimates
to the signed sieve remainder could help only after a precise quantitative
statement and its assumptions are extracted. None is established in this
workspace; GRH and additional correlation hypotheses are not silently assumed.
