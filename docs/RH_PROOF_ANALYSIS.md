# Riemann Hypothesis Proof Analysis

## Verified external status

**ESTABLISHED BY MACHINE CHECKS, NOT YET PEER-REFEREED:** The announcement
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

The human-readable proof has not been published as a refereed paper.  Therefore
this project treats the Lean result as externally machine-verified, but not as
a replacement for a final mathematical literature/peer-review assessment.

## Potentially useful intermediate machinery

The published archive is too large to use as a single source of a Legendre
inequality.  The direct terminal statement only supplies RH/GRH.  Any proposed
Legendre use must locate an actual stronger intermediate theorem in the Lean
code or paper; raw RH does not imply any known extra uniform gap bound merely
by the mere fact of a formal proof.
